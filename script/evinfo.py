#! /usr/bin/python
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

import re
from pprint import pprint

import evdev as ed

from hopr.backend.evdev import read_events

def match_any(name, patterns):
    if not patterns:
        return True

    for pattern in patterns:
        if re.search(pattern, name):
            return True

    return False

def find_devices(include):
    devices = set()
    for fn in ed.list_devices():
        dev = ed.InputDevice(fn)

        if not include:
            devices.add(dev)
        else:
            for match in include:
                (key, pattern) = match.split('=')
                text = str(getattr(dev, key))
                if re.search(pattern, text, re.I):                
                    devices.add(dev)
                
    return sorted(devices, key=lambda dev : dev.fn)


def capabilities(include):
    for dev in find_devices(include):
        print('{dev.fn} {dev.name}'.format(dev=dev))
        pprint(dev.capabilities(True))

def format_event(ev):
    return str(ed.categorize(ev))

def read(include):
    for dev,ev in read_events(find_devices(include), return_device=True):
        print('{} {}'.format(dev.fn, format_event(ev)))


def list_devices(include, property):
    for dev in find_devices(include):
        line = ' '.join(['{}={}'.format(key, getattr(dev, key)) for key in property])
        print(line)

def list_vars(include):
    for dev in find_devices(include):
        print(dev)
        pprint([x for x in dir(dev) if not x.startswith('_')])

def run(cmd, **kwargs):
    f = globals()[cmd]
    f(**kwargs)


def run_parse_args(args):
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-i', '--include', action='append', help='Example: evinfo.py -i name=keyboard -i "fn=.*event1?"')
    
    sp = p.add_subparsers(dest='cmd')
    q = sp.add_parser('list_devices')
    q.add_argument('-p', '--property', action='append', default='fn name info phys'.split())
    q = sp.add_parser('list_vars')
    q = sp.add_parser('capabilities')
    q = sp.add_parser('read')
    x = p.parse_args(args)
    # pprint(vars(x))
    run(**vars(x))
    

if __name__ == "__main__":
    import sys
    run_parse_args(sys.argv[1:])

