
import tempfile
import wave
import math
import struct
import PySimpleGUI as sg
import simpleaudio as sa
import random


soundFile = ''

#############################TEXT TO MORSE CODE########################################
morse = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
                 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
                 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-',
                 'W': '.--',
                 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.---', '2': '..---', '3': '...--', '4': '....-',
                 '5': '.....',
                 '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', '.': '.-.-.-', ',': '--..--',
                 '?': '..--..', ':': '---...', '/': '-..-.', '-': '-....-', '=': '-...-', '\'': '.----.',
                 '(': '-.--.-', ')': '-.--.-', '_': '..--.-', '&': '.-...', '!': '-.-.--', '\"': '.-..-.',
                 '\;': '-.-.-.',
                 '$': '...-..-'}

def conv2Morse(text):
    ret = ''
    arr = []
    arr[:0] = text
    for each in arr:
        try:
            each = each.upper()
        except ValueError:
            print("whoops, sorry")
        if each == " ":
            ret += "/ "
        else:
            ret += morse[each] + " "
    global soundFile
    soundFile = morse_to_wav(ret)
    return ret


###############################PLAYS SOUND#########################

def morse_to_wav(text, file_=None):
    char2signal = {'.': 0.2, '-': 0.4, '/': 0.5, ' ': 0.2}

    if not file_:
        _, file_ = tempfile.mkstemp(".wav")

    wav = wave.open(file_, 'w')
    wav.setnchannels(1)  # mono
    wav.setsampwidth(2)
    rate = 44100.0
    wav.setframerate(rate)

    for char in text:
        write_signal(wav, char2signal[char], volume=12767.0)
        write_signal(wav, 0.2, volume=0)

    wav.close()

    return file_



Rate = 125100.0
frequency = 1240.0

def write_signal(wavef, duration, volume=0, rate=44100.0, frequency=1240.0):
    """
    rate = 44100.0
    duration 0.1
    frequency = 1240.0
    """
    for i in range(int(duration * Rate * duration)):
        value = int(volume * math.sin(frequency * math.pi * float(i) / float(rate)))
        data = struct.pack('<h', value)
        wavef.writeframesraw(data)


def play(f):
    wave_obj = sa.WaveObject.from_wave_file(f)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing


###############################GAME###########################################
challengeStrings = ["TEST!", "DOG", "COW"]


def checkMorseGuess(guess, answer):
    guessArr = []
    guessArr[:0] = guess.strip().upper()

    ansArr = []
    ansArr[:0] = answer.upper()

    ret = ''
    for i in range(0,len(ansArr)):
        if i < len(guessArr) and ansArr[i] == guessArr[i]:
            ret += ansArr[i]
        else:
            ret += '#'
    return ret


# def game():
#     str = random.choice(challengeStrings)
#     morseStr = conv2Morse(str)
#     soundFile = morse_to_wav(morseStr)
#
#     right = False
#     while not right:
#         print(morseStr)
#         print(str)
#         guess = input("What do you think the morse says? ")
#         ans = checkMorseGuess(guess, str)
#         print(ans)
#         if ans == str.upper():
#             print("Nice job!")
#             right = not right
#         elif ans.upper() == "EXIT":
#             print("Thanks for playing!")
#             exit()
#
# playing = True
# while playing:
#     game()
#     cont = input("Do you want to keep playing? (Y/N) ")
#     if cont.upper() == "N" or cont.upper() == "NO":
#         playing = False


#############################USER INTERFACE####################################


import PySimpleGUI as sg

sg.theme('DarkPurple6')
layout = [[sg.Text("Hello Fellow Spy, Welcome to the Morse Code Encryptor! What message would you like us to encrypt?")],
[sg.Input(key='-input_phrase-')],[sg.Text("This is you encoded message:")], [sg.Output(size=(40,10))], [sg.Button('ENCODE'), sg.Button('Play Sound'), sg.Button('Guess'), sg.Button('Exit')]
,[sg.Button('Play a Game!')]
          ]

# Create the window
window = sg.Window("SPY ENCODER DEVICE", layout)
# Create an event loop

while True:
    event, values = window.read()
    input_phrase = ""
    game = False

    # Take in user input into variable input_phrase
    input_phrase = (str(values['-input_phrase-']))

    if event == 'ENCODE':
        print((conv2Morse(input_phrase)))

        # call encoding function
    if event == 'Play Sound':
        #print(input_phrase)
        print(conv2Morse(input_phrase))
        play(soundFile)

    if event == 'Play a Game!':
        game = True

    if game:
        str = random.choice(challengeStrings)
        morseStr = conv2Morse(str)

        right = False
        while not right:
            #print(morseStr)
            #print(str)
            if event == 'Guess':
                guess = input_phrase
                ans = checkMorseGuess(guess, str)
                #print(ans)
                if ans == str.upper():
                    print("Nice job!")
                    right = not right
                elif ans.upper() == "EXIT":
                    #print("Thanks for playing!")
                    exit()

    # playing = True
    # while playing:
    #     cont = input("Do you want to keep playing? (Y/N) ")
    #     if cont.upper() == "N" or cont.upper() == "NO":
    #         playing = False

        # checkMorseGuess(input_phrase,answer)


    if event == "Exit" or event == sg.WIN_CLOSED:
        # presses the EXIT button or closes the window
        break



