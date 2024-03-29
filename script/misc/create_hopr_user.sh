# Create a hopr user with permissions on /dev/uinput and /dev/input/event*
# Run hopper with this user instead of your own login if you don't want to your own user to have read/write rights on all devices.

# NOTE: For some reason, you it doesn't work if you change the group on uinput using chown. You must use a rule in udev.

# Create a uinput group and change group of uinput
adduser --group uinput
cp 91_hopr.rules /etc/udev/rules.d

# Reload udev rules
udevadm control --reload-rules
udevadm trigger

# Double check /dev/input/event* already has group input.
ls -al /dev/input/event*

adduser --shell /bin/false --no-create-home --disabled-login --gecos "" hopr
adduser hopr input
adduser hopr uinput

# Give hopr read permissions to the code. Either by adding a group or setting read flags.
# NOTE: Must set a+X permissions on all parent dirs
# Also, make sure the PYTHONPATH is correct etc

# Optionally, allow user to execute any command as hopr user.
# visudo /etc/sudoers.d/91_hopr_nopwd
## my_username ALL=(hopr) NOPASSWD: ALL

# TODO: Restrict execution permission to single command.

# Test with: sudo -u hopr python3 uinput_demo.py



