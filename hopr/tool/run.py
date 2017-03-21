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


import argparse
import logging
from contextlib import contextmanager
from time import time
from pprint import pprint

class Timeout(object):
    def __init__(self, t):
        self.t = time() + t

    def __call__(self):
        return time() > self.t

never_timeout = lambda : False

@contextmanager
def do_not_grab_keyboards():
    yield

def set_log_level(name):
    logging.basicConfig(level=name.upper())

def parse_args(args):
    p = argparse.ArgumentParser()
    p.add_argument('--no-grab', action='store_true')
    p.add_argument('-t', '--timeout', default=5, type=float)
    p.add_argument('-x',
                   dest='timeout',
                   help='Run with no timeout',
                   action='store_const',
                   const=0)

    p.add_argument('--log-level',
                   type=str,
                   default='debug',
                   choices='debug info warning error critical'.split())

    p.add_argument('--print-keymap', action='store_true')

    return p.parse_args(args)


class Run(object):
    def __init__(self,
                 parser,
                 event_wrapper,
                 find_keyboards,
                 read_events,
                 grab_keyboards):
        self.parser = parser
        self.event_wrapper = event_wrapper
        
        self.find_keyboards = find_keyboards
        self.read_events = read_events
        self.grab_keyboards = grab_keyboards

    def run(self,
            timeout=5,
            no_grab=True,
            log_level='error',
            print_keymap=False):

        set_log_level(log_level)

        if print_keymap:
            # TODO: HACK: Fix.
            pprint(self.parser.key_map.chords)
            pprint(self.parser.key_map.modifiers)
            return

        if timeout:
            logging.info('Automatic timeout in {}s'.format(timeout))
            is_timeout = Timeout(timeout)
        else:
            is_timeout = never_timeout

        kbds = self.find_keyboards()    

        logging.info('Found keyboards:')
        logging.info('\n'.join(str(kbd) for kbd in kbds))

        # NOTE: Keys can get stuck if exceptions occur after the keyboard was grabbed.
        #       i.e. ctrl is held when program starts, keyboard is grabbed and an exception occurs before release event is sent
        if not no_grab:
            logging.info('Grabbing keyboards')
            grab_keyboards = self.grab_keyboards(kbds)
        else:
            grab_keyboards = do_not_grab_keyboards() 

        with grab_keyboards: 
            for ev in self.read_events(kbds):
                if is_timeout():
                    break

                self.parser(self.event_wrapper(ev))



    def run_parse_args(self, args):
        x = parse_args(args)
        self.run(**vars(x))


if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_run', failfast=True, exit=False)

