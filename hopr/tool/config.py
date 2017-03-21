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
import os
import yaml
from pprint import pprint
from collections import namedtuple
        

# TODO: Mapping errors are not caught. Improve chord and key definitions.
# TODO: Can not use symbols with modified key defs. I.e. meta+%
# def parse_layers(layers, symbols, alias):
def parse_layers(layers, symbols, key_names):
    """
    Return a key chord map.
    The map is a dictionary from a key chord ((mods), key) to a key combination ((mods), key)
    """
    key_map = {}
    for (chord_mod, layer) in layers.items():

        if chord_mod:
            chord_mod = parse_key_combo(chord_mod, key_names)
        else:
            chord_mod = ()
            
        for (chord_key, key_combo) in layer.items():
            chord_key = parse_key(chord_key, key_names)

            # TODO: Symbols can only be used in layer definitions. Fix
            # TODO: Symbols can not be used with modifiers (Alt+%). Fix
            if key_combo in symbols:
                key_combo = symbols[key_combo]

            # Ignore empty definitions
            if key_combo:
                key_combo = parse_key_combo(key_combo, key_names)
                key_combo = (tuple(key_combo[:-1]), key_combo[-1])
                key_map[(chord_mod, chord_key)] = key_combo

    return key_map



def parse_modifiers(modifiers):
    # Make sure all is uppercased
    # TODO: Use only upper or lower case everywhere...
    return dict((k.upper(), v.upper()) for (k,v) in modifiers.items() if v.strip())

def unalias(key, aliases):
    if key in aliases:
        return aliases[key]
    else:
        return key

def format_kwargs(kwargs):
    pass

class ParseError(Exception):
    def __init__(self, msg, **kwargs):
        self.message = unicode(msg)
        
        self.info = []
        self.add_info(**kwargs)

    def add_info(self, **kwargs):
        self.info += [u'{}={}'.format(k,v) for k,v in sorted(kwargs.items())]

    def __str__(self):
        return self.message + u'\n' + u'\n'.join(self.info)

    

def assert_key_name(key, names):
    if key not in names:
        raise ParseError('Error in config. Unknown key: ' + repr(key))
    
def assert_(predicate, *args, **kwargs):
    if not predicate:
        params = [str(a) for a in args] + ['{}={}'.format(k,v) for k,v in kwargs.items()]
        msg = '\n'.join(params)
        raise ValueError(msg)


def parse_key(key, key_names):
    assert_(isinstance(key, basestring), unexpected_key=key)
    key = unalias(key.upper(), key_names.aliases)
    assert_key_name(key, key_names.names)
    return key

def parse_key_combo(key_combo, key_names, info={}):
    """ Accept both ('a', 'b') notation and 'a+b' """
    
    if isinstance(key_combo, basestring):
        key_combo = key_combo.split('+')

    try:
        key_combo = tuple(parse_key(key, key_names) for key in key_combo)
    except ParseError as e:
        e.add_info(key_combo=key_combo)
        e.add_info(**info)
        raise e
    
    return key_combo

def parse_passthrough(keys, key_names):
    return set(parse_key(k, key_names) for k in keys)

def parse_key_dict(dictionary, key_names):
    # Parse dictionary with key -> key combo items 
    return dict((parse_key(k, key_names), parse_key_combo(v, key_names)) for k,v in dictionary.items())


KeyBindings = namedtuple('KeyBindings', 'layers on_off passthrough modifiers'.lower().split())
def load_key_bindings(path, symbols, key_names):
    x = yaml.load(open(path, 'rb'))
    return KeyBindings(on_off=parse_key(x['on_off'], key_names),
                       passthrough=parse_passthrough(x['passthrough'], key_names),
                       modifiers=parse_key_dict(x['modifiers'], key_names),
                       layers=parse_layers(x['layers'], symbols=symbols, key_names=key_names))
                       


KeyNames = namedtuple('KeyNames', 'names aliases'.split())
def load_key_names(path):
    # HACK: TODO: Reconsider setup and configuration. Should probably parse key combos and replacing aliases when loading configs.
    aliases = yaml.load(open(path, 'rb').read().upper())['ALIAS']
    
    # HACK: For now, use evdev names without KEY_
    import evdev
    names = [x.upper()[4:] for x in evdev.ecodes.ecodes if x.startswith('KEY_')]
    
    return KeyNames(names=set(names), aliases=aliases)


KeyboardLayout = namedtuple('KeyboardLayout', 'symbols'.lower().split())
def load_keyboard_layout(path, key_names):
    try:
        x = yaml.load(open(path, 'rb'))
        symbols = dict((k, parse_key_combo(v, key_names, info=dict(symbol=k))) for (k,v) in x['symbols'].items())
    except ParseError as e:
        e.add_info(path=path)
        raise e
    
    return KeyboardLayout(symbols=symbols)    


Config = namedtuple('Config', 'key_names keyboard_layout key_bindings'.lower().split())
def load_config(config_dir,
                key_names_path=None,
                keyboard_layout_path=None,
                key_bindings_path=None):

    key_names_path = os.path.join(config_dir, key_names_path or 'keynames.yaml')
    keyboard_layout_path = os.path.join(config_dir, keyboard_layout_path or 'layout/se.yaml')
    key_bindings_path = os.path.join(config_dir, key_bindings_path or 'keybindings.yaml')

    key_names = load_key_names(key_names_path)
    keyboard_layout = load_keyboard_layout(keyboard_layout_path, key_names)
    key_bindings = load_key_bindings(key_bindings_path, keyboard_layout.symbols, key_names)

    return Config(key_names=key_names,
                  keyboard_layout=keyboard_layout,
                  key_bindings=key_bindings)

    

if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_config', failfast=True, exit=False)

