import threading
from pynput import keyboard
import time

def on_press(key, injected):
    print('{} pressed; it was {}\t{}'.format(
        key, 'faked' if injected else 'not faked', threading.get_ident()))

def on_release(key, injected):
    print('{} released; it was {}\t{}'.format(
        key, 'faked' if injected else 'not faked', threading.get_ident()))
    if key == keyboard.Key.esc:
        return False

print(threading.get_ident())

keyboardListener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    suppress=True)
keyboardListener.start()

print(threading.get_ident())

key = keyboard.Controller()

# key.tap("a")

# print()

# key.press(keyboard.Key.shift)
# key.tap("a")
# key.release(keyboard.Key.shift) #message sometimes gets sent twice, once faked and once not faked

# print()

# key.tap("a")

# print()

# key.press(keyboard.Key.shift) #message always gets sent twice, once not faked and once faked
# key.tap("a")
# key.release(keyboard.Key.shift) #message always gets sent twice, once not faked and once faked
# print()

# key.tap("a")


# time.sleep(0.1)
# key.tap(" ")
# time.sleep(0.1)

# print()

# key.press(keyboard.Key.space)
# time.sleep(0.1)
# key.tap(" ")
# time.sleep(0.1)
# key.release(keyboard.Key.space) #message sometimes gets sent twice, once faked and once not faked
# time.sleep(0.1)

# print()

# key.tap(" ")
# time.sleep(0.1)

# print()

# key.press(keyboard.Key.space) #message always gets sent twice, once not faked and once faked
# time.sleep(0.1)
# key.tap(" ")
# time.sleep(0.1)
# key.release(keyboard.Key.space) #message always gets sent twice, once not faked and once faked
# time.sleep(0.1)

# print()

# key.tap(" ")
# time.sleep(0.1)

key.tap(keyboard.Key.enter)
key.tap(keyboard.Key.enter)
# key.type(keyboard.Key.enter)
# key.type("\n")

#     
#does bug also happen with spacebar?