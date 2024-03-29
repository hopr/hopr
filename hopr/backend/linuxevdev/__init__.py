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
from hopr.backend.linuxevdev.event import Event
from hopr.backend.linuxevdev.etype import is_press, is_release
# TODO: Rename to devices?
from hopr.backend.linuxevdev.kbdinput import find_keyboards, grab, read_events
from hopr.backend.linuxevdev.kbdoutput import make_virtual_kbd
from hopr.backend.linuxevdev.signalhandlers import register_signal_handlers
