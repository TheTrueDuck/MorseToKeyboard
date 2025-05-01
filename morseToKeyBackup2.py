 # # import keyboard
# import pyautogui
import time
from pynput import keyboard
from pynput import mouse
from pysinewave import SineWave

#Simply edit these values to change the behaviour of the program :)
#------------------------------------------------------------------

VolumeInDecibels = -35
MorseKey = keyboard.Key.space

SupressKeyboardEvents = True
SupressMouseEvents = False

KeyboardTeminateKey = keyboard.Key.esc
MouseTeminateKey = mouse.Button.middle

WordsPerMinute = 15 #PARIS standard


#Make SOS exit lol

#------------------------------------------------------------------

Alphabet = {
    ".-": "a",
    "-...": "b",
    "-.-.": "c",
    "-..": "d",
    ".": "e",
    "..-.": "f",
    "--.": "g",
    "....": "h",
    "..": "i",
    ".---": "j",
    "-.-": "k",
    ".-..": "l",
    "--": "m",
    "-.": "n",
    "---": "o",
    ".--.": "p",
    "--.-": "q",
    ".-.": "r",
    "...": "s",
    "-": "t",
    "..-": "u",
    "...-": "v",
    ".--": "w",
    "-..-": "x",
    "-.--": "y",
    "--..": "z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0",
}

fadeoutTime = 0.05
smoothlyMuted = -1000

sinewave = SineWave(pitch = 17, decibels=VolumeInDecibels, decibels_per_second=(VolumeInDecibels-smoothlyMuted) / fadeoutTime)
# sinewave.set_frequency(1000)

heldStartTime = None#time.time()
print(heldStartTime)
currentLetter = []

dotDuration = 1.2/WordsPerMinute

timeOfLastRelease = time.time()

def on_press(key, injected):
    global heldStartTime
    if heldStartTime == None and key != KeyboardTeminateKey: #and key == MorseKey:
        try:
            print('alphanumeric key {} pressed; it was {}'.format(
                key.char, 'faked' if injected else 'not faked'))
        except AttributeError:
            print('special key {} pressed'.format(
                key))
        
        heldStartTime = time.time()
        # print(heldStartTime)
        
        sinewave.play()
        sinewave.set_volume(VolumeInDecibels)

def on_release(key, injected):
    print('{} released; it was {}'.format(
        key, 'faked' if injected else 'not faked'))
    
    global heldStartTime, timeOfLastRelease
    if key == KeyboardTeminateKey:
        # Stop listener
        return False
    elif heldStartTime != None:# key == MorseKey:
        # heldStartTime = time.time()
        heldTime = time.time() - heldStartTime
        currentLetter.append(heldTime)
        print(heldTime)
        print(currentLetter)
        heldStartTime = None
        
        timeOfLastRelease = time.time()
        
        sinewave.set_volume(smoothlyMuted)
        time.sleep(fadeoutTime)
        sinewave.stop()




def on_move(x, y):
    # print('Pointer moved to {0}'.format((x, y)))
    pass

def on_click(x, y, button, pressed):
    print('{0} {2} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y),
        button))
    if button == MouseTeminateKey and not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))


# from pynput.keyboard import Key, Controller

# key = Controller()

# # Press and release space
# key.press(Key.space)
# key.release(Key.space)

# # Type a lower case A; this will work even if no key on the
# # physical keyboard is labelled 'A'
# key.press('a')
# key.release('a')

# # Type two upper case As
# key.press('A')
# key.release('A')
# with key.pressed(Key.shift):
#     key.press('a')
#     key.release('a')

# # Type 'Hello World' using the shortcut type method
# key.type('Hello World')




# from pynput.mouse import Button, Controller

# mouse = Controller()

# # Read pointer position
# print('The current pointer position is {0}'.format(
#     mouse.position))

# # Set pointer position
# mouse.position = (10, 20)
# print('Now we have moved it to {0}'.format(
#     mouse.position))

# # Move pointer relative to current position
# mouse.move(5, -5)

# print('Now we have moved it to {0}'.format(
#     mouse.position))

# # Press and release
# mouse.press(Button.left)
# mouse.release(Button.left)

# # Double click; this is different from pressing and releasing
# # twice on macOS
# mouse.click(Button.left, 2)

# # Scroll two steps down
# mouse.scroll(0, 2)
    
print("Listening to input! Press esc, middle mouse button, or input ...---... to terminate.")

#supress mouse
mouseListener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll,
    suppress=SupressMouseEvents)
mouseListener.start()

# with mouse.Listener(
#         on_move=on_move,
#         on_click=on_click,
#         on_scroll=on_scroll,
#         suppress=True) as mouseListener:


