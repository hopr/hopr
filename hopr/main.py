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
# TODO: Strange. Log level is set to warning when I add logging statements in linux.backend.evdev.kbdoutput.

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

from tool import config
import backend.linuxevdev as backend

# TODO: Rename run.py to something more descriptive
from tool.run import Run
from v04 import eventparser, keymap

from pprint import pprint

def setup_parser(kbd_out, cfg):
    key_map = keymap.KeyMap(modifiers=cfg.key_bindings.modifiers,
                            chords=cfg.key_bindings.layers)

    p = eventparser.EventParser(key_map=key_map,
                                kbd=kbd_out,
                                on_off_key=cfg.key_bindings.on_off,
                                passthrough_keys=cfg.key_bindings.passthrough,
                                send_unknown_chord=cfg.app.send_unknown_chord,
                                )

    return p


def is_press_or_release(ev):
    return backend.is_press(ev) or backend.is_release(ev)


def run(args):
    backend.register_signal_handlers()

    cfg = config.load_config(config_dir)
    
    with backend.make_virtual_kbd() as kbdout:
        parser = setup_parser(kbdout, cfg)
        runner = Run(parser=parser,
                     event_wrapper=backend.Event,
                     # NOTE: Filter only press/release events (ignore hold for now)
                     read_events=partial(backend.read_events, event_filter=is_press_or_release),
                     grab_keyboards=backend.grab,
                     find_keyboards=backend.find_keyboards,
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
    
