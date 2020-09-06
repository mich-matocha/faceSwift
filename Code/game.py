###############################GAME###############################
import tempfile
import wave
import math
import struct
import PySimpleGUI as sg
import simpleaudio as sa
import random
import time


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
        write_signal(wav, char2signal[char], volume=32767.0)
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


sg.theme('DarkBlack')
layout =[[sg.Text(" Type to Start Game")],
         [sg.Input(key='-input_phrase-')],
         [sg.Output(size=(40,9), key='-OUTPUT-')],
         [sg.Button('Submit')]
         ]
window = sg.Window("Spy Game", layout)

game = True
right = False
stri = random.choice(challengeStrings)
morseStr = conv2Morse(stri)
while game:
    event, values = window.read()

    input_phrase = ""

    if not right:
        if event == 'Submit':
            window['-OUTPUT-'].update('')
            print('Input your guess')
            input_phrase = str(values['-input_phrase-'])
            #print("fre3")
            guess = input_phrase
            ans = checkMorseGuess(guess, stri)
            if ans == stri.upper():
                #game = False
                right = not right
                print("Nice job!")
                print('Would you like to keep playing? (Y/N)')
                #right = not right
            else:
                print(morseStr)
                print(ans)

    else:
        if event == 'Submit':
            input_phrase = str(values['-input_phrase-'])
            if input_phrase == 'Y' or input_phrase == 'y':
                right = not right
            else:
                print("Bye!")
                time.sleep(5)
                window.close()

window.close()


