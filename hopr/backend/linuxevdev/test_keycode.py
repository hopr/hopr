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


import unittest as ut
from evdev import ecodes

from keycode import *

class Tests(ut.TestCase):
    def test1_name(self):
        self.assertEqual('KEY_F', evdev_name('F'))
        self.assertEqual('KEY_F', evdev_name('f'))
        self.assertEqual('KEY_TAB', evdev_name('TAB'))
        self.assertEqual('KEY_TAB', evdev_name('Tab'))
        self.assertEqual('KEY_TAB', evdev_name('tAb'))

    def test2_key(self):
        self.assertEqual(keycode('F'), keycode('f'))
        self.assertEqual(ecodes.KEY_TAB, keycode('TAB'))
        self.assertEqual(ecodes.KEY_TAB, keycode('Tab'))
        self.assertEqual(ecodes.KEY_LEFTSHIFT, keycode('leftShift'))

    def test3_roundtrip(self):
        for (ename, code) in ecodes.ecodes.items():
            try:
                if (ename.startswith('KEY_')
                    # HACK: KEY_CNT and KEY_MAX are special
                    and not ename in 'KEY_CNT KEY_MAX'.split()
                    # Ignore keys with multiple names
                    and isinstance(ecodes.keys[code], basestring)):                   
                    name = ename[4:].upper()
                    self.assertEqual(code, keycode(name))
                    self.assertEqual(name, keyname(code))
            except:
                print(ename)
                raise

    def test4_name(self):
        self.assertEqual('A', keyname(ecodes.KEY_A))
        self.assertEqual('ENTER', keyname(ecodes.KEY_ENTER))


        

        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
