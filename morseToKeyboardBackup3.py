try:
    # # import keyboard
    # import pyautogui
    import threading
    import time
    from pynput import keyboard
    from pynput import mouse
    from pysinewave import SineWave
    # import pyautogui

    #Simply edit these values to change the behaviour of the program :)
    #------------------------------------------------------------------

    WordsPerMinute = 15 #PARIS standard

    VolumeInDecibels = -35
    MorseKey = keyboard.Key.space

    SupressKeyboardEvents = True
    SupressMouseEvents = False

    KeyboardTeminateKey = keyboard.Key.esc
    MouseTeminateKey = mouse.Button.middle

    AutoSpace = True#False

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
        "-----": "0",
        ".----": "1",
        "..---": "2",
        "...--": "3",
        "....-": "4",
        ".....": "5",
        "-....": "6",
        "--...": "7",
        "---..": "8",
        "----.": "9",
        ".-.-.-": ".",
        "--..--": ",",
        "..--..": "?",
        ".----.": "'",
        "-.-.--": "!",
        "-..-.": "/",
        "-.--.": "(",
        "-.--.-": ")",
        ".-...": "&",
        "---...": ":",
        "-.-.-.": ";",
        "-...-": "=",
        ".-.-.": "+",
        "-....-": "-",
        "..--.-": "_",
        ".-..-.": '"',
        "...-..-": "$",
        ".--.-.": "@",
        #--not official--
        "...-.": " ", #VE = VErified = Space
        # ".-.-": "qq\nee\ntrew\tyy", #RT = Return = Enter. Also ä
        ".-..-.-": "I, in my exalted wisdom and unbridled ambition, ", #EXA = EXAlted
    }

    KeysThatAreSuppressedForSomeReason = {
        ".-.-": keyboard.Key.enter, #HI = Hold shIft
        "........": keyboard.Key.backspace, #HI = Hold shIft
        "--------------": keyboard.Key.tab, #HI = Hold shIft
        # ".....-": keyboard.Key.alt,   #HA = Hold Alt
        # "....-.": keyboard.Key.ctrl,  #HN = Hold coNtrol
        # "....--": keyboard.Key.cmd,   #HM = Hold coMMand
    }

    HeldKeys = {
        "......": keyboard.Key.shift, #HI = Hold shIft
        ".....-": keyboard.Key.alt,   #HA = Hold Alt
        "....-.": keyboard.Key.ctrl,  #HN = Hold coNtrol
        "....--": keyboard.Key.cmd,   #HM = Hold coMMand
    }

    isKeyHeld = {key: False for morse, key in HeldKeys.items()}
    """
    ........ backspace
    ...---... exit
    .-.- enter
    space
    ---.-. | #OR
    \\
    $
    %
    ^
    *
    toggle shift = capslock
    toggle contol
    toggle alt
    toggle windows
    tab
    <>
    []
    {}
    f1-f12
    `~
    esc (but not out of the programm)

    up down left right arrows
    mouse
    move big medium small up down left right
    scroll big medium small up down left right
    click left right middle 4 5
    double click left right middle 4 5
    drag/hold left right middle 4 5

    release all held buttons
    
    home end, pg up, pg down
    #$%^*
    """


    fadeoutTime = 0.05
    smoothlyMuted = -1000

    sinewave = SineWave(pitch = 17, decibels=VolumeInDecibels, decibels_per_second=(VolumeInDecibels-smoothlyMuted) / fadeoutTime)
    # sinewave.set_frequency(1000)

    errorSinewave = SineWave(pitch = 13, decibels=VolumeInDecibels, decibels_per_second=(VolumeInDecibels-smoothlyMuted) / fadeoutTime)

    heldStartTime = None#time.time()
    print(heldStartTime)
    currentLetter = []

    dotDuration = 1.2/WordsPerMinute

    timeOfLastRelease = time.time()

    def on_press(key, injected):
        try:
            print('alphanumeric key {} pressed; it was {}'.format(
                key.char, 'faked' if injected else 'not faked'))
        except AttributeError:
            print('special key {} pressed; it was {}'.format(
                key, 'faked' if injected else 'not faked'))
        global heldStartTime
        if heldStartTime == None and key == MorseKey and not injected:
            
            heldStartTime = time.time()
            # print(heldStartTime)
            
            sinewave.play()
            sinewave.set_volume(VolumeInDecibels)
            
            # key = keyboard.Controller()
            # key.tap(keyboard.Key.enter)

    def on_release(key, injected):
        print('{} released; it was {}'.format(
            key, 'faked' if injected else 'not faked'))
        
        global heldStartTime, timeOfLastRelease
        if key == KeyboardTeminateKey:
            # Stop listener
            return False
        elif heldStartTime != None and key == MorseKey and not injected:
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
        # print('{0} {2} at {1}'.format(
        #     'Pressed' if pressed else 'Released',
        #     (x, y),
        #     button))
        if button == MouseTeminateKey and not pressed:
            # Stop listener
            return False

    def on_scroll(x, y, dx, dy):
        # print('Scrolled {0} at {1}'.format(
        #     'down' if dy < 0 else 'up',
        #     (x, y)))
        pass




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

    keyboardListener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=SupressKeyboardEvents)
    keyboardListener.start()


    controller = keyboard.Controller()
    
    canDoAutoSpace = False
    # key.tap(keyboard.Key.caps_lock)
    
    # key.tap(keyboard.Key.enter)

    while mouseListener.is_alive() and keyboardListener.is_alive():
        # print("waiting")
        time.sleep(0.01)
        
        if AutoSpace and len(currentLetter) == 0 and heldStartTime == None and time.time() > timeOfLastRelease + 7*dotDuration: 
            # print("a")
            if canDoAutoSpace:            
                print("auto space")
                # controller.tap(keyboard.Key.space)   
                # controller.type("")   
                
                print(f"Restarting listener...")
                keyboardListener.stop();
                
                #for whatever reason, keys like enter and backspace dont manage to break through the suppression, 
                #so we have to stop the suppression, press the key twice (no idea why), and restart the suppression
                controller.tap(keyboard.Key.space) 
                controller.tap(keyboard.Key.space)                 
                
                keyboardListener = keyboard.Listener(
                    on_press=on_press,
                    on_release=on_release,
                    suppress=SupressKeyboardEvents)
                keyboardListener.start()
                
                print(f"Restarted listener.")
                
                canDoAutoSpace = False 
            # else:
            #     print("b")
        
        if len(currentLetter) == 0 or heldStartTime != None or time.time() <= timeOfLastRelease + 3*dotDuration: 
            # print("no")
            continue        
        # controller.tap(keyboard.Key.space)   
        # print(f"aaaaaa {threading.get_ident()}")
        # # key.press(keyboard.Key.enter)
        # # time.sleep(1)
        # # key.release(keyboard.Key.enter)
        # time.sleep(1)     
        # # key = keyboard.Controller()           
        # # key.tap(keyboard.Key.enter) 
        # pyautogui.press("enter")
        # pyautogui.press("return")
        # pyautogui.press("\n")
        # continue
        
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
            seperator = (2*min(currentLetter) + max(currentLetter)) / 3 #should this weigh the dash more than the dot since dashes are 3x as long? Or is average better for grouping them?
            # seperator = 2*dotDuration
            # letter = #list(map(lambda x: (if x>= seperator: "-" else: "."), currentLetter))
            letter = ["-" if duration >= seperator else "." for duration in currentLetter]
            print(letter)
        else:
            print("Use sim")
            # seperator = (min(currentLetter)+max(currentLetter)) / 2 #should this weigh the dash more than the dot since dashes are 3x as long? Or is average better for grouping them?
            seperator = 1.666*dotDuration
            # letter = #list(map(lambda x: (if x>= seperator: "-" else: "."), currentLetter))
            if(sum(currentLetter)/len(currentLetter) > seperator): symbol = "-"
            else: symbol = "."
            letter = [symbol for duration in currentLetter]
            print("sim:", end="\t")
            print(letter)
        
        morse = ''.join(letter)
        if morse in Alphabet:
            key = Alphabet[morse]
            print(f"Recognized: {key}")
            controller.type(key) #maybe use tap instead and key enum?
            print(f"last is '{key[-1]}'")
            if(key[-1] == ' '): canDoAutoSpace = False
            else: canDoAutoSpace = True
        elif morse in KeysThatAreSuppressedForSomeReason:
            key = KeysThatAreSuppressedForSomeReason[morse]
            print(f"Recognized: {key}")
            
            if SupressKeyboardEvents:
                print(f"Restarting listener...")
                keyboardListener.stop();
                
                # key = keyboard.Controller()
                # time.sleep(0.1)
                
                #for whatever reason, keys like enter and backspace dont manage to break through the suppression, 
                #so we have to stop the suppression, press the key twice (no idea why), and restart the suppression
                controller.tap(key) 
                controller.tap(key) 
                
                # key.press(output)
                # key.release(output)
                # key.press(output)
                # key.release(output)
                
                
                # key.tap(keyboard.Key.enter)
                # key.tap(keyboard.Key.enter)
                # key.tap(keyboard.Key.enter) 
                # key.tap(keyboard.Key.enter) 
                
                keyboardListener = keyboard.Listener(
                    on_press=on_press,
                    on_release=on_release,
                    suppress=SupressKeyboardEvents)
                keyboardListener.start()
                
                print(f"Restarted listener.")
            else:
                controller.tap(key)   
            
            canDoAutoSpace = False
        elif morse in HeldKeys:
            key = HeldKeys[morse]
            isKeyHeld[key] = not isKeyHeld[key]
            # key.touch(HeldKeys[input], isKeyHeld[input])
            if isKeyHeld[key]: controller.press(key)
            else: controller.release(key)
            
            print(f"Key {key} pressed state is now {isKeyHeld[key]}!")
            print(f"Shift: {controller.shift_pressed}")
            
            canDoAutoSpace = False
        else:
            print(f"Not recognized!")        
            errorSinewave.set_volume(VolumeInDecibels)
            errorSinewave.play()
            time.sleep(0.15)
            errorSinewave.set_volume(smoothlyMuted)
            time.sleep(fadeoutTime)
            errorSinewave.stop()

        currentLetter = []
        

    # Stop both if one stops
    mouseListener.stop()
    keyboardListener.stop()


    # # time.sleep(10)
    # time.sleep(5)
    # keyboard.Controller().type('Hello World')
    # time.sleep(5)

except Exception as e:
    # print(e)
    print("Error encountered!")
    
    errorSinewave.set_volume(VolumeInDecibels)
    errorSinewave.play()
    time.sleep(0.3)
    # errorSinewave.set_volume(smoothlyMuted)
    # time.sleep(fadeoutTime + dotDuration)
    # errorSinewave.stop()
    
    raise e
finally:
    print("Terminating.")

    for key, isHeld in isKeyHeld.items():
        if(isHeld):
            print(f"Releasing {key}")
            controller.release(key)
    
    errorSinewave.set_volume(VolumeInDecibels)
    errorSinewave.play()
    time.sleep(0.15)
    errorSinewave.set_volume(smoothlyMuted)
    time.sleep(fadeoutTime)
    errorSinewave.stop()