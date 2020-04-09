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
from hopr.tool.config import *

# TODO: HACK: Use __file__ to find config directory. Improve.
# base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
# config_dir = os.path.join(base_dir, 'config')


# TODO: Clean up notation. Symbols vs keys etc. Physical keys vs symbols/characters.
class ParseLayersTests(ut.TestCase):
    def setUp(self):
        self.key_names = KeyNames(names=list(u'abcdefghijklmnopqrstuvxyz'.upper())
                                  + u'semicolon shift ctrl'.upper().split(),
                                  aliases={})


    def test21_parse_layers(self):
        key_map = parse_layers(layers={'x': {'a': 'q',
                                             'b': 'r'}},
                               symbols={},
                               key_names=self.key_names)

        self.assertEqual({pretty_key(('x', 'a')): pretty_key('q'),
                          pretty_key(('x', 'b')): pretty_key('r')},
                         key_map)


    def test22_empty_layer_is_used_for_key_rebinding(self):
        key_map = parse_layers(layers={'': {'a': 'q',
                                            'b': 'r'}},
                               symbols={},
                               key_names=self.key_names)

        self.assertEqual({pretty_key('a'): pretty_key('q'),
                          pretty_key('b'): pretty_key('r')},
                         key_map)


    def test2_error_if_not_key(self):
        parse_layers(layers={'x': {'y': 'z'}},
                     symbols={},
                     key_names=self.key_names) # No error
        
        self.assertRaises(ParseError,
                          parse_layers,
                          layers={'DUMMY': {'y': 'z'}},
                          symbols={},
                          key_names=self.key_names)
        
        self.assertRaises(ParseError,
                          parse_layers,
                          layers={'x': {'DUMMY': 'z'}},
                          symbols={}, key_names=self.key_names)
        
        self.assertRaises(ParseError,
                          parse_layers,
                          layers={'x': {'y': 'DUMMY'}},
                          symbols={},
                          key_names=self.key_names)
        
        
    def test2_parse_layers_double_modifiers(self):
        key_map = parse_layers(layers={('x', 'y'): {'a': 'q'}},
                               symbols={},
                               key_names=self.key_names)

        self.assertEqual({pretty_key((('x', 'y'), 'a')): pretty_key('q')},
                           key_map)

                             
    def test2_parse_layers_modified_key(self):
        key_map = parse_layers(layers={'x': {'a': ('shift', 'q')}},
                               symbols={},
                               key_names=self.key_names)

        self.assertEqual({pretty_key(('x', 'a')): pretty_key(('shift', 'q'))},
                           key_map)


       
    def test2_parse_layers_map_to_symbol(self):
        key_map = parse_layers(layers={'x': {'a': ';',
                                             'b': ':',
                                             }},
                               symbols={';': 'semicolon',
                                        ':': ('shift', 'semicolon'),
                                        },
                               key_names=self.key_names)

        self.assertEqual({pretty_key(('x', 'a')): pretty_key('semicolon'),
                          pretty_key(('x', 'b')): pretty_key(('shift', 'semicolon'))},
                         key_map)

    def test3_extended_syntax(self):
        key_map = parse_layers(layers={'x': {'a': u'ctrl+shift+q',
                                             'b': u'ctrl+r',
                                             }},
                               symbols={}, key_names=self.key_names)

        self.assertEqual({pretty_key(('x', 'a')): pretty_key((('ctrl', 'shift'), 'q')),
                            pretty_key(('x', 'b')): pretty_key(('ctrl', 'r'))},
                           key_map)

    def test4_ignore_empty_definitions(self):
        key_map = parse_layers(layers={'x': {'a': u'q',
                                             'b': u'',
                                             }},
                               symbols={},
                               key_names=self.key_names)

        self.assertEqual({pretty_key(('x', 'a')): pretty_key('q')}, key_map)



class TestModifiers(ut.TestCase):
    def test(self):
        self.assertEqual({'A':'B',
                            'C':'D'},
                           parse_modifiers({'a':'b',
                                            'c':'d',
                                            'x':''}))


def check_layers(layers, key_names):
    for kmap in list(layers.items()):
        (from_mods, from_key), (to_mods, to_key) = kmap
        for key in (from_key, to_key) + from_mods + to_mods:
            if key not in key_names:
                raise ValueError("Faulty key name '{}' in {} ".format(key, kmap))



import os
class TestConfig(ut.TestCase):
    def setUp(self):
        self.config = load_config(default_config_dir())

    def test10_key_names(self):
        a = self.config.key_names
        self.assertTrue(isinstance(a.names, set))
        self.assertTrue('LEFTSHIFT' in a.names)
        
        self.assertTrue(isinstance(a.aliases, dict))
        self.assertEqual(a.aliases['SHIFT'], 'LEFTSHIFT')


    def test11_layout(self):
        a = self.config.keyboard_layout
        self.assertTrue(type(a.symbols) is dict)
        # TODO: ??? Format does not match layer definitions: (<mods tuple>, <key>)
        self.assertEqual(a.symbols['('], ('LEFTSHIFT', '8'))


    def test12_load_keybindings(self):
        a = self.config.key_bindings
        self.assertTrue(type(a.layers) is dict)
        self.assertEqual(((), 'DOWN'), a.layers[(('SPACE',), 'J')])
        self.assertEqual((('LEFTSHIFT',), '8'), a.layers[(('D',), 'J')])
        
        self.assertTrue(type(a.modifiers) is dict)
        self.assertEqual(a.modifiers['F'], ('LEFTSHIFT',))
        
        self.assertTrue(type(a.passthrough) is set)
        self.assertTrue('LEFTSHIFT' in a.passthrough)
        
        self.assertTrue(type(a.on_off) is str)

    def test3_load_app_config(self):
        a = self.config.app
        self.assertTrue(isinstance(a.send_unknown_chord, bool))



if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
