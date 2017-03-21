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
from mock import MagicMock, sentinel, call


from run import Run, parse_args

class TestParseArgs(ut.TestCase):
    def setUp(self):
        self.args = {'no_grab': False,
                     'timeout': 5,
                     'log_level': 'debug',
                     'print_keymap': False,
                     }
        
    def test2_parse_args(self):
        x = parse_args('--no-grab -t 10 --log-level warning'.split())
        self.args.update({'no_grab': True,
                          'timeout': 10,
                          'log_level': 'warning',
                          })

        self.assertEqual(self.args, vars(x))


    def test2_no_timeout(self):
        x = parse_args('-x'.split())
        self.args.update({'timeout': 0})
        self.assertEqual(self.args, vars(x))
        
    def test1_parse_args_defaults(self):
        x = parse_args(''.split())
        self.assertEqual({'no_grab': False,
                          'timeout': 5,
                          'log_level': 'debug',
                          'print_keymap': False,
                          }, vars(x))

class TestRun(ut.TestCase):
    def setUp(self):
        self.run = Run(parser=MagicMock(name='parser'),
                       event_wrapper=MagicMock(name='event_wrapper'),
                       find_keyboards=MagicMock(name='find_keyboards'),
                       read_events=MagicMock(name='read_events'),
                       grab_keyboards=MagicMock(name='grab_keyboards'))

    def test1_no_events(self):
        self.run.run(timeout=5,
                     no_grab=True,
                     log_level='error')

    def test2_keyboards_are_optionally_grabbed(self):
        kbds = [sentinel.kbd1, sentinel.kbd2]
        self.run.find_keyboards.return_value = kbds
        self.run.run(no_grab=True)
        self.run.grab_keyboards.assert_not_called()

        self.run.run(no_grab=False)
        self.run.grab_keyboards.assert_called_once_with(kbds)

    def test2_keyboards_events_are_read(self):
        kbds = [sentinel.kbd1, sentinel.kbd2]
        
        self.run.find_keyboards.return_value = kbds
        self.run.run()
        self.run.read_events.assert_called_once_with(kbds)

    def test2_events_are_wrapped_before_parsing(self):
        events = [sentinel.event]
        self.run.read_events.return_value = events
        self.run.event_wrapper.return_value = sentinel.wrapped_event
        self.run.run()
        self.run.event_wrapper.assert_called_once_with(sentinel.event)
        self.run.parser.assert_called_once_with(sentinel.wrapped_event)


    def test2_events_are_sent_to_parser(self):
        events = [sentinel.event1, sentinel.event2]
        self.run.read_events.return_value = events
        self.run.event_wrapper.side_effect = lambda x : x
        self.run.run()
        self.run.parser.assert_has_calls([call(e) for e in events])


    def test3_timeout(self):
        self.run.run(timeout=-1)
        
        


if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
