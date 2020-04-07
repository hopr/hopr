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
from builtins import str
from builtins import object
import os
import sys
import argparse
import logging
from functools import partial
from contextlib import contextmanager
from time import time
from pprint import pprint

from . import config

class Timeout(object):
    def __init__(self, t):
        self.end_time = time() + t

    def __call__(self):
        return time() > self.end_time


never_timeout = lambda : False

@contextmanager
def do_not_grab_keyboards():
    yield

def parse_args(args):
    p = argparse.ArgumentParser()
    p.add_argument('--config-dir', default='')
    p.add_argument('--no-grab', action='store_true')
    p.add_argument('-t', '--timeout', default=5, type=float)
    p.add_argument('-x',
                   dest='timeout',
                   help='Run with no timeout',
                   action='store_const',
                   const=0)

    p.add_argument('--log-file', default='')
    p.add_argument('--log-level',
                   type=str,
                   default='info',
                   choices='debug info warning error critical'.split())

    p.add_argument('--print-keymap', action='store_true')

    return p.parse_args(args)

def run(event_parser,
        event_wrapper,
        find_keyboards,
        read_events,
        grab_keyboards, 
        timeout=5,
        no_grab=True,
        print_keymap=False):
    
    if print_keymap:
        # TODO: HACK: Fix.
        pprint(event_parser.key_map.chords)
        pprint(event_parser.key_map.modifiers)
        return

    if timeout:
        logging.info('Automatic timeout in {}s'.format(timeout))
        is_timeout = Timeout(timeout)
    else:
        is_timeout = never_timeout

    kbds = find_keyboards()    

    logging.info('Found keyboards:')
    logging.info('\n'.join(str(kbd) for kbd in kbds))

    # NOTE: Keys can get stuck if exceptions occur after the keyboard was grabbed.
    #       i.e. ctrl is held when program starts, keyboard is grabbed and an exception occurs before release event is sent
    if not no_grab:
        logging.info('Grabbing keyboards')
        grab_keyboards = grab_keyboards(kbds)
    else:
        grab_keyboards = do_not_grab_keyboards() 

    with grab_keyboards: 
        for ev in read_events(kbds):
            if is_timeout():
                break

            event_parser(event_wrapper(ev))



# TODO: Review: Is this filter necessary? Make it part of backend. Only return filtered events?
def is_press_or_release(backend, ev):
    return backend.is_press(ev) or backend.is_release(ev)

def run_config(backend,
               make_eventparser,
               cfg,
               args):
    
    backend.register_signal_handlers()

    with backend.make_virtual_kbd() as kbdout:
        parser = make_eventparser(cfg, kbdout)
        # NOTE: Filter only press/release events (ignore hold for now)
        event_filter = partial(is_press_or_release, backend)

        # TODO: Merge cfg and args. Should be able to use both interchangeably
        run(event_parser=parser,
            event_wrapper=backend.Event,
            read_events=partial(backend.read_events, event_filter=event_filter),
            grab_keyboards=backend.grab,
            find_keyboards=backend.find_keyboards,
            timeout=args.timeout,
            no_grab=args.no_grab,
            print_keymap=args.print_keymap)
                   
                   
def setup_logging(log_file,
                  log_level):

    log = logging.getLogger()
    log.setLevel(log_level.upper())
    
    log.addHandler(logging.StreamHandler())

    if log_file:
        f = logging.FileHandler(log_file, encoding='utf-8')
        f.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        log.addHandler(f)
        
        log.info('Logging to ' + log_file)

def base_dir():
    # TODO: HACK: base_dir depends on location of current file. Unstable.
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))    

def default_config_dir():
    return os.path.join(base_dir(), 'config')

def run_parse_args(backend,
                   make_eventparser,
                   args):

    args = parse_args(args)
    setup_logging(log_file=args.log_file,
                  log_level=args.log_level)
        
    try:
        config_dir = args.config_dir or default_config_dir()
        # TODO: Merge args and config
        cfg = config.load_config(config_dir)
        
        run_config(backend,
                   make_eventparser,
                   cfg,
                   args)
        
    except SystemExit as e:
        sys.exit(e)
    except:
        import traceback
        logging.error(traceback.format_exc())
        raise



if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_run', failfast=True, exit=False)

