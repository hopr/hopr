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



PRESS = 'PRESS'
RELEASE = 'RELEASE'
HOLD = 'HOLD'

actions = {'P': PRESS,
           'R': RELEASE,
           'H': HOLD,
           }


class Event(object):
    def __init__(self, ev=None, action=None, key=None):
        """
        pa => key=A action=Press
        ra => key=A action=Release
        ha => key=A action=Hold NOT IN USE
        pany = key=ANY action=Press
        """
        if ev:
            ev = ev.upper()
            action = actions[ev[0]]
            key = ev[1:]

        self.key = key
        self.action = action

    def is_press(self):
        return self.action == PRESS

    def is_release(self):
        return self.action == RELEASE


    def __str__(self):
        return '{} {}'.format(self.action, self.key)

    def __repr__(self):
        return 'Event(action={!r}, key={!r})'.format(self.action, self.key)




def parse_events(s):
    events = [Event(e) for e in s.split()]
    return events


def is_iterable(x):
    if isinstance(x, basestring):
        return False
    
    try:
        iter(x)
        return True
    except ValueError:
        return False


def key_index(modifiers, key):
    return (tuple(sorted(m.upper() for m in modifiers)), key.upper())


def pretty_key(mods, key):
    if isinstance(key, basestring):
        return chord_index((), key)

    (modifiers, key) = key
    if is_iterable(modifiers):
        modifiers = tuple(modifiers)
    else:
        modifiers = (modifiers,)
        
    return key_index(modifiers, key)




if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_mockevent', failfast=True, exit=False)

