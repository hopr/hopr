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
from builtins import object
from evdev import UInput, ecodes as e
import logging

from . import etype
from .keycode import keycode

def to_str(ui):
    # NOTE: Some kind of error with str when using Ubuntu 16.04. ui not open when using ui.capabilities
    return '{ui.name}({ui.devnode})'.format(ui=ui)

class KbdOutput(object):

    def __init__(self):
        self.ui = UInput()
        logging.info('Creating uinput device: ' + to_str(self.ui))

    def __enter__(self):
        return self
        
    def press(self, key):
        self.ui.write(e.EV_KEY, keycode(key), etype.KEY_PRESS)

    def release(self, key):
        self.ui.write(e.EV_KEY, keycode(key), etype.KEY_RELEASE)

    def sync(self):
        self.ui.syn()

    def close(self):
        self.ui.close()

    def __exit__(self, exc_type, exc_value, traceback):
        logging.info('Closing uinput device: ' + to_str(self.ui))
        self.close()

make_virtual_kbd = KbdOutput

if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_kbdoutput', failfast=True, exit=False)








