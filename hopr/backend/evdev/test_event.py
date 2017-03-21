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
from evdev import ecodes as e, InputEvent

import etype
from event import *

class Tests(ut.TestCase):
    def test(self):
        ev = Event(InputEvent(sec=0, usec=0,
                              type=e.EV_KEY,
                              code=e.KEY_TAB,
                              value=etype.KEY_PRESS))

        self.assertEqual('PRESS', ev.type)
        self.assertEqual('TAB', ev.key)

        self.assertEqual('PRESS TAB(15)', str(ev))
        self.assertEqual("Event(type='PRESS', key='TAB(15)')", repr(ev))
        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
