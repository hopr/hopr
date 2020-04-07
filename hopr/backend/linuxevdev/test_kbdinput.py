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
import unittest as ut

from evdev import UInput
from .kbdinput import *

class Tests(ut.TestCase):
    # TODO: NOTE: Need read permissions on /dev/input/* to work
    def test1_find_keyboards(self):
        kbds = find_keyboards()
        self.assert_(len(kbds) >= 1)

    def test2_uinput_not_in_keyboards(self):
        with UInput() as ui:
            kbds = find_keyboards()
            devices = set([k.fn for k in kbds])
            self.assert_(ui.device.fn not in devices, 'UInput must not be listed as keyboard')


    def test2_read_key_press_release(self):
        # TODO: Implement tests.
        pass



if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
