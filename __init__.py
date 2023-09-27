'''
Deps
portaudio19-dev
'''

# UI imports
import curses

# Google drive imports
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# For keyboard testing
import keyboard

# For system info
import platform

# audio test
#import pysine
from scipy.io.wavfile import write
import pyaudio
import wave


gauth = GoogleAuth()
drive = GoogleDrive(gauth)


class testCollector:
    def __init__(self, testName: str = "", testData: str = "", result: bool = False):

        self.__dict = {
            "testName": testName,
            "testData": testData,
        }
        self.__passed = result

    def setName(self, name: str):
        self.__dict["testName"] = name

    def setData(self, data: str):
        self.__dict["testData"] = data

    def setPassed(self, passed: bool):
        self.__passed = passed

    def getName(self):
        return self.__dict["testName"]

    def getData(self,):
        return self.__dict["testData"]

    def getPassed(self):
        return self.__passed


def printtestCollector(screen, testResult: testCollector):
    screen.clear()
    screen.addstr(0, 0, "Test Name: " + testResult.getName())
    screen.addstr(1, 0, "Test Passed: " + str(testResult.getPassed()))
    screen.addstr(2, 0, "Test Data:\n" + testResult.getData())
    screen.refresh()


def keyboardTest(stdscr):
    targetKeys = ['enter', 'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'unknown', 'scroll lock', 'pause', 'page up', 'home', 'insert', 'delete', 'end', 'page down', 'up', 'left', 'down', 'right', '`', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                  '0', '−', '=', 'backspace', 'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'caps lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '#', 'shift', '|', 'z', '\\', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'ctrl', 'alt', 'alt gr', 'menu', 'space']

    keysAlreadyRead = dict()
    missingKeys = list()
    testResult = testCollector()

    testResult.setName("Keyboard Test")
    while True:
        stdscr.refresh()
        keyIn = keyboard.read_key()
        keyInstr = str(keyIn)
        stdscr.addstr(0, 0, "Press ctrl+d to exit\n")
        stdscr.addstr(1, 0, "Last key pressed: " + str(keyInstr) + "\n")
        if keyboard.is_pressed('ctrl+d'):
            break
        if keyInstr not in keysAlreadyRead:
            keysAlreadyRead[str(keyInstr)] = 0
            missingKeys = set(targetKeys) - set(list(keysAlreadyRead.keys()))
            stdscr.addstr(2, 0, "new key found: " + str(keyInstr) + "\n")
            stdscr.addstr(3, 0, "keys pressed: " +
                          str(list(keysAlreadyRead.keys())) + "\n")
            stdscr.addstr(4, 0, "keys not yet pressed: " +
                          str(missingKeys) + "\n")
            if len(missingKeys) == 0:
                testResult.setPassed(True)
                break

    testResult.setData("Keys pressed:" +
                       str(list(keysAlreadyRead.keys())) + "\n" +
                       "Keys not pressed: " + str(list(missingKeys)) + "\n")

    return testResult


def audioTest(stdscr):
    hello = 0

from ctypes import *
from contextlib import contextmanager
import pyaudio

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

def main(stdscr):

    

    # Clear screen
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Conor's PC test tool")
    stdscr.addstr(1, 0, "Press any key to get started")
    stdscr.refresh()

    printtestCollector(stdscr, keyboardTest(stdscr))

    # get system info
    while True:
        pass


# sampleRate = 44100  # Sample rate
# seconds = 3  # Duration of recording
# myrecording = sd.rec(int(seconds * sampleRate), samplerate=sampleRate, channels=2)
# pysine.sine(frequency=440.0, duration=1.0)
# sd.wait() # wait for recording to finish
# write('output.wav', sampleRate, myrecording)  # Save as WAV file


with noalsaerr():
    audio = pyaudio.PyAudio()  # Create an interface to PortAudio

# Ask the user what audio device to use for audio recording

for index in range(audio.get_device_count()):
    print("index " + str(index) + " " + str(audio.get_device_info_by_index(index)["name"]))
print("Please enter the number which matches your audio device, it's usually 0")
inputIndex = input()
info = audio.get_device_info_by_index(int(inputIndex))

#Check if sample rate exists on device

if "defaultSampleRate" in info.keys():
    fs = int(info["defaultSampleRate"])  # Record at 44100 samples per second
else:
    fs = 16000

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
seconds = 3
filename = "outputa.wav"

print('Recording')

stream = audio.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True, input_device_index=2)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
audio.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(audio.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

exit()

curses.wrapper(main)
