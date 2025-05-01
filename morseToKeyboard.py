try:
    # # import keyboard
    # import pyautogui
    import threading
    import time
    from pynput import keyboard
    from pynput import mouse
    from pysinewave import SineWave

    #Simply edit these values to change the behaviour of the program :)
    #------------------------------------------------------------------

    WordsPerMinute = 15 #PARIS standard

    VolumeInDecibels = -35
    MorseKey = keyboard.Key.space

    SuppressKeyboardEvents = True
    SupressMouseEvents = False

    KeyboardTeminateKey = keyboard.Key.esc
    MouseTeminateKey = mouse.Button.middle

    AutoSpace = True#False

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
        
        ".--.-": "à", #also å
        "-.-..": "ç", #also ć, ĉ
        "----": "š", #also ch, ĥ
        "..-..": "é", #also ę, đ
        "..--.": "ð",
        ".-..-": "è", #also ł
        "--.-.": "ĝ",
        ".---.": "ĵ",
        "--.--": "ñ", #also ń
        "---.": "ö", #also ø, ó
        "...-...": "ś",
        ".--..": "þ",
        "..--": "ü", #also ŭ
        "--..-.": "ź",
        "--..-": "ż",
        "..-.-": "¿",
        
        #--not official--
        "...-.": " ", #VE = VErified = Space
        ".-..-.-": "I, in my exalted wisdom and unbridled ambition, ", #EXA = EXAlted                
    }        
    
    SpecialKeys = {
        #--not official--
        #mouse movements need coords! also prob make UI and MO switxh. Nah moving happen way more
        # "..-...-": lambda: mouseController.move(0, 1), #UIA = UI Above = move mouse up
        # "..-..-.": lambda: mouseController.move(0, -1), #UIN = UI dowN = move mouse down
        # "..-...": lambda: mouseController.move(-1, 0), #UIE = UI lEft = move mouse left
        # "..-..-": lambda: mouseController.move(1, 0), #UIT = UI righT = move mouse right
        
        "..-...-": lambda: mouseController.move(0, -100), #UIA = UI Above = move mouse up
        "..-..-.": lambda: mouseController.move(0, 100), #UIN = UI dowN = move mouse down
        "..-....": lambda: mouseController.move(100, 0), #UII = UI rIght = move mouse right
        "..-..--": lambda: mouseController.move(-100, 0), #UIM = UI towards Marxism/coMMunisM (left) = move mouse left

        # "..---.-": lambda: mouseController.click(mouse.Button.scroll_up), #2A = scroll 2 Above = scroll up
        # "..----.": lambda: mouseController.click(mouse.Button.scroll_down), #2N = scroll 2 dowN = scroll down
        # "..---.": lambda: mouseController.click(mouse.Button.scroll_left), #2E = scroll 2 lEft = scroll left
        # "..----": lambda: mouseController.click(mouse.Button.scroll_right), #2T = scroll 2 righT = scroll right
        
        # "..---.-": lambda: mouseController.scroll(0, 1), #2A = scroll 2 Above = scroll up
        # "..----.": lambda: mouseController.scroll(0, -1), #2N = scroll 2 dowN = scroll down
        # "..---.": lambda: mouseController.scroll(-1, 0), #2E = scroll 2 lEft = scroll left
        # "..----": lambda: mouseController.scroll(1, 0), #2T = scroll 2 righT = scroll right
        
        "..---.-": lambda: mouseController.scroll(0, 1), #2A = scroll 2wards Above = scroll up
        "..----.": lambda: mouseController.scroll(0, -1), #2N = scroll 2wards dowN = scroll down
        "..---..": lambda: mouseController.scroll(1, 0), #2I = scroll 2wards rIght = scroll right
        "..-----": lambda: mouseController.scroll(-1, 0), #2M = scroll 2wards Marxism/coMMunisM (left) = scroll left

        "-----.": lambda: mouseController.click(mouse.Button.left, 1),    #MOE = MOuse lEft                 = mouse left click
        "-----..": lambda: mouseController.click(mouse.Button.left, 2),   #MOEE = MOuse lEft lEft           = mouse left double click
        "-----...": lambda: mouseController.click(mouse.Button.left, 3),  #MOEEE = MOuse lEft lEft lEft     = mouse left triple click
        "-----....": lambda: SlowMultiClick(mouse.Button.left, 3, 0.1), #MOEEEE = MOuse lEft lEft lEft Eh = mouse left slow triple click (sometimes instant triple click doesn't register)
        "------": lambda: mouseController.click(mouse.Button.right, 1),   #MOT = MOuse righT                = mouse right click
        "-------": lambda: OutMouseListener(lambda: mouseController.click(mouse.Button.middle, 1)), #MOM = MOuse Middle               = mouse middle click
        "--------": lambda: mouseController.click(mouse.Button.right, 2), #MOMT = MOuse Multi righT         = mouse double right click
        "---------": lambda: OutMouseListener(lambda: mouseController.click(mouse.Button.middle, 2)), #MOMM = MOuse Multi Middle      = mouse double middle click
        
        # "------": lambda: OutMouseListener(lambda: mouseController.click(mouse.Button.right, 1)),   #MOT = MOuse righT                = mouse right click
        # # "-------": lambda: with OutMouseListener(): mouseController.click(mouse.Button.middle, 1), #MOI = MOuse mIddle               = mouse middle click #!!!!!!!!!!!!!!shouldn't terminate!
        # "-------": lambda: OutMouseListener(lambda: mouseController.click(mouse.Button.middle, 1)), #MOI = MOuse mIddle               = mouse middle click #!!!!!!!!!!!!!!shouldn't terminate!
        # "--------": lambda: OutMouseListener(lambda: mouseController.click(mouse.Button.right, 2)), #MOIT = MOuse twIce righT         = mouse double right click
        # "---------": lambda: OutMouseListener(lambda: mouseController.click(mouse.Button.middle, 2)), #MOII = MOuse twIce mIddle      = mouse double middle click
        
        
        # "-----.": mouse.Button.left,    #MOE = MOuse lEft                 = mouse left click
        # "-----..": mouse.Button.left,   #MOEE = MOuse lEft lEft           = mouse left double click
        # "-----...": mouse.Button.left,  #MOEEE = MOuse lEft lEft lEft     = mouse left triple click
        # "-----....": mouse.Button.left, #MOEEEE = MOuse lEft lEft lEft Eh = mouse left slow triple click (sometimes instant triple click doesn't register)
        # "------": mouse.Button.right,   #MOT = MOuse righT                = mouse right click
        # "-------": mouse.Button.middle, #MOI = MOuse mIddle               = mouse middle click #!!!!!!!!!!!!!!shouldn't terminate!
        # "--------": mouse.Button.right, #MOIT = MOuse twIce righT         = mouse double right click
        # "---------": mouse.Button.middle, #MOII = MOuse twIce mIddle      = mouse double middle click
        #these numbered button seem to be offset by 4. I expect this is because button4-7 are taken by the scroll buttons
        #if these produce an error, it may be because windows doesn't support them. In that case, use Buttons x1 and x2 for back and forward and delete the rest.
        "-----....-": lambda: mouseController.click(mouse.Button.button8), #M4 = MOuse 4 = mouse button 4/back click
        "-----.....": lambda: mouseController.click(mouse.Button.button9), #M5 = MOuse 5 = mouse button 5/forward click
        "------....": lambda: mouseController.click(mouse.Button.button10), #M6 = MOuse 6 = mouse button 6 click 
        "-------...": lambda: mouseController.click(mouse.Button.button11), #M7 = MOuse 7 = mouse button 7 click 
        "--------..": lambda: mouseController.click(mouse.Button.button12), #M8 = MOuse 8 = mouse button 8 click 
        "---------.": lambda: mouseController.click(mouse.Button.button13), #M9 = MOuse 9 = mouse button 9 click 
        "-----.---------": lambda: mouseController.click(mouse.Button.button14), #M10 = MOuse 10 = mouse button 10 click 
        "-----.----.----": lambda: mouseController.click(mouse.Button.button15), #M11 = MOuse 11 = mouse button 11 click 
        "-----.----..---": lambda: mouseController.click(mouse.Button.button16), #M12 = MOuse 12 = mouse button 12 click 
        "-----.----...--": lambda: mouseController.click(mouse.Button.button17), #M13 = MOuse 13 = mouse button 13 click 
        "-----.----....-": lambda: mouseController.click(mouse.Button.button18), #M14 = MOuse 14 = mouse button 14 click 
        "-----.----.....": lambda: mouseController.click(mouse.Button.button19), #M15 = MOuse 15 = mouse button 15 click 
        "-----.-----....": lambda: mouseController.click(mouse.Button.button20), #M16 = MOuse 16 = mouse button 16 click 
        "-----.------...": lambda: mouseController.click(mouse.Button.button21), #M17 = MOuse 17 = mouse button 17 click 
        "-----.-------..": lambda: mouseController.click(mouse.Button.button22), #M18 = MOuse 18 = mouse button 18 click 
        "-----.--------.": lambda: mouseController.click(mouse.Button.button23), #M19 = MOuse 19 = mouse button 19 click 
        "-----..--------": lambda: mouseController.click(mouse.Button.button24), #M20 = MOuse 20 = mouse button 20 click 
        "-----..---.----": lambda: mouseController.click(mouse.Button.button25), #M21 = MOuse 21 = mouse button 21 click 
        "-----..---..---": lambda: mouseController.click(mouse.Button.button26), #M22 = MOuse 22 = mouse button 22 click 
        "-----..---...--": lambda: mouseController.click(mouse.Button.button27), #M23 = MOuse 23 = mouse button 23 click 
        "-----..---....-": lambda: mouseController.click(mouse.Button.button28), #M24 = MOuse 24 = mouse button 24 click 
        "-----..---.....": lambda: mouseController.click(mouse.Button.button29), #M25 = MOuse 25 = mouse button 25 click 
        "-----..----....": lambda: mouseController.click(mouse.Button.button30), #M26 = MOuse 26 = mouse button 26 click 
        
    }
    
    KeysThatAreSuppressedForSomeReason = {
        ".-.-": keyboard.Key.enter, #RT = ReTurn = enter. Also ä
        #--not official--
        "........": keyboard.Key.backspace, #HH
        
        "....-.-.": keyboard.Key.esc, #ESC = ESCape     
        
        # "...--.-": keyboard.Key.up, #3A = k3yboard Above = up arrow
        # "...---.": keyboard.Key.down, #3N = k3yboard dowN = down arrow
        # "...--.": keyboard.Key.left, #3E = k3yboard lEft = left arrow
        # "...---": keyboard.Key.right, #3T = k3yboard righT = right arrow  
        
        "...--.-": keyboard.Key.up, #3A = k3yboard Above = up arrow
        "...---.": keyboard.Key.down, #3N = k3yboard dowN = down arrow
        "...--..": keyboard.Key.right, #3I = k3yboard rIght = right arrow  
        "...----": keyboard.Key.left, #3M = k3yboard towards Marxism/coMMunisM (left) = left arrow
        
        "..-..----": keyboard.Key.f1, #F1
        "..-...---": keyboard.Key.f2, #F2
        "..-....--": keyboard.Key.f3, #F3
        "..-.....-": keyboard.Key.f4, #F4
        "..-......": keyboard.Key.f5, #F5
        "..-.-....": keyboard.Key.f6, #F6
        "..-.--...": keyboard.Key.f7, #F7
        "..-.---..": keyboard.Key.f8, #F8
        "..-.----.": keyboard.Key.f9, #F9
        "..-..---------": keyboard.Key.f10, #F10
        "..-..----.----": keyboard.Key.f11, #F11
        "..-..----..---": keyboard.Key.f12, #F12
        "..-..----...--": keyboard.Key.f13, #F13
        "..-..----....-": keyboard.Key.f14, #F14
        "..-..----.....": keyboard.Key.f15, #F15
        "..-..-----....": keyboard.Key.f16, #F16
        "..-..------...": keyboard.Key.f17, #F17
        "..-..-------..": keyboard.Key.f18, #F18
        "..-..--------.": keyboard.Key.f19, #F19
        "..-...--------": keyboard.Key.f20, #F20
        
        #shortened notation
        # "..-..-": keyboard.Key.f1, #F1
        # "..-...-": keyboard.Key.f2, #F2
        # "..-....-": keyboard.Key.f3, #F3
        # "..-.....-": keyboard.Key.f4, #F4
        # "..-......": keyboard.Key.f5, #F5
        # "..-.-....": keyboard.Key.f6, #F6
        # "..-.-...": keyboard.Key.f7, #F7
        # "..-.-..": keyboard.Key.f8, #F8
        # "..-.-.": keyboard.Key.f9, #F9
        # "..-..--": keyboard.Key.f10, #F10
        # "..-..-.-": keyboard.Key.f11, #F11
        # "..-..-..-": keyboard.Key.f12, #F12
        # "..-..-...-": keyboard.Key.f13, #F13
        # "..-..-....-": keyboard.Key.f14, #F14
        # "..-..-.....": keyboard.Key.f15, #F15
        # "..-..--....": keyboard.Key.f16, #F16
        # "..-..--...": keyboard.Key.f17, #F17
        # "..-..--..": keyboard.Key.f18, #F18
        # "..-..--.": keyboard.Key.f19, #F19
        # "..-...--": keyboard.Key.f20, #F20
    }

    HeldKeys = {
        "......": keyboard.Key.shift, #HI = Hold shIft
        ".....-": keyboard.Key.alt,   #HA = Hold Alt
        "....-.": keyboard.Key.ctrl,  #HN = Hold coNtrol
        "....--": keyboard.Key.cmd,   #HM = Hold coMMand
    }

    isKeyHeld = {key: False for morse, key in HeldKeys.items()}
    
    ExitWord = "...---..." #SOS
    
    """
    ...---... exit
    ---.-. | #OR
    \\
    $
    %
    ^
    *
    tab
    <>
    []
    {}
    `~
    mouse
    move big medium small up down left right
    scroll big medium small up down left right
    click left right middle 4 5
    double click left right middle 4 5
    drag/hold left right middle 4 5

    release all held buttons
    
    home end, pg up, pg down

    #$%^*
    for these, do a shift shortcut, so #HI3 for #
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
        pass
    def on_click(x, y, button, pressed):
        if button == MouseTeminateKey and not pressed:
            return False
    def on_scroll(x, y, dx, dy):
        pass


    def SlowMultiClick(button, timesToClick, delay):
        for i in range(timesToClick):
            if i != 0: time.sleep(delay)
            mouseController.press(button)
            time.sleep(delay)
            mouseController.release(button)

    # from pynput.mouse import Button, Controller
    
    class OutKeyboardListener:
        def __init__(self, function = None):
            if(function != None):
                with OutKeyboardListener():
                    function()
                    
        def __enter__(self):
            global keyboardListener
            keyboardListener.stop()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            global keyboardListener
            keyboardListener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release,
                suppress=SuppressKeyboardEvents
            )
            keyboardListener.start()
            
    class OutMouseListener:
        def __init__(self, function = None):
            if(function != None):
                with OutMouseListener():
                    function()
        
        def __enter__(self):
            global mouseListener
            mouseListener.stop()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            global mouseListener
            mouseListener = mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll,
                suppress=SupressMouseEvents)
            mouseListener.start()
                                


    mouseController = mouse.Controller()
    
    
    mouseController.move(73, 73)
    # mouseController.move(73, 73)
    
    # mouseController.move(2477, 2477)
    
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
    
    # mouseController.press(Button.button8)
    # mouseController.release(Button.button8)
    # mouseController.press(Button.scroll_up)
    # mouseController.release(Button.scroll_up)
    # mouseController.press(Button.scroll_left)
    # mouseController.release(Button.scroll_left)

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
        suppress=SuppressKeyboardEvents)
    keyboardListener.start()


    controller = keyboard.Controller()
    
    
    
    # with OutKeyboardListener():
    #     controller.tap(keyboard.Key.esc) 
    #     controller.tap(keyboard.Key.esc) 
    # def multitap():
    #     controller.tap(keyboard.Key.esc)
    #     controller.tap(keyboard.Key.esc)
    
    # OutKeyboardListener(lambda: multitap())
    
    # controller.tap(keyboard.Key.esc) 
    
    # with OutMouseListener():
    #     mouseController.click(mouse.Button.middle)     
    
    
    
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
                    suppress=SuppressKeyboardEvents)
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
            controller.type(key)
            print(f"last is '{key[-1]}'")
            if(key[-1] == ' '): canDoAutoSpace = False
            else: canDoAutoSpace = True
        elif morse in SpecialKeys:
            function = SpecialKeys[morse]
            print(f"Recognized function!")
            function()
            canDoAutoSpace = False
        elif morse in KeysThatAreSuppressedForSomeReason:
            key = KeysThatAreSuppressedForSomeReason[morse]
            print(f"Recognized: {key}")
            
            if SuppressKeyboardEvents:
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
                    suppress=SuppressKeyboardEvents)
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
        elif morse == ExitWord:
            print("SOS Recognized!")
            keyboardListener.stop()
            mouseListener.stop()
            break
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
    time.sleep(0.35)
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
