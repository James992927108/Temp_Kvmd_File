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


from typing import Type

from .. import BasePlugin
from .. import get_plugin_class

from ...logging import get_logger


# =====
class BaseAuthService(BasePlugin):
    async def authorize(self, user: str, passwd: str) -> bool:
        raise NotImplementedError  # pragma: nocover

    async def cleanup(self) -> None:
        pass


# =====
def get_auth_service_class(name: str) -> Type[BaseAuthService]:
    get_logger(0).debug("auth -> name %r", name)
    return get_plugin_class("auth", name)  # type: ignore
