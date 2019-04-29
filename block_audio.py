import speech_recognition as rs
import pyaudio
import audioop
import os
import math
from os import system
import threading
import subprocess
import time
import pygame
import os
import pprint

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import spacy
import sys
import string
from nltk.stem.porter import *


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
x = 0
y = 0
a = 0
b = 0
c = 0
d = 0
rotate = True


for i in range(0, 300):
    try:
        os.remove("{}.txt".format(i))
    except:
        break


def listen(file1):
    r=rs.Recognizer()
    while(True):
        system('say Please state your command or question.')
        with rs.Microphone() as source:
            audio=r.listen(source)
            try:
                text = r.recognize_google(audio)
            except:
                system('say Please repeat your command or question.')
                text = r.recognize_google(audio)
            res = process(text.lower(), file1)
            return res

def build_block(x, y, a, b, c, d):
    global file_counter
    x_val = 0.1 + x * 0.2
    y_val = 0.00385 + y * 0.2
    textfile = textfile_init
    textfile += "block {} {} {} {} {} {}\n".format(x_val, y_val, a, b, c, d)
    file1 = open("{}.txt".format(file_counter) , "w")
    file1.write(textfile)
    file1.close()
    textfile = textfile_init
    file_counter += 1

def build_block2(x, y, a, b, c, d):
    global file_counter
    textfile = textfile_init
    textfile += "block {} {} {} {} {} {}\n".format(x, y, a, b, c, d)
    file1 = open("{}.txt".format(file_counter) , "w")
    file1.write(textfile)
    file1.close()
    textfile = textfile_init
    file_counter += 1

def build_structure(x, y):
    global file_counter
    x_val1 = 0.1 + x * 0.2 #xval for front and back planks
    y_val_front = 0.05285 + y * 0.2
    y_val_back = 0.14715 + y * 0.2
    x_val_left = 0.05285 + x * 0.2 #xval for left
    x_val_right = 0.14715 + x * 0.2 #xval for right
    y_val1 = 0.1 + y * 0.2 #yval for left/right
    #struct = """block {} {} 0.00385 0 0 0\nblock {} {} 0.00385 0 0 0\nblock {} {} 0.01155 0 0 1.5708\nblock {} {} 0.01155 0 0 1.5708\n""".format(x_val1, y_val_front, x_val1, 
                                                                                                                                              #  y_val_back, x_val_left, y_val1, 
                                                                                                                                              #  x_val_right, y_val1)
    i = 0
    for i in range(0, 2):
        build_block2(x_val1, y_val_front, 0.00385, 0, 0, 0)
        build_block2(x_val1, y_val_back, 0.00385, 0, 0, 0)
        build_block2(x_val_left, y_val1, 0.01155, 0, 0, 1.5708)
        build_block2(x_val_right, y_val1, 0.01155, 0, 0, 1.5708)

    '''
    textfile = textfile_init
    textfile += ret
    print("Building structure at ({},{}) in {}.txt".format(x, y, file_counter))
    file1 = open("{}.txt".format(file_counter) , "w")
    print(file1)
    file1.write(textfile)
    file1.close()
    textfile = textfile_init
    file_counter += 1'''

def process(text, file1):
 #   ''''''''''''''''''''''''''''''''''''''''''''''''
 #   '''''''Your application goes here ''''''''''''''
 #   ''''''''''''''''''''''''''''''''''''''''''''''''
    global textfile
    words = text.split(' ')
    print(words)
    if words[0] == "exit" or words[0] == "stop" or words[0] == "quit":
        return -1
    if words[0] == "wait":
        return -3
    if words[0] == "build" or words[0] == "place":
        if len(words) == 3 and len(words[2]) == 3 and words[2][1] == "/":
            x = int(words[2][0])
            y = int(words[2][2])
        elif len(words) > 3 and words[2] == "to":
            x = 2
            if len(words) > 3 and words[3] == "three":
                y = 3
            elif words[3] == "to":
                y = 2
            else:
                y = int(words[3])
        elif len(words) > 3 and words[2] == "three":
            x = 3
            if len(words) > 3 and words[3] == "three":
                y = 3
            else:
                y = int(words[3])
        elif len(words) > 2 and words[2] == "tutu":
            x = 2
            y = 2
        elif len(words) > 3 and words[2] == "for":
            x = 4
            y = int(words[3])
        elif len(words) > 3 and words[3] == "for":
            x = int(words[2])
            y = 2
        elif len(words) > 3:
            x = int(words[2])
            y= int(words[3])
        if words[1] == "block":
            build_block(x, y, a, b, c, d)
            return 1
        elif words[1] == "structure":
            build_structure(x, y)
            return 1
    else:
        file1 = open("question.txt", "w")
        file1.truncate(0)
        file1.write(text)
        file1.close()
        system('python3 answer.py wiki.txt question.txt')

