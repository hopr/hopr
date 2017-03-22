from evdev import UInput, ecodes

KEY_RELEASE = 0L
KEY_PRESS = 1L

def run():    
    ui = UInput()
    ui.write(ecodes.EV_KEY, ecodes.KEY_A, KEY_PRESS)
    ui.write(ecodes.EV_KEY, ecodes.KEY_A, KEY_RELEASE)
    ui.syn()
    ui.close()


if __name__ == "__main__":
    run()









