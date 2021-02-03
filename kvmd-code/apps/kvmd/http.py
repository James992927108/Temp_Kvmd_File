# ========================================================================== #
#                                                                            #
#    KVMD - The main Pi-KVM daemon.                                          #
#                                                                            #
#    Copyright (C) 2018  Maxim Devaev <mdevaev@gmail.com>                    #
#                                                                            #
#    This program is free software: you can redistribute it and/or modify    #
#    it under the terms of the GNU General Public License as published by    #
#    the Free Software Foundation, either version 3 of the License, or       #
#    (at your option) any later version.                                     #
#                                                                            #
#    This program is distributed in the hope that it will be useful,         #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#    GNU General Public License for more details.                            #
#                                                                            #
#    You should have received a copy of the GNU General Public License       #
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.  #
#                                                                            #
# ========================================================================== #


import os
import socket
import dataclasses
import inspect
import json

from typing import List
from typing import Dict
from typing import Callable
from typing import Optional

import aiohttp
import aiohttp.web

try:
    from aiohttp.web import AccessLogger  # type: ignore
except ImportError:
    from aiohttp.helpers import AccessLogger  # type: ignore

from ...logging import get_logger

from ...validators import ValidatorError


# =====
class HttpError(Exception):
    def __init__(self, msg: str, status: int) -> None:
        super().__init__(msg)
        self.status = status


class UnauthorizedError(HttpError):
    def __init__(self) -> None:
        super().__init__("Unauthorized", 401)


class ForbiddenError(HttpError):
    def __init__(self) -> None:
        super().__init__("Forbidden", 403)


class UnavailableError(HttpError):
    def __init__(self) -> None:
        super().__init__("Service Unavailable", 503)


# =====
@dataclasses.dataclass(frozen=True)
class HttpExposed:
    method: str
    path: str
    auth_required: bool
    handler: Callable


_HTTP_EXPOSED = "_http_exposed"
_HTTP_METHOD = "_http_method"
_HTTP_PATH = "_http_path"
_HTTP_AUTH_REQUIRED = "_http_auth_required"


def exposed_http(http_method: str, path: str, auth_required: bool=True) -> Callable:
    def set_attrs(handler: Callable) -> Callable:
        setattr(handler, _HTTP_EXPOSED, True)
        setattr(handler, _HTTP_METHOD, http_method)
        setattr(handler, _HTTP_PATH, path)
        setattr(handler, _HTTP_AUTH_REQUIRED, auth_required)
        return handler
    return set_attrs


def get_exposed_http(obj: object) -> List[HttpExposed]:
    return [
        HttpExposed(
            method=getattr(handler, _HTTP_METHOD),
            path=getattr(handler, _HTTP_PATH),
            auth_required=getattr(handler, _HTTP_AUTH_REQUIRED),
            handler=handler,
        )
        for handler in [getattr(obj, name) for name in dir(obj)]
        if inspect.ismethod(handler) and getattr(handler, _HTTP_EXPOSED, False)
    ]


# =====
@dataclasses.dataclass(frozen=True)
class WsExposed:
    event_type: str
    handler: Callable


_WS_EXPOSED = "_ws_exposed"
_WS_EVENT_TYPE = "_ws_event_type"


def exposed_ws(event_type: str) -> Callable:
    def set_attrs(handler: Callable) -> Callable:
        setattr(handler, _WS_EXPOSED, True)
        setattr(handler, _WS_EVENT_TYPE, event_type)
        return handler
    return set_attrs


def get_exposed_ws(obj: object) -> List[WsExposed]:
    return [
        WsExposed(
            event_type=getattr(handler, _WS_EVENT_TYPE),
            handler=handler,
        )
        for handler in [getattr(obj, name) for name in dir(obj)]
        if inspect.ismethod(handler) and getattr(handler, _WS_EXPOSED, False)
    ]


# =====
def make_json_response(
    result: Optional[Dict]=None,
    status: int=200,
    set_cookies: Optional[Dict[str, str]]=None,
    wrap_result: bool=True,
) -> aiohttp.web.Response:

    response = aiohttp.web.Response(
        text=json.dumps(({
            "ok": (status == 200),
            "result": (result or {}),
        } if wrap_result else result), sort_keys=True, indent=4),
        status=status,
        content_type="application/json",
    )
    if set_cookies:
        for (key, value) in set_cookies.items():
            response.set_cookie(key, value)
    return response


def make_json_exception(err: Exception, status: Optional[int]=None) -> aiohttp.web.Response:
    name = type(err).__name__
    msg = str(err)
    if isinstance(err, HttpError):
        status = err.status
    else:
        get_logger().error("API error: %s: %s", name, msg)
    assert status is not None, err
    return make_json_response({
        "error": name,
        "error_msg": msg,
    }, status=status)


# =====
async def get_multipart_field(reader: aiohttp.MultipartReader, name: str) -> aiohttp.BodyPartReader:
    field = await reader.next()
    if not isinstance(field, aiohttp.BodyPartReader):
        raise ValidatorError(f"Expected body part as {name!r} field")
    if not field or field.name != name:
        raise ValidatorError(f"Missing {name!r} field")
    return field


# =====
_REQUEST_AUTH_INFO = "_kvmd_auth_info"


def _format_P(request: aiohttp.web.BaseRequest, *_, **__) -> str:  # type: ignore  # pylint: disable=invalid-name
    return (getattr(request, _REQUEST_AUTH_INFO, None) or "-")


AccessLogger._format_P = staticmethod(_format_P)  # type: ignore  # pylint: disable=protected-access


def set_request_auth_info(request: aiohttp.web.BaseRequest, info: str) -> None:
    setattr(request, _REQUEST_AUTH_INFO, info)


# =====
class HttpServer:
    def run(
        self,
        host: str,
        port: int,
        unix_path: str,
        unix_rm: bool,
        unix_mode: int,
        access_log_format: str,
    ) -> None:

        assert port or unix_path
        if unix_path:
            socket_kwargs: Dict = {}
            if unix_rm and os.path.exists(unix_path):
                os.remove(unix_path)
            server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            server_socket.bind(unix_path)
            if unix_mode:
                os.chmod(unix_path, unix_mode)
            socket_kwargs = {"sock": server_socket}
        else:
            socket_kwargs = {"host": host, "port": port}

        aiohttp.web.run_app(
            app=self._make_app(),
            access_log_format=access_log_format,
            print=self.__run_app_print,
            **socket_kwargs,
        )

    async def _make_app(self) -> aiohttp.web.Application:
        raise NotImplementedError

    def __run_app_print(self, text: str) -> None:
        logger = get_logger(0)
        for line in text.strip().splitlines():
            logger.info(line.strip())
