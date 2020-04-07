#!/usr/bin/python
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

from past.builtins import basestring
import string
from pprint import pprint
import subprocess
import os

from collections import defaultdict

import jinja2

class Template(string.Template):
    delimiter = ':'

from hopr.tool import config

# TODO: HACK: Hard coded config dir
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, 'config'))
print(config_dir)

keys = list('qwertyuiopasdfghjklzxcvbnm')
special_keys = 'capslock leftbrace rightbrace semicolon apostrophe backslash comma dot slash leftshift rightshift tab'.split()
unassigned_keys = dict((key, '') for key in keys + special_keys)

empty_layer = {'name': 'EMPTY'}
empty_layer.update(unassigned_keys)


# TODO: Use aliases from config.
latex_symbol = {u'leftctrl': 'C',
         u'rightctrl': 'C',
         u'leftshift': 'S',
         u'rightshift': 'S',
         u'leftalt': 'A',
         u'rightalt': 'AGr',
         u'minus': '-',
         u'comma': ',',
         u'dot': '.',
         # Latex reserved chars
         u'#': r'\#',
         u'$': r'\$',
         u'%': r'\%',
         u'^': r'\^',
         u'&': r'\&',
         u'_': r'\_',
         u'~': r'\~',
         u'<': r'<',
         u'>': r'>',
         u'\\': r'\textbackslash{}',
         # Long names
         u'leftbrace': r'\{',
         u'rightbrace': r'\}',
         u'{': r'\{',
         u'}': r'\}',
         u'slash': r'/',
         u'backslash': r'\textbackslash{}',
         # Movement
         u'left': r'$\leftarrow$',
         u'right': r'$\rightarrow$',
         u'up': r'$\uparrow$',
         u'down': r'$\downarrow$',
         # Word
         u'home': r'$\Leftarrow$',
         u'end': r'$\Rightarrow$',
         u'pageup': r'$\Uparrow$',
         u'pagedown': r'$\Downarrow$',
         u'backspace': r'$\triangleleft$',
         u'bksp': r'$\triangleleft$',
         u'delete': r'$\triangleright$',
         u'del': r'$\triangleright$',
         u'tab': r'$\mapsto$',
         u'enter': r'$\hookleftarrow$',
         u'return': r'$\hookleftarrow$',
         u'ret': r'$\hookleftarrow$',
         # Misc
         u"'": r"\textquotesingle", # r"\texttt{'}", # $'$",
         u'"': r'\textquotedbl', # r"$''$",
         u"`": u'\\`{ }',
        u"´": u"\\'{ }",
        # NOTE: Must match definition exactly! 
        # TODO: HACK: Use aliases to name actions delete-word, delete-line etc. 
        # Very long definitions
        u"ctrl+shift+bksp": r"$\triangleleft\triangleleft\triangleleft$", 
        u"ctrl+shift+del": r"$\triangleright\triangleright\triangleright$", 
        u"ctrl+bksp": r"$\triangleleft\triangleleft$",
        u"ctrl+del": r"$\triangleright\triangleright$",
        u"ctrl+up": r"$\uparrow\uparrow$",
        u"ctrl+down": r"$\downarrow\downarrow$",
        u"ctrl+left": r"$\leftarrow\leftarrow$",
        u"ctrl+right": r"$\rightarrow\rightarrow$",
        }


def latex_key(key):
    key = key.lower()
    if key in latex_symbol:
        return latex_symbol[key]
    else:
        return key

def pretty_key(key):
    # HACK: Handle + in definitions.
    # TODO: Coordinate parsing of layers.

    # HACK: Flatten
    # print(repr(key))
    # key = key[0] + key[1]
    # print(key)
    
    # if key.find('+') > 0:
    #     key = key.split('+')

    if not key:
        return ''
        
    if isinstance(key, basestring):
        return latex_key(key)

    mod, key = key
    key = latex_key(key)
    
    if isinstance(mod, basestring):
        mod = latex_key(mod)
    else:
        mod = ''.join(latex_key(m) for m in mod)

    # print(mod,key)
    return '{mod}+{key}'.format(**locals())

