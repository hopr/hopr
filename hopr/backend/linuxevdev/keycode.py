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


import evdev.ecodes as e

def evdev_name(name):
    return 'KEY_' + name.upper()

def keycode(name):
    try:
        return e.ecodes[evdev_name(name)]
    except Exception as exc:
        raise ValueError('Unknown key name: {!r}\n{}'.format(name, exc))

def keyname(code):
    # HACK: key names are compatible with evdev key names
    name = e.keys[code]
    if not isinstance(name, str):
        name = name[0]

    return name[4:].upper()



if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_keycode', failfast=True, exit=False)

