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


import asyncio

from typing import List

from aiohttp.web import Request
from aiohttp.web import Response

from ....validators.kvm import valid_info_fields

from ..info import InfoManager

from ..http import exposed_http
from ..http import make_json_response

from ....logging import get_logger

# =====
class InfoApi:
    def __init__(self, info_manager: InfoManager) -> None:
        get_logger(0).debug("start InfoApi init()")
        self.__info_manager = info_manager
        get_logger(0).debug("end InfoApi init()")


    # =====

    @exposed_http("GET", "/info")
    async def __common_state_handler(self, request: Request) -> Response:
        fields = self.__valid_info_fields(request)
        results = dict(zip(fields, await asyncio.gather(*[
            self.__info_manager.get_submanager(field).get_state()
            for field in fields
        ])))
        return make_json_response(results)

    def __valid_info_fields(self, request: Request) -> List[str]:
        subs = self.__info_manager.get_subs()
        return sorted(valid_info_fields(
            arg=request.query.get("fields", ",".join(subs)),
            variants=subs,
        ) or subs)
