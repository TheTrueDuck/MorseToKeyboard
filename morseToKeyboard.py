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
        "...-.": " ", #VE = VErified = Space. Also ŝ
        "---.-.": "|", #OR
        "-......": "\\", #BS = BackSlash
        "-.--..": "[",
        "-.--..-": "]",
        "-.--...": "{",
        "-.--...-": "}",
        ".-.--": "~",
        "-..--": "`",
        ".-..-.-": "I, in my exalted wisdom and unbridled ambition, ", #EXA = EXAlted                
    }        
    
    SpecialKeys = {
        ".-.--......": lambda: mouseController.move(0, -1), #APEEEEE = Above Pointer ElusivE*5 = move mouse up        
        ".-.--.....": lambda: mouseController.move(0, -3), #APEEEE = Above Pointer ElusivE*4 = move mouse up        
        ".-.--....": lambda: mouseController.move(0, -7), #APEEE = Above Pointer ElusivE*3 = move mouse up        
        ".-.--...": lambda: mouseController.move(0, -17), #APEE = Above Pointer ElusivE*2 = move mouse up        
        ".-.--..": lambda: mouseController.move(0, -37), #APE = Above Pointer ElusivE*1 = move mouse up                    
        ".-.--.": lambda: mouseController.move(0, -73), #AP = Above Pointer = move mouse up
        ".-.--.-": lambda: mouseController.move(0, -149), #APT = Above Pointer TiTanic*1 = move mouse up        
        ".-.--.--": lambda: mouseController.move(0, -307), #APTT = Above Pointer TiTanic*2 = move mouse up        
        ".-.--.---": lambda: mouseController.move(0, -617), #APTTT = Above Pointer TiTanic*3 = move mouse up        
        ".-.--.----": lambda: mouseController.move(0, -1237), #APTTTT = Above Pointer TiTanic*4 = move mouse up
        ".-.--.-----": lambda: mouseController.move(0, -2477), #APTTTTT = Above Pointer TiTanic*5 = move mouse up
        
        "-..--......": lambda: mouseController.move(0, 1), #NPEEEEE = dowN Pointer ElusivE*5 = move mouse down
        "-..--.....": lambda: mouseController.move(0, 3), #NPEEEE = dowN Pointer ElusivE*4 = move mouse down
        "-..--....": lambda: mouseController.move(0, 7), #NPEEE = dowN Pointer ElusivE*3 = move mouse down
        "-..--...": lambda: mouseController.move(0, 17), #NPEE = dowN Pointer ElusivE*2 = move mouse down
        "-..--..": lambda: mouseController.move(0, 37), #NPE = dowN Pointer ElusivE*1 = move mouse down
        "-..--.": lambda: mouseController.move(0, 73), #NP = dowN Pointer = move mouse down
        "-..--.-": lambda: mouseController.move(0, 149), #NPT = dowN Pointer TiTanic*1 = move mouse down
        "-..--.--": lambda: mouseController.move(0, 307), #NPTT = dowN Pointer TiTanic*2 = move mouse down
        "-..--.---": lambda: mouseController.move(0, 617), #NPTTT = dowN Pointer TiTanic*3 = move mouse down
        "-..--.----": lambda: mouseController.move(0, 1237), #NPTTTT = dowN Pointer TiTanic*4 = move mouse down
        "-..--.-----": lambda: mouseController.move(0, 2477), #NPTTTTT = dowN Pointer TiTanic*5 = move mouse down
        
        "...--......": lambda: mouseController.move(1, 0), #IPEEEEE = rIght Pointer ElusivE*5 = move mouse right
        "...--.....": lambda: mouseController.move(3, 0), #IPEEEE = rIght Pointer ElusivE*4 = move mouse right
        "...--....": lambda: mouseController.move(7, 0), #IPEEE = rIght Pointer ElusivE*3 = move mouse right
        "...--...": lambda: mouseController.move(17, 0), #IPEE = rIght Pointer ElusivE*2 = move mouse right
        "...--..": lambda: mouseController.move(37, 0), #IPE = rIght Pointer ElusivE*1 = move mouse right
        "...--.": lambda: mouseController.move(73, 0), #IP = rIght Pointer = move mouse right        
        "...--.-": lambda: mouseController.move(149, 0), #IPT = rIght Pointer TiTanic*1 = move mouse right
        "...--.--": lambda: mouseController.move(307, 0), #IPTT = rIght Pointer TiTanic*2 = move mouse right
        "...--.---": lambda: mouseController.move(617, 0), #IPTTT = rIght Pointer TiTanic*3 = move mouse right
        "...--.----": lambda: mouseController.move(1237, 0), #IPTTTT = rIght Pointer TiTanic*4 = move mouse right
        "...--.-----": lambda: mouseController.move(2477, 0), #IPTTTTT = rIght Pointer TiTanic*5 = move mouse right                
        
        "--.--......": lambda: mouseController.move(-1, 0), #MPEEEEE = towards Marxism/coMMunisM (left) Pointer ElusivE*5 = move mouse left
        "--.--.....": lambda: mouseController.move(-3, 0), #MPEEEE = towards Marxism/coMMunisM (left) Pointer ElusivE*4 = move mouse left        
        "--.--....": lambda: mouseController.move(-7, 0), #MPEEE = towards Marxism/coMMunisM (left) Pointer ElusivE*3 = move mouse left
        "--.--...": lambda: mouseController.move(-17, 0), #MPEE = towards Marxism/coMMunisM (left) Pointer ElusivE*2 = move mouse left
        "--.--..": lambda: mouseController.move(-37, 0), #MPE = towards Marxism/coMMunisM (left) Pointer ElusivE*1 = move mouse left
        "--.--.": lambda: mouseController.move(-73, 0), #MP = towards Marxism/coMMunisM (left) Pointer = move mouse left
        "--.--.-": lambda: mouseController.move(-149, 0), #MPT = towards Marxism/coMMunisM (left) Pointer TiTanic*1 = move mouse left
        "--.--.--": lambda: mouseController.move(-307, 0), #MPTT = towards Marxism/coMMunisM (left) Pointer TiTanic*2 = move mouse left
        "--.--.---": lambda: mouseController.move(-617, 0), #MPTTT = towards Marxism/coMMunisM (left) Pointer TiTanic*3 = move mouse left
        "--.--.----": lambda: mouseController.move(-1237, 0), #MPTTTT = towards Marxism/coMMunisM (left) Pointer TiTanic*4 = move mouse left
        "--.--.-----": lambda: mouseController.move(-2477, 0), #MPTTTTT = towards Marxism/coMMunisM (left) Pointer TiTanic*5 = move mouse left
        
        
        
        ".-..---": lambda: mouseController.scroll( 0, 1), #A2 = Above scroll 2wards = scroll up
        "-...---": lambda: mouseController.scroll( 0,-1), #N2 = dowN scroll 2wards = scroll down
        "....---": lambda: mouseController.scroll( 1, 0), #I2 = rIght scroll 2wards = scroll right
        "--..---": lambda: mouseController.scroll(-1, 0), #M2 = Marxism/coMMunisM scroll 2wards (left) = scroll left

        "-----.": lambda: mouseController.click(mouse.Button.left, 1),    #MOE = MOuse lEft                 = mouse left click
        "-----..": lambda: mouseController.click(mouse.Button.left, 2),   #MOEE = MOuse lEft lEft           = mouse left double click
        "-----...": lambda: mouseController.click(mouse.Button.left, 3),  #MOEEE = MOuse lEft lEft lEft     = mouse left triple click
        "-----....": lambda: SlowMultiClick(mouse.Button.left, 3, 0.1), #MOEEEE = MOuse lEft lEft lEft Eh = mouse left slow triple click (sometimes instant triple click doesn't register)
        "------": lambda: mouseController.click(mouse.Button.right, 1),   #MOT = MOuse righT                = mouse right click
        "-------": lambda: OutMouseListener(lambda: mouseController.click(mouse.Button.middle, 1)), #MOM = MOuse Middle               = mouse middle click
        "--------": lambda: mouseController.click(mouse.Button.right, 2), #MOMT = MOuse Multi righT         = mouse double right click
        "---------": lambda: OutMouseListener(lambda: mouseController.click(mouse.Button.middle, 2)), #MOMM = MOuse Multi Middle      = mouse double middle click
        

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
        "........": keyboard.Key.backspace, #E*8 = Error
        "-.....": keyboard.Key.delete, #DEEE = DElEtE
        
        "-.-.-": keyboard.Key.home, #CT = home CweeT home. Also Start of work
        "...-.-": keyboard.Key.end, #VA = end oV it All. Also End of work
        

        ".-----": keyboard.Key.tab,
        "....-.-.": keyboard.Key.esc, #ESC = ESCape     
        

        "---.-": keyboard.Key.pg_up, #OA = AbOve = page up
        "-.---": keyboard.Key.pg_down, #NO = dOwN = page down
        
        
        
        ".-...--": keyboard.Key.up, #A3 = Above k3yboard = up arrow
        "-....--": keyboard.Key.down, #N3 = dowN k3yboard = down arrow
        ".....--": keyboard.Key.right, #I3 = rIght k3yboard = right arrow  
        "--...--": keyboard.Key.left, #M3 = towards k3yboard Marxism/coMMunisM (left) = left arrow
        
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

        #".--.-..": keyboard.Key.cmd,   #HM = Hold coMMand
        #".--..-..": mouse.Button.left,   #P
        #".--..-.": mouse.Button.right,   #HM = Hold coMMand
        #".--.--": mouse.Button.middle,   #HM = Hold coMMand
        #".--.....-": mouse.Button.button8,   #HM = Hold coMMand
        #".--......": mouse.Button.button9,   #HM = Hold coMMand
        #etc
        "-...-.": mouse.Button.left,   #D
        "-...--": mouse.Button.right,   #HM = Hold coMMand
        "-...---": mouse.Button.middle,   #HM = Hold coMMand
        "-...-....-": mouse.Button.button8,   #HM = Hold coMMand
        "-...-.....": mouse.Button.button9,   #HM = Hold coMMand
        #etc
    }

    isKeyHeld = {key: False for morse, key in HeldKeys.items()}
    
    ExitWord = "...---..." #SOS
    
    """
    for these, do a shift shortcut, so #HI3 for #
    #
    %
    ^
    *
    <>
    insert
    pause
    print screen
    scroll lock
    num lock caps lock
    
    release all held buttons
    undo -.--..
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
    
    canDoAutoSpace = False

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

            appropriateController = controller if key is keyboard.Key else mouseController

            if isKeyHeld[key]: appropriateController.press(key)
            else: appropriateController.release(key)
            
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

    errorSinewave = SineWave(pitch = 13, decibels=VolumeInDecibels, decibels_per_second=(VolumeInDecibels-smoothlyMuted) / fadeoutTime)
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
