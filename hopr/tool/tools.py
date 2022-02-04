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


import yaml
from pprint import pprint
from collections import namedtuple
    
def pretty_key(key):
    """ Helper function to create key combinations in tests """
    
    if not key:
        return None

    # TODO: REVIEW: is all this type checking necessary?
    if isinstance(key, str):
        mods = ()
        key = key
    else:
        try:
            (mods, key) = key
        except:
            raise ValueError('Unexpected key definition: ' + repr(key))

    if isinstance(mods, str):
        mods = (mods,)

    mods = tuple(sorted(m.upper() for m in mods))
    return (mods, key.upper())



if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_tools', failfast=True, exit=False)

