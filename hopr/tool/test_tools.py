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
from pprint import pprint
 
from tools import *

class Tests(ut.TestCase):
    def test11_single_key(self):
        self.assertEqual(((), 'A'), pretty_key('a'))

    def test12_single_modifier(self):
        self.assertEqual((('X',), 'A'), pretty_key(('x', 'a')))

    def test13_many_modifiers(self):
        self.assertEqual((('X', 'Y'), 'A'), pretty_key((['x', 'y'], 'a')))

    def test13_modifiers_are_sorted(self):
        self.assertEqual((('X', 'Y'), 'A'), pretty_key((['y', 'x'], 'a')))

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
