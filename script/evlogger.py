#! /usr/bin/python
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

import csv
import sys

from pickle import dump, load
from collections import defaultdict
from evdev import ecodes as e

from hopr.backend.linuxevdev import find_keyboards, read_events, etype
from time import time
import os
import logging

from pprint import pprint, pformat

# TODO: Measure time spent pressing any particular key. How much time is spent pressing ctrl vs shift?
# TODO: General timing info. How much time is spent typing?

class SaveFile(object):
    def __init__(self, filename):
        self.filename = filename

    @property
    def temp_filename(self):
        return self.filename + '.tmp'
    
    def __enter__(self):
        self.file = open(self.temp_filename, 'wb')
        return self

    def __exit__(self, exc, exc_type, exc_tb):
        os.fsync(self.file.fileno())
        self.file.close()
        # Rename temp file to filename
        os.rename(self.temp_filename, self.filename)        
        

def key_name(code):
    if code is None:
        return 'NONE'
    else:
        name = e.keys[code]
        if not isinstance(name, basestring):
            name = name[0]
            
        return name.replace('KEY_', '')


def key_code(name):
    if name == 'NONE':
        return None
    else:
        return e.ecodes['KEY_' + name]


def append(history, code):
    history[:-1] = history[1:]
    history[-1] = code

def tuplify(x):
    if isinstance(x, tuple):
        return x
    else:
        return (x,)


def save_ngrams(filename, ngrams):
    n_ngrams = len(ngrams)
    n_event = sum([n for _,n in list(ngrams.items())])
    logging.info('Saving: {filename} n-grams: {n_ngrams} event_count: {n_event}'.format(**locals()))
    
    key_header = None
    with SaveFile(filename) as f:
        w = csv.writer(f.file)
        for (keys, values) in list(ngrams.items()):
            keys = tuplify(keys)
            values = tuplify(values)

            if not key_header:
                key_header = ['key{}'.format(i+1) for i in range(len(keys))]
                value_header = ['value']
                w.writerow(key_header + value_header)
                
            w.writerow(keys + values)


def save_csv(filename, log):
    for (tag, sublog) in list(log.items()):
        save_ngrams(filename + '.' + tag, sublog)

def empty_sublog():
    return defaultdict(int)

def empty_log():
    return defaultdict(empty_sublog)

def load_ngrams(filename):
    ngrams = empty_sublog()
    
    reader = csv.reader(open(filename, 'rb'))
    header = next(reader)
    assert header[-1] == 'value'
    
    n = len(header) - 1
    for row in reader:
        key = tuple(int(code) for code in row[:-1])
        n = int(row[-1])
        ngrams[key] = n
    return ngrams

# def load_csv(filename):
#     log = empty_log()
#     for fname in glob(filename + '.*'):
#         tag = fname.replace('filename.', '')
#         sublog = load_ngrams(fname)
        

def load_pickle(filename):
    return load(open(filename, 'rb'))


        
def save_pickle(filename, log):
    logging.info('Saving log: {}'.format(dict((key, len(value)) for key,value in list(log.items()))))
    with SaveFile(filename) as f:
        dump(log, f.file, protocol=2)


# def save_csv(filename, log):
#     save_ngrams(filename + '.bigrams', log['event'])
#     save_ngrams(filename + '.events', log['press2'])

load_log = load_pickle

def save_log(filename, log):
    save_pickle(filename, log)
    save_csv(filename, log)


def start(filename, save_interval):
    " Log statistics for all keyboard events "

    if os.path.exists(filename):
        log = load_log(filename)
    else:
        log = empty_log()
        
    press = [None]*2

    last_save = 0
    try:
        for ev in read_events(find_keyboards()):
            if time() - last_save > save_interval:
                save_log(filename, log)
                last_save = time()

            if ev.type == e.EV_KEY:
                logging.debug('{}'.format(ev))
                log[etype.name(ev.value)][key_name(ev.code)] += 1

                if ev.value == etype.KEY_PRESS:
                    append(press, key_name(ev.code))
                    log['PRESS2'][tuple(press)] += 1
                
    except KeyboardInterrupt as SystemExit:
        logging.info('Quitting. Saving log')
        save_log(filename, log)
    except Exception as exc:
        logging.error('Unexpected exception' + str(exc))
        raise




def view(filename):
    x = load_log(filename)

    events = {}
    for ((code, value), count) in list(x['event'].items()):
        key = '{}={}'.format(key_name(code), value)
        events[key] = count

    print('Key Count')
    pprint(events)

    press = {}    
    for ((code1, code2), count) in list(x['press2'].items()):
        key = '{},{}'.format(key_name(code1), key_name(code2))
        press[key] = count

    print('Paired event count')
    pprint(press)

# def print_pairs(filename):
#     x = load_log(filename)
#     pairs = x['press2']

#     codes = sorted(set([c for pair in pairs for c in pair]))
#     code2idx = dict((c,idx) for (idx, c) in enumerate(codes))

#     N = len(codes)
#     count = [[0]*N for _ in range(N)]
    
#     for ((code1, code2), n) in x['press2'].items():
#         count[code2idx[code1]][code2idx[code2]] += n

#     codes = [key_name(code) for code in codes]
#     w = csv.writer(sys.stdout)
#     w.writerow([''] + codes)
#     for code, row in zip(codes, count):
#         w.writerow([code] + row)
    


def summary(filename, top):
    x = load_log(filename)

    press = []
    hold = []
    for ((code, value), count) in list(x['event'].items()):
        if value == etype.KEY_PRESS:
            press.append((count, key_name(code)))
        elif value == etype.KEY_HOLD:
            hold.append((count, key_name(code)))
            

    print('Key Press')
    pprint(sorted(press, reverse=True)[:top])
    print('Key Hold')
    pprint(sorted(hold, reverse=True)[:top])

    press2 = []
    for ((code1, code2), count) in list(x['press2'].items()):
        # TODO: Option. Ignore repeated key presses.
        if code1 != code2:
            key = '{},{}'.format(key_name(code1), key_name(code2))
            press2.append((count, key))

    print('Paired event count')
    pprint(sorted(press2, reverse=True)[:top])

        
def run(cmd, verbose, **kwargs):
    if verbose:
        logging.getLogger().setLevel(level=logging.DEBUG)

    logging.debug('Running {} with args {}'.format(cmd, pformat(kwargs)))
        
    f = globals()[cmd]
    f(**kwargs)
    
def run_parse_args(args):    
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-v', '--verbose', action='store_true')

    sp = p.add_subparsers(dest='cmd')

    q = sp.add_parser('start')
    q.add_argument('-i', '--save_interval', default=60.0, type=float)
    # TODO: Global file name arg.
    q.add_argument('filename', nargs='?', default='out/evlogger.log')

    q = sp.add_parser('view')
    q.add_argument('filename', nargs='?', default='out/evlogger.log')

    q = sp.add_parser('summary')
    q.add_argument('filename', nargs='?', default='out/evlogger.log')
    q.add_argument('-t', '--top', default=15, type=int)

    # q = sp.add_parser('print_pairs')
    # q.add_argument('filename', nargs='?', default='out/evlogger.log')
    
    x = p.parse_args(args)
    logging.debug('parse args: {}'.format(x))
    run(**vars(x))


if __name__ == "__main__":
    import sys
    run_parse_args(sys.argv[1:])
    # run_parse_args('-v print_pairs'.split())
    

