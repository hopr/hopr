#!/bin/bash
# TODO: Way too permissive. Gives rw permissions to EVERYONE and every event.
# TODO: Replace with something better...
chmod +0006 /dev/input/event*
chmod +0006 /dev/uinput


