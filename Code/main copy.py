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


def morse2text(mors):
  mstr = mors.split(" ")
  ret = ''
  for w in mstr:
      ret += list(morse.keys())[list(morse.values()).index(w)]
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


############################# USER INTERFACE ####################################


import PySimpleGUI as sg

# import os
#
# cwd = os.getcwd()
# fname = 'Morse_Code.png'
#
# with open('{}/{}'.format(cwd, fname)) as fh:
#     Morse_Code = fh.read()

sg.theme('DarkBlack')
layout = [[sg.Text("Hello Fellow Spy, Welcome to the Morse Code Encryptor! What message would you like us to encrypt?")],
        [sg.Input(key='-input_phrase-')],
          [sg.Button('Encode'), sg.Button('Decode'), sg.Button('Play Sound')],
        [sg.Text("This is your encoded/decoded message:")],
        [sg.Output(size=(40,10), key='-OUTPUT-')],
          [sg.Button('Clear'),sg.Button('Exit')]
]

window = sg.Window("SPY ENCODER DEVICE", layout).Finalize()
window.Maximize()

while True:
    event, values = window.read()

    input_phrase = ""
    #input_phrase2 = ""
    game = False

    # Take in user input into variable input_phrase
    input_phrase = (str(values['-input_phrase-']))
    #input_phrase2 = (str(values['-input_phrase2-']))

    if event == 'Encode':
        print(input_phrase, "encoded:", conv2Morse(input_phrase))
        # call encoding function

    if event == 'Play Sound':
        print(input_phrase)
        print(conv2Morse(input_phrase))
        play(soundFile)

    if event == 'Decode':
        print("Decoded:", morse2text(input_phrase))

    if event == 'Clear':
        window['-OUTPUT-'].update('')

    if event == "Exit" or event == sg.WIN_CLOSED:
        break