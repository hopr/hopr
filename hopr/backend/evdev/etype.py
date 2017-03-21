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

# evdev event type values
from evdev import ecodes
KEY_RELEASE = 0L
KEY_PRESS = 1L
KEY_HOLD = 2L

_name = {KEY_PRESS: 'PRESS',
         KEY_RELEASE: 'RELEASE',
         KEY_HOLD: 'HOLD',
         }

def name(code):
    return _name[code]

_code = dict((name, code) for (code, name) in _name.items())

def code(name):
    return _code[name]
    

def is_press(ev):
    return (ev.type == ecodes.EV_KEY and ev.value == KEY_PRESS)


def is_release(ev):
    return (ev.type == ecodes.EV_KEY and ev.value == KEY_RELEASE)
