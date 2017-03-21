#!/bin/bash
# TODO: Way too permissive. Only add permissions for physical keyboards.
# TODO: Replace with something better...
chmod +0006 /dev/input/event*
chmod +0006 /dev/uinput


