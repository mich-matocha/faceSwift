import tempfile
import wave
import math
import struct
import random

import simpleaudio as sa

Rate = 125100.0
frequency = 1240.0

morse = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
         'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
         'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--',
         'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.---', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
         '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', '.': '.-.-.-', ',': '--..--',
         '?': '..--..', ':': '---...', '/': '-..-.', '-': '-....-', '=': '-...-', '\'': '.----.',
         '(': '-.--.-', ')': '-.--.-', '_': '..--.-', '&': '.-...', '!': '-.-.--', '\"': '.-..-.', '\;': '-.-.-.',
         '$': '...-..-'}

challengeStrings = ["Yeehaw, pardner!", "I love HowdyHack", "TEST!", "DOG", "COW", "I am tired"]


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
    return ret


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
        write_signal(wav, char2signal[char], volume=5767.0)
        write_signal(wav, 0.2, volume=0)

    wav.close()

    return file_


def play(f):
    wave_obj = sa.WaveObject.from_wave_file(f)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing


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


def game():
    str = random.choice(challengeStrings)
    morseStr = conv2Morse(str)
    soundFile = morse_to_wav(morseStr)

    right = False
    while not right:
        print(morseStr)
        print(str)
        guess = input("What do you think the morse says? ")
        ans = checkMorseGuess(guess, str)
        print(ans)
        if ans == str.upper():
            print("Nice job!")
            right = not right
        elif ans.upper() == "EXIT":
            print("Thanks for playing!")
            exit()


testString = 'Howdy'
testMorse = conv2Morse(testString)
print(testMorse)
file = morse_to_wav(testMorse)
# play(file)
playing = True
while playing:
    game()
    cont = input("Do you want to keep playing? (Y/N) ")
    if cont.upper() == "N" or cont.upper() == "NO":
        playing = False
