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


# TODO: Reconsider
from eventparser import EventParser
from keymap import KeyMap

def make_eventparser(cfg, output_kbd):

    key_map = keymap.KeyMap(modifiers=cfg.key_bindings.modifiers,
                            chords=cfg.key_bindings.layers)

    p = eventparser.EventParser(key_map=key_map,
                                kbd=output_kbd,
                                on_off_key=cfg.key_bindings.on_off,
                                passthrough_keys=cfg.key_bindings.passthrough,
                                send_unknown_chord=cfg.app.send_unknown_chord,
                                )

    return p
