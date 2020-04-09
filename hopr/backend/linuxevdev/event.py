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
from builtins import object
import evdev
# print(evdev.__file__)

from evdev import ecodes
from hopr.backend.linuxevdev import keycode
from hopr.backend.linuxevdev import etype

def pretty_key(code):
    if code is None:
        return 'None'
    
    key = ecodes.keys[code].replace('KEY_', '')
    return '{}({})'.format(key, code)


class Event(object):
    def __init__(self, ev):
        self.event = ev

    @property
    def type(self):
        return etype.name(self.event.value)

    @property
    def key(self):
        # TODO: Key naming scheme. Use for both config and pretty printing.
        # return pretty_key(self.event.code)
        return keycode.keyname(self.event.code)

    def __str__(self):
        return '{} {}'.format(self.type, pretty_key(self.event.code))

    def __repr__(self):
        return 'Event(type={!r}, key={!r})'.format(self.type, pretty_key(self.event.code))

    def is_press(self):
        return etype.is_press(self.event)

    def is_release(self):
        return etype.is_release(self.event)


if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_event', failfast=True, exit=False)

