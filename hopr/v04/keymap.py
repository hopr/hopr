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

# -*- coding: utf-8 -*-

# TODO: Rename. KeyMap vs key_map.
class KeyMap(object):
    def __init__(self,
                 modifiers,
                 chords):
        self.chords = chords
        self.modifiers = modifiers

    def __call__(self, pressed_keys, released_index):
        # TODO: Better handling of case insensitivity. Review and make sure case is handled at loading.
        
        pressed_mods = sorted(pressed_keys[0:released_index])
        pressed_key = pressed_keys[released_index]
        
        # Get mapped modifiers
        modifiers = tuple(self.modifiers[key] for key in pressed_mods if key in self.modifiers)
        # Flatten modifiers list
        modifiers = tuple(mod for mods in modifiers for mod in mods)
        

        # Mapped modifiers are excluded from chord modifiers. 
        chord_mods = tuple(key for key in pressed_mods if key not in self.modifiers)

        if (chord_mods, pressed_key) in self.chords:
            # NOTE: Registered key mappings overrides plain key presses
            # TODO: Naming conventions. Map from (mod, key) to (mod, key)
            mapped_keys = self.chords[(chord_mods, pressed_key)]
            if not mapped_keys:
                return ()
            
            (mapped_mods, mapped_key) = mapped_keys
            return (modifiers + mapped_mods, mapped_key)
        elif not chord_mods:
            # Plain key press. Return pressed modifiers and key
            return (modifiers, pressed_key)
        else:
            # Unregistered chord. Default to ignoring
            # TODO: Default handling
            return ()



if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_keymap', failfast=True, exit=False)

