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

import evdev
from evdev import ecodes

KEY_RELEASE = 0L
KEY_PRESS = 1L
KEY_HOLD = 2L

def write_key(ui, key):
    name = 'KEY_' + key.upper()
    code = ecodes.ecodes[name]
    print("Pressing " + name)
    ui.write(ecodes.EV_KEY, code, KEY_PRESS)
    print("Releasing " + name)
    ui.write(ecodes.EV_KEY, code, KEY_RELEASE)
    ui.syn()

def write(ui, text):
    for char in text:
        write_key(ui, char)

def run():
    print('This program tests uinput by typing "catCAT"')
    
    ui = evdev.UInput()
    write(ui, 'cat')
    print("Pressing KEY_LEFTSHIFT")
    ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, KEY_PRESS)
    write(ui, 'cat')
    print("Releasing KEY_LEFTSHIFT")
    ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, KEY_RELEASE)
    ui.syn()
    ui.close()


if __name__ == "__main__":
    run()









