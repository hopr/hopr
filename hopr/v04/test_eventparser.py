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
import mock
from hopr.tool.mockevent import Event, parse_events
from hopr.v04.eventparser import EventParser, logging

from keymap import KeyMap
from hopr.tool.tools import pretty_key

def return_released_key(pressed_keys, released_index):
    return ((), pressed_keys[released_index])

def return_chord(pressed_keys, released_index):
    return (tuple(sorted(pressed_keys[:released_index])), pressed_keys[released_index])

class Keyboard(object):
    def __init__(self):
        self.events_list = []

    @property
    def events(self):
        return ' '.join(self.events_list)

    def press(self, key):
        self.events_list.append('p' + key.lower())

    def release(self, key):
        self.events_list.append('r' + key.lower())

    def sync(self):
        self.events_list.append('s')
    


class Test1EventParser(ut.TestCase):
    def setUp(self):
        self.kbd = Keyboard()
        self.key_map = mock.MagicMock()        
        self.parser = EventParser(self.key_map,
                                  kbd=self.kbd,
                                  on_off_key='esc',
                                  passthrough_keys=['shift'])




    def test11_press_and_release_key(self):
        self.key_map.side_effect = return_released_key
        
        self.parser(Event('pa'))
        self.assertEqual(['A'], self.parser.pressed_keys)
        self.assertEqual('', self.kbd.events)
        self.key_map.assert_not_called()

        self.parser(Event('ra'))
        self.assertEqual([], self.parser.pressed_keys)
        self.assertEqual('pa ra s', self.kbd.events)
        # NOTE: Mock objects keeps refs to passed params. List is modified after call.
        self.key_map.assert_called_once_with(self.parser.pressed_keys, 0)

    def test12_two_interleaved_keys_pab_rab(self):
        self.key_map.side_effect = return_released_key
        
        map(self.parser, parse_events('pa pb'))
        self.key_map.assert_not_called()
        self.assertEqual(['A', 'B'], self.parser.pressed_keys)
        self.assertEqual('', self.kbd.events)
        
        self.parser(Event('ra'))
        self.assertEqual(['B'], self.parser.pressed_keys)
        self.assertEqual('pa ra s', self.kbd.events)

        # NOTE: Event order is NOT preserved
        self.parser(Event('rb'))
        self.assertEqual([], self.parser.pressed_keys)
        self.assertEqual('pa ra s pb rb s', self.kbd.events)

    def test14_three_keys_pabc_rbac(self):
        self.key_map.side_effect = return_chord
        
        map(self.parser, parse_events('px pb pc rb rx rc'))
        # Two calls to key_map:
        # First mod=x, key=b returns <x+b>
        # Second mod=None, key=c returns <c>
        self.assertEqual('px pb rb s rx s pc rc s', self.kbd.events)

    def test21_key_map(self):
        self.parser.key_map.return_value = ((), 'Q')
        
        map(self.parser, parse_events('pa ra'))
        self.assertEqual('pq rq s', self.kbd.events) 

    def test22_key_mapped_with_one_modifier(self):
        self.parser.key_map.return_value = (('X',), 'Q')
        map(self.parser, parse_events('pa ra'))
        self.assertEqual('px pq rq rx s', self.kbd.events) 

    def test23_key_mapped_with_two_modifiers(self):
        self.parser.key_map.return_value = (('X', 'Y'), 'Q')
        map(self.parser, parse_events('pa ra'))
        self.assertEqual('px py pq rq rx ry s', self.kbd.events) 

    def test24_key_chord_modifier_is_silenced(self):
        self.parser.key_map.side_effect = lambda p, r: ((), 'Q')
        map(self.parser, parse_events('px pb rb rx'))
        self.assertEqual('pq rq s', self.kbd.events) 

    def test23_key_chord_modifiers_are_silenced(self):
        self.parser.key_map.side_effect = lambda p, r: ((), 'Q')
        map(self.parser, parse_events('px py pb rb rx ry'))
        self.assertEqual('pq rq s', self.kbd.events) 

    def test24_key_chord_modifier_order_independence(self):
        self.parser.key_map.side_effect = lambda p, r: ((), 'Q')
        map(self.parser, parse_events('px py pb rb ry rx'))
        self.assertEqual('pq rq s', self.kbd.events)

    @mock.patch('hopr.v04.eventparser.logging.warning', autospec=True)
    def test25_missing_key_map(self, warn):
        self.parser.send_unknown_chord = False
        self.parser.key_map.side_effect = lambda p, r: ((), None)
        map(self.parser, parse_events('px pa ra rx'))
        self.assertEqual('', self.kbd.events)

        self.parser.key_map.side_effect = lambda p, r: None
        map(self.parser, parse_events('px pa ra rx'))
        self.assertEqual('', self.kbd.events)

    def test31_merge_single_modifier(self):
        self.parser.key_map.side_effect = lambda p, r: (('M',), 'Q')

        map(self.parser, parse_events('px pa ra pb rb rx'))
        self.assertEqual('pm pq rq s pq rq s rm s', self.kbd.events)

    def test31_merge_switching_modifiers(self):
        self.parser.key_map.side_effect = lambda p, r: (('M', 'N'), 'Q')
        map(self.parser, parse_events('px py pa ra ry'))
        self.assertEqual('pm pn pq rq s', self.kbd.events)
        
        self.parser.key_map.side_effect = lambda p, r: (('M',), 'R')
        map(self.parser, parse_events('pb rb rx'))
        self.assertEqual('pm pn pq rq s rn pr rr s rm s', self.kbd.events)

    @mock.patch('hopr.v04.eventparser.logging.info', autospec=True)
    def test41_missing_key_mapping(self, warn):
        self.parser.send_unknown_chord = False
        self.parser.key_map.return_value = ()

        map(self.parser, parse_events('pa ra'))
        self.assertEqual('', self.kbd.events)
        warn.assert_called_once_with("Unknown chord: ['A']")

    @mock.patch('hopr.v04.eventparser.logging.warning', autospec=True)
    def test42_unexpected_release_event_is_passed_on_and_logged(self, warn):
        self.parser.key_map.side_effect = return_released_key
        
        self.parser(Event('ra'))
        self.assertEqual('ra s', self.kbd.events)
        warn.assert_called_once_with('Unexpected key release: RELEASE A')

    @mock.patch('hopr.v04.eventparser.logging.warning', autospec=True)
    def test42_unexpected_release_event_is_passed_on_and_logged_again(self, warn):
        self.parser.key_map.side_effect = return_released_key
        
        map(self.parser, parse_events('pa rb ra'))
        self.assertEqual('rb s pa ra s', self.kbd.events)
        warn.assert_called_once_with('Unexpected key release: RELEASE B')

    def test6_misc_combinations(self):
        self.parser.key_map.side_effect = return_chord

        # Press abc, release ca, press d, release b
        map(self.parser, parse_events('pa pb pc rc ra pd rd rb'))
        self.assertEqual('pa pb pc rc s ra pd rd s rb s', self.kbd.events)

    def test71_on_off_switch1(self):
        self.parser.on_off_key = 'ESC'
        map(self.parser, parse_events('pesc pa resc pb ra rb'))
        self.assertEqual('pa s pb s ra s rb s', self.kbd.events)

    @mock.patch('hopr.v04.eventparser.logging.warning', autospec=True)
    def test72_on_off_switch_unexpected_key_release(self, warn):
        self.parser.key_map.return_value = ((), 'Q')
        
        self.parser.on_off_key = 'ESC'
        map(self.parser, parse_events('pesc pa resc pesc ra pa pb resc rb ra'))
        self.assertEqual('pa s ra s pq rq s', self.kbd.events)
        warn.assert_called_once_with('Unexpected key release: RELEASE A')

    def test81_passthrough_keys(self):
        self.parser.key_map.side_effect = return_chord
        
        self.parser.passthrough_keys = set('shift'.upper().split())
        map(self.parser, parse_events('pshift pa rshift pb rb ra'))
        self.assertEqual('pshift s pa s rshift s pb rb s ra s', self.kbd.events)

    def test82_passthrough_modifier_and_key(self):
        self.parser.key_map.side_effect = return_chord
        
        self.parser.passthrough_keys = set('shift'.upper().split())
        map(self.parser, parse_events('pa pshift ra rshift pb rb'))
        self.assertEqual('pa s pshift s ra s rshift s pb rb s', self.kbd.events)

    @mock.patch('hopr.v04.eventparser.logging.info', autospec=True)
    def test9_do_not_send_unrecognized_chord(self, warn):
        self.parser.send_unknown_chord = False
        self.parser.key_map.return_value = None 
        
        map(self.parser, parse_events('pa pb rb ra'))
        self.assertEqual('', self.kbd.events)
        warn.assert_called_once_with("Unknown chord: ['A', 'B']")


    @mock.patch('hopr.v04.eventparser.logging.info', autospec=True)
    def test91_do_send_unrecognized_chord(self, info):
        self.parser.send_unknown_chord = True
        self.parser.key_map.return_value = None 
        
        map(self.parser, parse_events('pa pb rb'))        
        self.assertEqual('pa pb s rb s', self.kbd.events)

        self.parser(Event('ra'))
        self.assertEqual('pa pb s rb s ra s', self.kbd.events)
        info.assert_called_once_with("Unknown chord: ['A', 'B']")



