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

class EventParser(object):
    """
    Parses keyboard events and detects chord shortcuts.
    
    Maintains a list of pressed keys.
    
    Calls key_map(pressed_keys, i) when the i:th key is released.

    Merges repeated maps of the same modifiers. Repeated Alt+Tab -> Alt + repetead Tabs
    """
    
    def __init__(self,
                 key_map,
                 kbd,
                 on_off_key,
                 passthrough_keys,
                 ):
        
        self.key_map = key_map
        self.kbd = kbd
        self.on_off_key = on_off_key
        self.passthrough_keys = set(passthrough_keys)
        
        self.is_on = True        
        self.reset()

    def send(self, event):
        if event.is_press():
            self.press(event.key)
        elif event.is_release():
            self.release(event.key)
        else:
            raise ValueError('Unexpected event type:' + str(event))

    def press(self, key):
        self.kbd.press(key)
        self.synced = False

    def release(self, key):
        self.kbd.release(key)
        self.synced = False


    def _update_modifiers(self, current_modifiers=()):
        """
        Releases modifiers which are no longer pressed and press new modifiers.

        Update list of pressed modifiers.
        """
        last = self.last_modifiers
        current = current_modifiers

        for mod in sorted(last - current):
            self.release(mod)

        for mod in sorted(current - last):
            self.press(mod)

        if last != current:
            self.last_modifiers = current
            self.synced = False
        

    def sync(self):
        if not self.synced:
            self.kbd.sync()
            self.synced = True

    def _release_key(self, i):
        """
        Handle release of the i:th key.
        """
        mapped = self.key_map(self.pressed_keys, i)
        logging.debug('Sending: ' + str(mapped))

        if mapped:
            (mods, key) = mapped
        else:
            (mods, key) = ((), None)

        mods = set(mods)
        if mods != self.last_modifiers:
            # If modifiers have changed since last key press:
            #       release old and press new
            self._update_modifiers(mods)

        if key is not None:
            self.press(key)
            self.release(key)
        else:
            logging.warning('Unmapped chord: ' + str(self.pressed_keys[:i+1]))

    def reset_key_event_counters(self):
        self.pressed_keys = []
        self.last_released_idx = 0
        self.last_modifiers = set()

    def reset(self):
        # NOTE: is_on is not reset
        self.reset_key_event_counters()
        self.synced = True
        self.passthrough_key_is_pressed = False

    def __call__(self, event):
        
        logging.debug("EventParser: event=" + str(event))
        
        # On/Off mode
        if event.key == self.on_off_key:
            if event.is_press():
                self.reset()
                self.is_on = not self.is_on
                state = 'ON' if self.is_on else 'OFF'
                logging.info('Chording is ' + state)
            return

        if not self.is_on:
            self.send(event)
            self.sync()
            return


        # Passthrough keys
        if event.key in self.passthrough_keys:
            if event.is_press():
                self.passthrough_key_is_pressed = True
                # Send pressed keys and clear queue
                for key in self.pressed_keys:
                    self.press(key)
                self.reset_key_event_counters()
                self.sync()
            elif event.is_release():
                self.passthrough_key_is_pressed = False
                # Prevent unneccesary key release warning
                self.send(event)
                self.sync()
                return

        if self.passthrough_key_is_pressed:
            self.send(event)
            self.sync()
            return

        # Chord parsing
        if event.is_press():
            self.pressed_keys.append(event.key)
        elif event.is_release():
            try:
                i = self.pressed_keys.index(event.key)
            except ValueError:
                # Unexpected key release
                logging.warning('Unexpected key release: ' + str(event))
                self.release(event.key)
                self.sync()
                return

            if i < self.last_released_idx:
                # Released key was part of a chord modifier.                    
                self.last_released_idx -= 1
            else:
                self._release_key(i)
                self.last_released_idx = i

            del self.pressed_keys[i]

            if self.last_released_idx == 0:
                # Last chord mofifier was released. Send all held modifier events.
                self._update_modifiers(set())

            self.sync()
        else:
            raise ValueError('Unexpected event type: ' + str(event))




if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_eventparser', failfast=True, exit=False)

