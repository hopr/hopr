# -*- coding: utf-8 -*-
#
# This file is part of hopr: https://github.com/hopr/hopr.
#
# Hopr is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hopr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hopr.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from evdev import ecodes
from time import sleep
from .kbdoutput import make_virtual_kbd

def run():
    with make_virtual_kbd() as kbd:
        kbd.press(ecodes.KEY_LEFTSHIFT)
        kbd.sync()
        print('Check shift is pressed')
        sleep(5)
    print('Check shift is not pressed')



def run_with_exception():
    with make_virtual_kbd() as kbd:
        kbd.press(ecodes.KEY_LEFTSHIFT)
        kbd.sync()
        print('Check shift is pressed')
        sleep(5)
        raise ValueError()
    
    print('Check shift is not pressed')



if __name__ == "__main__":
    run_with_exception()
