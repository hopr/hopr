#!/usr/bin/env python3
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

import os

import hopr.backend.linuxevdev as backend
from hopr.tool.run import run_parse_args
from hopr.v04 import make_eventparser

def main():
    import sys
    run_parse_args(backend=backend,
                   args=sys.argv[1:],
                   make_eventparser=make_eventparser
                   )    

if __name__ == "__main__":
    main()
    
