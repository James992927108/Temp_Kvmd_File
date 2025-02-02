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


import sys
import types
import logging
import coloredlogs

from typing import Optional


# =====

def get_logger(depth: int=1) -> logging.Logger:
    frame: Optional[types.FrameType] = sys._getframe(1)  # pylint: disable=protected-access
    assert frame
    frames = []
    while frame:
        frames.append(frame)
        frame = frame.f_back
        if len(frames) - 1 >= depth:
            break
    name = frames[depth].f_globals["__name__"]

    # Anthony add ->
    my_logger = logging.getLogger(name)
    my_logger.setLevel(level=logging.DEBUG) # if use coloredlogs setLevel is not work
    # my_fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)i - %(message)s')
    my_fmt = "%(asctime)s %(levelname)s %(name)s Fun:{ %(funcName)s } LineNo:{ %(lineno)i } %(message)s"
    coloredlogs.install(level='DEBUG',logger = my_logger, fmt = my_fmt)
    # <- 
    return my_logger
