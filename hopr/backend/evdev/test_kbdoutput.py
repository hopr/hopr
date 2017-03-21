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

# -*- coding: utf-8 -*-
import unittest as ut
import evdev.ecodes as e
from mock import patch

import etype

from hopr.backend.evdev.kbdoutput import *

class Tests(ut.TestCase):

    @patch('hopr.backend.evdev.kbdoutput.UInput', autospec=True)
    def setUp(self, ui):
        self.out = KbdOutput()

    def test1_alias(self):
        self.assertEqual(make_virtual_kbd, KbdOutput)
    
    def test1_press(self):
        self.out.press('a')
        self.out.ui.write.assert_called_once_with(e.EV_KEY, e.KEY_A, etype.KEY_PRESS)

    def test1_press_alias(self):
        self.out.press('leftctrl')
        self.out.ui.write.assert_called_once_with(e.EV_KEY, e.KEY_LEFTCTRL, etype.KEY_PRESS)

    def test1_release(self):
        self.out.release('a')
        self.out.ui.write.assert_called_once_with(e.EV_KEY, e.KEY_A, etype.KEY_RELEASE)

    def test1_release(self):
        self.out.sync()
        self.out.ui.syn.assert_called_once_with()

    @patch('hopr.backend.evdev.kbdoutput.UInput', autospec=True)
    def test2_with(self, ui):
        with KbdOutput() as kbd:            
            kbd.press('a')
            kbd.ui.write.assert_called_once_with(e.EV_KEY, e.KEY_A, etype.KEY_PRESS)
            
        kbd.ui.close.assert_called_once_with()

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