#     # Collect events until released
#     with keyboard.Listener(
#             on_press=on_press,
#             on_release=on_release,
#             suppress=True) as listener:
        
        
        
#         # key.type('Hello World')
        
        
#         listener.join()
#         mouseListener.join()
# print("Hello, world! 2")
# # ...or, in a non-blocking fashion:
keyboardListener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    suppress=SupressKeyboardEvents)
keyboardListener.start()


# from pysinewave import SineWave

# fadeoutTime = 0.05
# smoothlyMuted = -1000


# # Create a sine wave, with a starting pitch of 12, and a pitch change speed of 10/second.
# sinewave = SineWave(pitch = 17, decibels=SinewaveVolumeInDecibels, decibels_per_second=(SinewaveVolumeInDecibels-smoothlyMuted) / fadeoutTime)

# # Turn the sine wave on.
# sinewave.play()

# # Sleep for 2 seconds, as the sinewave keeps playing.
# time.sleep(1)

# # Set the goal pitch to -5.
# # sinewave.set_pitch(5)
# sinewave.set_volume(smoothlyMuted)
# # sinewave.play()
# # Sleep for 3 seconds, as the sinewave smoothly slides its pitch down from 12 to -5, and stays there.
# time.sleep(fadeoutTime)
# sinewave.stop()

# sinewave.play()
# sinewave.set_volume(SinewaveVolumeInDecibels)
# key = keyboard.Controller()
# # with key.pressed(keyboard.Key.shift):
# key.press(keyboard.Key.shift)
# key.press('a')
# key.release('a')
# key.type("hello World")
# key.press('b')
# key.release('b')
# key.release(keyboard.Key.shift)

# key.type("hello World")
# key.press('C')
# key.release('C')

# key.press('DAr')
# key.release('DAr')

key = keyboard.Controller()

while mouseListener.is_alive() and keyboardListener.is_alive():
    # print("waiting")
    time.sleep(0.1)
    
    if len(currentLetter) == 0 or time.time() <= timeOfLastRelease + 7*dotDuration: 
        # print("no")
        continue
    
    # seperator = (min(currentLetter)+max(currentLetter)) / 2 #should this weigh the dash more than the dot since dashes are 3x as long? Or is average better for grouping them?
    seperator = 1.666*dotDuration
    # letter = #list(map(lambda x: (if x>= seperator: "-" else: "."), currentLetter))
    if(sum(currentLetter)/len(currentLetter) > seperator): symbol = "-"
    else: symbol = "."
    letter = [symbol for duration in currentLetter]
    print("sim:", end="\t")
    print(letter)
    
    # seperator = (min(currentLetter)+max(currentLetter)) / 2 #should this weigh the dash more than the dot since dashes are 3x as long? Or is average better for grouping them?
    seperator = 1.666*dotDuration
    # letter = #list(map(lambda x: (if x>= seperator: "-" else: "."), currentLetter))
    letter = ["-" if duration >= seperator else "." for duration in currentLetter]
    print("wpm:", end="\t")
    print(letter)
    
    seperator = (2*min(currentLetter) + max(currentLetter)) / 3 #should this weigh the dash more than the dot since dashes are 3x as long? Or is average better for grouping them?
    # seperator = 2*dotDuration
    # letter = #list(map(lambda x: (if x>= seperator: "-" else: "."), currentLetter))
    letter = ["-" if duration >= seperator else "." for duration in currentLetter]
    print("avg:", end="\t")
    print(letter)
    print("seper:", end="\t")
    print(seperator)
    
    # range = max(currentLetter) - min(currentLetter)
    # print("range:", end="\t")
    # print(range)
    ratio = max(currentLetter) / min(currentLetter)
    print("ratio:", end="\t")
    print(ratio)    
    
    # if range > 0.5*dotDuration:
    # if ratio > 1.666:
    # if ratio > 1.8:
    if ratio > 2:
        print("Use avg")
    else:
        print("Use wmp")
    
    currentLetter = []
    # key.type(currentLetter)
    

# Stop both if one stops
mouseListener.stop()
keyboardListener.stop()


# # time.sleep(10)
# time.sleep(5)
# keyboard.Controller().type('Hello World')
# time.sleep(5)


print("Terminating.")


errorSinewave = SineWave(pitch = 13, decibels=VolumeInDecibels, decibels_per_second=(VolumeInDecibels-smoothlyMuted) / fadeoutTime)
errorSinewave.play()
time.sleep(0.15)
errorSinewave.set_volume(smoothlyMuted)
time.sleep(fadeoutTime)
errorSinewave.stop()
