from evdev import UInput, ecodes
KEY_RELEASE = 0
KEY_PRESS = 1

ui = UInput()
ui.write(ecodes.EV_KEY, ecodes.KEY_A, KEY_PRESS)
ui.write(ecodes.EV_KEY, ecodes.KEY_A, KEY_RELEASE)
ui.syn()
ui.close()










