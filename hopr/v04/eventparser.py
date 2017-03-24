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

class VirtualKeyboard(object):
    def __init__(self, device):
        self.device = device
        self.reset()

    def reset(self):
        self.press_count = 0
        self.release_count = 0
        self.synced = True
        self.pressed_modifiers = set()

    def set_modifiers(self, current):
        """
        Releases modifiers which are no longer pressed and press new modifiers.
        Update list of pressed modifiers.
        """
        current = set(current)
        
        last = self.pressed_modifiers        
        for mod in sorted(last - current):
            self.release(mod)

        for mod in sorted(current - last):
            self.press(mod)

        if last != current:
            self.pressed_modifiers = current
            self.synced = False


    def send(self, event):
        if event.is_press():
            self.press(event.key)
        elif event.is_release():
            self.release(event.key)
        else:
            raise ValueError('Unexpected event type:' + str(event))

    def press(self, key):
        self.press_count += 1
        self.device.press(key)
        self.synced = False

    def release(self, key):
        self.release_count += 1
        self.device.release(key)
        self.synced = False        

    def sync(self):
        if not self.synced:
            self.device.sync()
            self.synced = True




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
                 send_unknown_chord=True,
                 ):
        
        self.key_map = key_map
        self.kbd = VirtualKeyboard(kbd)
        self.on_off_key = on_off_key
        self.passthrough_keys = set(passthrough_keys)
        self.send_unknown_chord = send_unknown_chord
        
        self.is_on = True        
        self.reset()

    # Only used from init and on_off
    def reset(self):
        # NOTE: is_on must not be reset.
        self.kbd.reset()

        # pressed_keys: Keeps track of the press key events which have not yet been sent. 
        self.pressed_keys = []
        # cmods_idx: keeps track of the index of the last released key.
        #     It is used to detect when a chord modifier is released.
        #     All pressed keys with i < cmods_idx are chord modifiers.
        #     Pressed keys with i > cmod_idx are not yet classified
        self.cmods_idx = 0


    def _send_key_events(self, i):
        """
        Handle release of the i:th key.        
        """
        mapped = self.key_map(self.pressed_keys, i)
        logging.debug('Sending: ' + str(mapped))

        if mapped:
            (mods, key) = mapped
        else:
            (mods, key) = ((), None)

        # Handle changes in output modifer keys
        self.kbd.set_modifiers(mods)

        if key is not None:
            self.kbd.press(key)
            self.kbd.release(key)
            del self.pressed_keys[i]
            self.cmods_idx = i
        else:
            logging.info('Unknown chord: ' + str(self.pressed_keys[:i+1]))
            if self.send_unknown_chord:
                key = self.pressed_keys[i]
                # NOTE: Empties the pressed_keys queue
                self._send_all_pressed_keys()
                self.kbd.release(key)
            else:                
                # Unrecognized chord is silently ignored. No events are sent.
                del self.pressed_keys[i]
                self.cmods_idx = i

    def _send_all_pressed_keys(self):
        for key in self.pressed_keys:
            self.kbd.press(key)

        self.pressed_keys = []
        self.cmods_idx = 0
        self.kbd.sync()
        

    def handle_on_off(self, event):
        if event.key == self.on_off_key:
            if event.is_press():
                self.reset()
                self.is_on = not self.is_on
                state = 'ON' if self.is_on else 'OFF'
                logging.info('Chording is ' + state)
            return True
        else:
            return False

    def handle_passthrough_keys(self, event):
        """
        Passthrough keys events are sent immediately without further processing. 
        All press key events are sent to preserve event order as much as possible.
        Used for scenario 'press shift press a release shift release a'
        """
        if event.key in self.passthrough_keys:
            self._send_all_pressed_keys()
            self.kbd.send(event)
            self.kbd.sync()
            return True
        else:
            return False


    def __call__(self, event):
        logging.debug("EventParser: event=" + str(event))
        
        if self.handle_on_off(event):
            return
        
        if not self.is_on:
            # Chording is turned off. Send events without parsing.
            self.kbd.send(event)
            self.kbd.sync()
            return

        if self.handle_passthrough_keys(event):
            return

        # Chord parsing
        if event.is_press():
            self.pressed_keys.append(event.key)
        elif event.is_release():
            try:
                i = self.pressed_keys.index(event.key)
            except ValueError:
                # HACK: Both passthrough keys and unrecognized chords empty the pressed_keys queue. Check counters to verify there have been more press events than release events
                if self.kbd.press_count <= self.kbd.release_count:
                    # Unexpected key release
                    logging.warning('Unexpected key release: ' + str(event))
                    
                self.kbd.release(event.key)
                self.kbd.sync()
                return

            if i < self.cmods_idx:
                # Released key was part of a chord modifier. Do not send release event. 
                self.cmods_idx -= 1
                del self.pressed_keys[i]
            else:
                # Released key was a chord key or a regular key
                self._send_key_events(i)

            if self.cmods_idx == 0:
                # Last chord modifier was released. Send release events for all held modifier events.
                self.kbd.set_modifiers(current=())

            self.kbd.sync()
        else:
            raise ValueError('Unexpected event type: ' + str(event))




if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_eventparser', failfast=True, exit=False)

