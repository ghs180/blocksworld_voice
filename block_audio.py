import speech_recognition as rs
import pyaudio
import audioop
import os
import math
from os import system
import threading
import subprocess

# Microphone stream config.
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 1500  # The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).

SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.


textfile = """time_step 0.005\nxyz 0.5 -0.5 0.5\nhpr 90.0 -25.0 0.0\n"""

file1 = open("test.txt" , "w")
file1.truncate(0)
file1.write(textfile)

def audio_int(num_samples=50):
    """ Gets average audio intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.
    """

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4)))
              for x in range(num_samples)]
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print(" Average audio intensity is ", r)
    stream.close()
    p.terminate()

    if r > THRESHOLD:
        listen(0)

    threading.Timer(SILENCE_LIMIT, audio_int).start()


"""
def listen(x):
    r=rs.Recognizer()
    if x == 0:
        system('say Hi. How can I help?')
    with rs.Microphone() as source:
        audio=r.listen(source)
    try:
        text = r.recognize_google(audio)
        y = process(text.lower())
        return(y)
    except:
        if x == 1:
            system('say Good Bye!')
        else:
            system('say I did not get that. Please say again.')
            listen(1)
"""

def listen(x, p):
    r=rs.Recognizer()
    if x == 0:
        system('say Hi. How can I help?')
    with rs.Microphone() as source:
        audio=r.listen(source)
        text = r.recognize_google(audio)
        res = process(text.lower(), p)
        return res

def process(text, p):
 #   ''''''''''''''''''''''''''''''''''''''''''''''''
 #   '''''''Your application goes here ''''''''''''''
 #   ''''''''''''''''''''''''''''''''''''''''''''''''
    words = text.split(' ')
    print(words)
    if words[0] == "exit":
        return -1
    if words[0] == "place":
        if words[1] == "block":
            if words[2] == "left":
                #file1.truncate(0)
                write_str = "block 0.1 0.05285 0.00385 0 0 0\n"
                file1.write(write_str)
                file1.close()
                process = subprocess.run(['./blocks-mac','test.txt'])
            elif words[2] == "right":
                write_str = "block 0.9 0.1549 0.05875 0 1.5708 1.5708 \n"
                file1.write(write_str)
                file1.close()
                process = subprocess.run(['./blocks-mac','test.txt'])

    if words[0] == "build":
        if words[1] == "structure":
            if words[2] == "right":
                #file1.truncate(0)
                write_str = """block 0.9 0.0451 0.05875 0 1.5708 1.5708\n
                               block 0.9 0.1549 0.05875 0 1.5708 1.5708\n
                               block 0.9 0.1 0.12135 0 0 1.5708\n
                               block 0.9 0.0451 0.18395 0 1.5708 1.5708\n
                               block 0.9 0.1549 0.18395 0 1.5708 1.5708\n
                               block 0.9 0.1 0.24655 0 0 1.5708\n
                               block 0.9 0.0451 0.30915 0 1.5708 1.5708\n
                               block 0.9 0.1549 0.30915 0 1.5708 1.5708\n
                               block 0.9 0.1 0.37175 0 0 1.5708\n
                               block 0.9 0.0451 0.43435 0 1.5708 1.5708\n
                               block 0.9 0.1549 0.43435 0 1.5708 1.5708\n
                               block 0.9 0.1 0.49695 0 0 1.5708"""
                file1.write(write_str)
                file1.close()
                process = subprocess.run(['./blocks-mac','test.txt'])
            elif words[2] == "left":
                write_str = """block 0.1 0.05285 0.00385 0 0 0\n
                               block 0.1 0.14715 0.00385 0 0 0\n
                               block 0.05285 0.1 0.01155 0 0 1.5708\n
                               block 0.14715 0.1 0.01155 0 0 1.5708\n
                               block 0.1 0.05285 0.01925 0 0 0\n
                               block 0.1 0.14715 0.01925 0 0 0\n
                               block 0.05285 0.1 0.02695 0 0 1.5708\n
                               block 0.14715 0.1 0.02695 0 0 1.5708\n
                               block 0.1 0.05285 0.03465 0 0 0\n
                               block 0.1 0.14715 0.03465 0 0 0\n
                               block 0.05285 0.1 0.04235 0 0 1.5708\n
                               block 0.14715 0.1 0.04235 0 0 1.5708\n
                               block 0.1 0.05285 0.05005 0 0 0\n
                               block 0.1 0.14715 0.05005 0 0 0\n
                               block 0.05285 0.1 0.05775 0 0 1.5708\n
                               block 0.14715 0.1 0.05775 0 0 1.5708"""
                file1.write(write_str)
                file1.close()
                process = subprocess.run(['./blocks-mac','test.txt'])



    return 0


#audio_int()

#process = subprocess.run(['./blocks-mac','test.txt'])

while True:
    res = listen(0, process)
    if res == -1:
        break
