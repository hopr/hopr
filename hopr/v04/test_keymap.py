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
from hopr.tool.tools import pretty_key

from .keymap import KeyMap

class Tests(ut.TestCase):
    def setUp(self):
        self.map = KeyMap(chords={}, modifiers={})

    def test11_single_key(self):
        self.assertEqual(((), 'A'), self.map(['A'], 0))

    def test11_first_key_released_before_second(self):
        self.assertEqual(((), 'A'), self.map(['A', 'B'], 0))

    def test12_mapped_chord(self):
        self.map.chords = {pretty_key(('X', 'A')): pretty_key('B')}
        self.assertEqual(((), 'B'), self.map(['X', 'A'], 1))

    def test2_chords_are_independent_of_modifier_order(self):
        self.map.chords = {pretty_key((['X', 'Y', 'Z'], 'A')): pretty_key('B')}

        self.assertEqual(((), 'B'), self.map(['X', 'Y', 'Z', 'A'], 3))
        self.assertEqual(((), 'B'), self.map(['Y', 'X', 'Z', 'A'], 3))
        self.assertEqual(((), 'B'), self.map(['Z', 'X', 'Y', 'A'], 3))

    def test30_modifiers(self):
        self.map.modifiers = {'F': ('SHIFT',)}
        self.assertEqual((('SHIFT',), 'A'), self.map(['F', 'A'], 1))

    def test31_two_modifiers(self):
        self.map.modifiers = {'F': ('SHIFT',),
                              'G': ('CTRL',),
                              }
        
        self.assertEqual((('SHIFT', 'CTRL'), 'A'), self.map(['F', 'G', 'A'], 2))
        self.assertEqual((('SHIFT', 'CTRL'), 'A'), self.map(['G', 'F', 'A'], 2))

    def test31_two_modifiers_on_one_key(self):
        self.map.modifiers = {'F': ('SHIFT', 'CTRL'),
                              'G': ('ALT',),
                              }
        
        self.assertEqual((('SHIFT', 'CTRL'), 'A'), self.map(['F', 'A'], 1))
        self.assertEqual((('SHIFT', 'CTRL', 'ALT'), 'A'), self.map(['F', 'G', 'A'], 2))


    def test32_modifier_and_chord(self):
        self.map.modifiers = {'F': ('SHIFT',)}
        self.map.chords = {pretty_key(('X', 'A')): pretty_key(('CTRL', 'B'))}
        
        self.assertEqual((('SHIFT', 'CTRL'), 'B'), self.map(['F', 'X', 'A'], 2))
        self.assertEqual((('SHIFT', 'CTRL'), 'B'), self.map(['X', 'F', 'A'], 2))


    def test32_unmapped_chord(self):
        self.map.chords = {pretty_key(('X', 'A')): None}
        self.assertEqual((), self.map(['X', 'A'], 1))


    def test5_errors(self):
        self.assertRaises(IndexError, self.map, [], 0)
        self.assertRaises(IndexError, self.map, ['X'], 1)




if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