from pprint import pprint
class Test2EventParserWithKeyMap(ut.TestCase):
    def setUp(self):
        self.kbd = Keyboard()
        # NOTE: Modifiers is case sensitive when testing.
        self.key_map = KeyMap(modifiers={'A': ('SHIFT',)},
                              chords={pretty_key(('x', 'b')): pretty_key('c')})

        self.parser = EventParser(key_map=self.key_map,
                                  kbd=self.kbd,
                                  on_off_key=None,
                                  passthrough_keys=[])

    def test11_chord_not_pressed(self):
        map(self.parser, parse_events('px pb rx rb'))
        self.assertEqual('px rx s pb rb s', self.kbd.events)

    def test12_chord_pressed(self):
        map(self.parser, parse_events('px pb rb rx'))
        self.assertEqual('pc rc s', self.kbd.events)

    def test13_modifier_not_pressed(self):
        map(self.parser, parse_events('pa pb ra rb'))
        self.assertEqual('pa ra s pb rb s', self.kbd.events)

    def test14_modifier_pressed(self):
        map(self.parser, parse_events('pa pb rb ra'))
        self.assertEqual('pshift pb rb s rshift s', self.kbd.events)

def find_warning(msg):
    raise msg

if __name__ == "__main__":
    # logging.warning = find_warning
    ut.main(failfast=True, exit=False)
    
