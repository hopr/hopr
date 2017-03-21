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


from mockevent import *

class Tests(ut.TestCase):
    def test1_event(self):
        ev = Event('pany')
        self.assertEqual(PRESS, ev.action)
        self.assertEqual('ANY', ev.key)

        ev = Event('rx')
        self.assertEqual(RELEASE, ev.action)
        self.assertEqual('X', ev.key)

    def test2_str(self):
        self.assertEqual('PRESS ANY', str(Event('pany')))
        self.assertEqual("Event(action='PRESS', key='ANY')", repr(Event('pany')))



if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
