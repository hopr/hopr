#!/usr/bin/python
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

# TODO: Reconsider safe construction/destruction kbd output and grabbing/ungrabbing of kbd input. OS independence. 
# TODO: Clean up!

import logging
# TODO: Strange. Log level is set to warning when I add logging statements in backend.evdev.kbdoutput.

import os, sys
# TODO: HACK: base_dir depends on location of current file.
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
out_dir = os.path.join(base_dir, 'out')
config_dir = os.path.join(base_dir, 'config')

import os
if not os.path.exists(out_dir):
    os.mkdir(out_dir)


logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(out_dir, 'hopr.log'),
                    format='%(asctime)s %(message)s')

log = logging.getLogger()
log.addHandler(logging.StreamHandler())


from functools import partial

from hopr.tool import config
from hopr.backend import evdev


# TODO: Rename run.py to something more descriptive
from hopr.tool.run import Run
from hopr.v04 import eventparser, keymap


from pprint import pprint
import signal

signal_name = dict((v,k) for k,v in vars(signal).items() if k.startswith('SIG'))

def exit_on_signal(sig, frame):
    msg = 'Caught signal {}={}. Exiting...'.format(signal_name[sig], sig)
    if sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGTSTP):
        log.info(msg)
        sys.exit(0) # NOTE: Raises SystemExit
    else:
        raise RuntimeError(msg)

def register_signal_handlers():
    # NOTE: Application exits on C-z
    
    # Handle signals: Hangup, terminate, suspend (terminal stop)
    # SIGTERM: Ask for termination. Can be blocked
    # SIGINT: Interrupt C-c.
    # SIGTSTP: Suspend C-z.
    # SIGHUP: Hangup. Terminal disconnected.
    # SIGQUIT: User detected error. Create core dump. TODO:

    # Unblockable and unhandled:
    # SIGSTOP: Stops process.
    # SIGKILL: Unblockable kill

    for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGTSTP, signal.SIGQUIT, signal.SIGINT):
        signal.signal(sig, exit_on_signal)

def send_event(kbd, e):
    if e.is_press():
        kbd.press(e.key)
    elif e.is_release():
        kbd.release(e.key)
    else:
        raise ValueError("Unexpected event: " + str(e))


def setup_parser(kbd_out, cfg):
    key_map = keymap.KeyMap(modifiers=cfg.key_bindings.modifiers,
                            chords=cfg.key_bindings.layers)

    p = eventparser.EventParser(key_map=key_map,
                                kbd=kbd_out,
                                on_off_key=cfg.key_bindings.on_off,
                                passthrough_keys=cfg.key_bindings.passthrough)

    return p


def is_press_or_release(ev):
    return evdev.is_press(ev) or evdev.is_release(ev)


def run(args):
    register_signal_handlers()

    cfg = config.load_config(config_dir)
    
    with evdev.make_virtual_kbd() as kbdout:
        parser = setup_parser(kbdout, cfg)
        # TODO: No help text if no rw permissions on uinput and evdev. uinput and evdev are created/grabbed before arguments are parsed. 
        runner = Run(parser=parser,
                     event_wrapper=evdev.Event,
                     # NOTE: Filter only press/release events (ignore hold for now)
                     read_events=partial(evdev.read_events, event_filter=is_press_or_release),
                     grab_keyboards=evdev.grab,
                     find_keyboards=evdev.find_keyboards,
                     )
        runner.run_parse_args(args)


def main():
    import sys
    try:
        run(sys.argv[1:])
    except SystemExit as e:
        sys.exit(e)
    except:
        import traceback
        log.error(traceback.format_exc())
        raise
    

if __name__ == "__main__":
    main()
    
