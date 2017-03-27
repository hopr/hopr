import sys
import signal

import logging

signal_name = dict((v,k) for k,v in vars(signal).items() if k.startswith('SIG'))

def exit_on_signal(sig, frame):
    msg = 'Caught signal {}={}. Exiting...'.format(signal_name[sig], sig)
    if sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGTSTP):
        logging.info(msg)
        sys.exit(0) # NOTE: Raises SystemExit
    else:
        raise RuntimeError(msg)

def register_signal_handlers():
    # NOTE: Application exits on C-z
    
    # Handle signals: Hangup, terminate, suspend (terminal stop)
    # SIGTERM: Ask for termination. Can be blocked
    # SIGINT: Interrupt C-c.
    # SIGTSTP: Suspend C-z.
    # SIGHUP: Hangup. Terminal disconnected.
    # SIGQUIT: User detected error. Create core dump. TODO:

    # Unblockable and unhandled:
    # SIGSTOP: Stops process.
    # SIGKILL: Unblockable kill

    for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGTSTP, signal.SIGQUIT, signal.SIGINT):
        signal.signal(sig, exit_on_signal)