def fix_layers(layers, symbols):
    # HACK: Make layers look like old layers structure.
    x = defaultdict(dict)
    for ((chord_mods, chord_key), key_combo) in list(layers.items()):
        assert len(chord_mods) <= 1 # TODO: Only single key allowed for now
        if chord_mods:
            (chord_mod,) = chord_mods
        else:
            chord_mod = ''

        if key_combo in symbols:
            key_combo = symbols[key_combo]
            
        x[chord_mod.lower()][chord_key.lower()] = key_combo
    return dict(x)
            
        

def get_layer(layers, keys):
    is_mapped = False
    
    layer = unassigned_keys.copy()
    for key in keys:
        if key in layers:
            is_mapped = True
            layer.update(layers[key])

    # pprint(layers)
    # print(keys)
    assert is_mapped

    layer =  dict((key, pretty_key(value)) for key,value in list(layer.items()))
    # pprint(layer)
    return layer

def load_template():
    text = open('kbd.ltx').read()
    template = Template(text)
    template.delimiter = ':'
    return template

def make_layout_python_template(layer):
    template = load_template()
    out = template.substitute(layer)

    name = layer['name']
    fname = 'out/kbd_{name}.ltx'.format(**locals())
    open(fname, 'wb').write(out.encode('latin-1'))
    subprocess.call(['pdflatex', '-output-directory=out', fname])


def make_layout_jinja(output, layers):
    env = jinja2.Environment(
        block_start_string = '<%',
        block_end_string = '%>',
        variable_start_string = '<<',
        variable_end_string = '>>',
        comment_start_string = '<#',
        comment_end_string = '#>',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
        )

    template = env.get_template('kbd.jinja2.ltx')
    latex = template.render(layers=layers)
    open(output, 'wb').write(latex.encode('latin-1'))
    subprocess.call(['pdflatex', '-output-directory=out', output])
    
import yaml
def get_layers(layer_keys):
    params = []

    # TODO: HACK: Hard coded path
    c = yaml.load(open(os.path.join(config_dir, 'keybindings.yaml')))
    layers = c['layers']
    pprint(layers)
    
    # TODO: Symbols are not reversed correctly
    # symbols = dict((v, k) for k,v in c.keyboard_layout.symbols.items())
    # pprint(symbols)
    
    for keys in layer_keys:
        # print(keys)
        # pprint(c.key_bindings.layers)
        # layers = fix_layers(c.key_bindings.layers, symbols) # HACK: TODO: Rewrite

        layer = get_layer(layers, keys)
        
        name = ''.join(keys).upper()
        layer['name'] = name

        # for key in keys:
        #     if not layer[key]:
        #         layer[key] = u'$\otimes$'
                
        params.append(layer)
    return params
        
def run(layers,
        empty,
        output):

    if empty:
        params = [empty_layer]*empty
    else:
        if not layers:
            raise NotImplemented("Todo") # layers = defaultkeybinding.layers.keys()
            
        params = get_layers(layers)

    # HACK: Create missing output dir
    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))
        
    make_layout_jinja(output, params)


def run_parse_args(args):
    from argparse import ArgumentParser
    p = ArgumentParser()
    
    p.add_argument('-l', '--layers',
                   type=lambda x : x.split(','),
                   default=(('space',), 'dk', 'sl'))

    p.add_argument('-a', '--all-layers',
                   dest='layers',
                   action='store_const',
                   const=[])
    
    p.add_argument('-e', '--empty',
                   metavar='N',
                   type=int,
                   default=0,
                   help='Create empty keyboard layouts')
    p.add_argument('-o', '--output', default='out/kbdlayout.ltx')
    

    x = p.parse_args(args)
    run(**vars(x))
        


    
    




if __name__ == "__main__":
    import sys
    # run_parse_args("-e 6".split())
    run_parse_args(sys.argv[1:])
