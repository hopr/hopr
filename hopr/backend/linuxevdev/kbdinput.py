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


import logging
from select import select
from evdev import list_devices, ecodes as e, InputDevice

class GrabDevices(object):
    """
    Device grabbing object. Use with 'with' statement.
    Grabs on enter, releases on exit
    """
    
    def __init__(self, devices):
        self.devices = devices
    
    def __enter__(self):
        for dev in self.devices:
            logging.info('Grabbing device {}'.format(dev))
            dev.grab()

    def __exit__(self, exc_type, exc_val, exc_tb):
        for dev in self.devices:
            logging.info('Ungrabbing device {}'.format(dev))
            dev.ungrab()

grab = GrabDevices

def is_physical_keyboard(dev):
    
    if not dev.phys:
        # Only physical devices
        # NOTE: In Ubuntu 18.04, py-evdev-uinput registers as a physical device. Insufficient.
        return False
    
    # TODO: Improve handling. How to distinguish physical keyboard from uinput safely?
    if dev.name.find('uinput') >= 0:
        return False

    # Does the device have key events?
    c = dev.capabilities()
    if e.EV_KEY not in c:
        return False

    # Does the device have A-Z key events? (Not just numeric keyboard)
    # TODO: Perhaps grab numerical keypad as well (?) to allow key pad chords.
    keys = c[e.EV_KEY]
    if (e.KEY_A not in keys
        or e.KEY_Z not in keys):
        return False
    
    return True


def find_keyboards():
    # TODO: Make sure uinput device is NOT returned. Should perhaps device so it can be excluded. Or, create/list devices at the same time.
    keyboards = []
    for fn in list_devices():
        dev = InputDevice(fn)
        if is_physical_keyboard(dev):
            keyboards.append(dev)
    return keyboards


def read_events(devices,
                event_filter=lambda ev : True,
                return_device=False):
    """
    Reads events from the devices and returns them (yields)

    return_device: Return a (device, event) pair instead of a single the event.
    """
    
    if not devices:
        raise ValueError('Can not read device events: No devices')
    
    devices = {dev.fd: dev for dev in devices}
    try:
        while True:
            # NOTE: Blocks until there is a read ready device. Returns devices ready for reading.
            # TODO: Why is select necessary? Can't remember... Is there a timeout until keyboards are readable?
            r,w,x = select(devices, [], [])
            for fd in r:
                for event in devices[fd].read():
                    # NOTE: If an exception occurs below, the event is never sent. Keys may get stuck.
                    if event_filter(event):
                        if not return_device:                        
                            yield event
                        else:
                            yield (devices[fd], event)
                        
    except KeyboardInterrupt:
        for dev in devices.values():
            dev.close()
        raise
            

if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_kbdinput', failfast=True, exit=False)