def audio_control():
    while True:
        res = listen(file1)
        if res == -1:
            system('say Exiting voice control!')
            break
        if res == -3:
            system('say Good night!')
            time.sleep(10)


        if res == 0:
            system('say Unable to recognize your command.')


'''
Steps:
0. Run simulation initially empty
1. Ask user if they would like to add object(s) to grid
2. User adds object to grid using voice/remote
3. Run simulation and repeat step 1
'''

#Controller code

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self, ):
        """Listen for events to happen"""
        global file_counter, x, y, a, b, c, d, rotate
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        x = 0
        y = 0
        a = 0.01155
        b = 0
        c = 0
        d = 1.5708
        while True:
            for event in pygame.event.get():
                '''if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:
                        if event.value > 0:
                            
                            #print("right")
                        if event.value < 0:
                            #print("left")
                    if event.axis == 1:
                        if event.value > 0:
                            #print("down")
                        if event.value < 0:
                            #print("up")'''
                if event.type == pygame.JOYBUTTONUP:
                    if event.button == 1:
                        build_block(x, y, a, b, c, d)
                        system('say Building block at {} {}'.format(x, y))
                    if event.button == 2:
                        build_structure(x, y)
                        system('say Building structure at {} {}'.format(x, y))
                    if event.button == 3:
                        system('say Activating voice control')
                        audio_control()
                    if event.button == 4:
                        system('say Rotating left.')
                        if rotate == True:
                            #0.01155 0 0 1.5708
                            a = 0.00385
                            b = 0
                            c = 0
                            d = 0
                            rotate = False
                        else:
                            a = 0.01155
                            b = 0
                            c = 0
                            d = 1.5708
                            rotate = True
                        print("{} {} {} {}".format(a,b,c,d))

                    if event.button == 5:
                        system('say Rotating right.')
                        print("{} {} {} {}".format(a,b,c,d))
                        if rotate == True:
                            #0.01155 0 0 1.5708
                            a = 0.00385
                            b = 0
                            c = 0
                            d = 0
                            rotate = False
                        else:
                            a = 0.01155
                            b = 0
                            c = 0
                            d = 1.5708
                            rotate = True
                        print("{} {} {} {}".format(a,b,c,d))

                    
                        
                        
                elif event.type == pygame.JOYHATMOTION:
                    if event.hat == 0:
                        if event.value == (1, 0):
                            if x < 8:
                                x += 1
                            system('say {} {}.'.format(x, y))
                        if event.value == (-1, 0):
                            if x > 0:
                                x -= 1
                            system('say {} {}.'.format(x, y))
                        if event.value == (0, 1):
                            if y < 8:
                                y += 1
                            system('say {} {}.'.format(x, y))
                        if event.value == (0, -1):
                            if y > 0:
                                y -= 1
                            system('say {} {}.'.format(x, y))
                        
                #pprint.pprint(self.button_data)
                #pprint.pprint(self.axis_data)
                #pprint.pprint(self.hat_data)

'''
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
        listen()
    threading.Timer(SILENCE_LIMIT, audio_int).start()
'''


file_counter = 0
#Init text file
textfile_init = """time_step 0.005\nxyz 0.5 -0.5 0.5\nhpr 90.0 -25.0 0.0\n"""
textfile = textfile_init
file1 = open("{}.txt".format(file_counter) , "w")
file1.truncate(0)
file1.write(textfile)
file1.close()
file_counter += 1
#Step 0
#Run simulation with empty textfile
sprocess = subprocess.Popen(['./blocks'], stdin = subprocess.PIPE, stdout = subprocess.PIPE)

#Set up PS4 remote IMPORTANT TO UNCOMMENT IF REMOTE CONNECTED
ps4 = PS4Controller()
ps4.init()
system('say Enabled remote control')
ps4.listen()



#input_bytes = os.linesep.join(["username@email.com", "password"]).encode("ascii")
#sprocess.communicate(input_bytes)



