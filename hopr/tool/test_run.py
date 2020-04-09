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
import tempfile

from mock import MagicMock, sentinel, call


from hopr.tool.run import *  # Run, parse_args, run


# TODO: Suppress log output during tests.
class Test1Misc(ut.TestCase):
    def test_timeout(self):
        dt = 0.01
        e = 0.001

        timeout = Timeout(dt)
        t1 = time()
        while(True):
            a = timeout()
            t2 = time()
            
            if t2 - t1 < dt-e:
                self.assertEqual(a, False)
            else:
                break

        while(t2 - t1 <= dt + e):
            t2 = time()

        self.assertEqual(timeout(), True)
            

class TestParseArgs(ut.TestCase):
    def setUp(self):
        self.args = {'no_grab': False,
                     'timeout': 5,
                     'log_level': 'info',
                     'print_keymap': False,
                     'log_file': '',
                     'config_dir': '',
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
                          'log_level': 'info',
                          'log_file': '',
                          'config_dir': '',
                          'print_keymap': False,
                          }, vars(x))

    def test1_parse_args_defaults(self):
        x = parse_args('--log-file log.txt'.split())
        self.assertEqual({'no_grab': False,
                          'timeout': 5,
                          'log_level': 'info',
                          'log_file': 'log.txt',
                          'config_dir': '',
                          'print_keymap': False,
                          }, vars(x))

class TestRun(ut.TestCase):
    def setUp(self):
        params = dict(event_parser=MagicMock(name='parser'),
                      event_wrapper=MagicMock(name='event_wrapper'),
                      find_keyboards=MagicMock(name='find_keyboards'),
                      read_events=MagicMock(name='read_events'),
                      grab_keyboards=MagicMock(name='grab_keyboards'))
        
        for k,v in list(params.items()):
            setattr(self, k, v)

        self.run = partial(run, **params)

    def test1_no_events(self):
        self.run(timeout=5,
                 no_grab=True)
                     

    def test2_keyboards_are_optionally_grabbed(self):
        kbds = [sentinel.kbd1, sentinel.kbd2]
        self.find_keyboards.return_value = kbds
        self.run(no_grab=True)
        self.grab_keyboards.assert_not_called()

        self.run(no_grab=False)
        self.grab_keyboards.assert_called_once_with(kbds)

    def test2_keyboards_events_are_read(self):
        kbds = [sentinel.kbd1, sentinel.kbd2]
        
        self.find_keyboards.return_value = kbds
        self.run()
        self.read_events.assert_called_once_with(kbds)

    def test2_events_are_wrapped_before_parsing(self):
        events = [sentinel.event]
        self.read_events.return_value = events
        self.event_wrapper.return_value = sentinel.wrapped_event
        self.run()
        self.event_wrapper.assert_called_once_with(sentinel.event)
        self.event_parser.assert_called_once_with(sentinel.wrapped_event)


    def test2_events_are_sent_to_parser(self):
        events = [sentinel.event1, sentinel.event2]
        self.read_events.return_value = events
        self.event_wrapper.side_effect = lambda x : x
        self.run()
        self.event_parser.assert_has_calls([call(e) for e in events])


    def test3_timeout(self):
        self.run(timeout=-1)
        
        
class TestRunFunction(ut.TestCase):
    def test(self):
        backend = MagicMock(name='backend')
        make_eventparser = MagicMock(name='make_eventparser')
        args = '--log-level=error'.split()
        run_parse_args(backend=backend,
                       make_eventparser=make_eventparser,
                       args=args)

    def test_log_file(self):
        f = tempfile.NamedTemporaryFile('r')
        backend = MagicMock(name='backend')
        make_eventparser = MagicMock(name='make_eventparser')
        args = ['--log-level', 'debug', '--log-file', f.name]
        run_parse_args(backend=backend,
                       make_eventparser=make_eventparser,
                       args=args)

        logging.getLogger().debug('Test Message')

        text = f.read()
        self.assertTrue(text.strip().endswith('Test Message'))
        
        



if __name__ == "__main__":
    # import logging
    # logging.getLogger().setLevel('ERROR')
    ut.main(failfast=True, exit=False)
    
