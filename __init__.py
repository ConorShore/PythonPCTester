# UI imports
import curses

# Google drive imports
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# For keyboard testing
import keyboard

# For system info
import platform

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
    # targetKeys = ['enter', 'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'unknown', 'scroll lock', 'pause', 'page up', 'home', 'insert', 'delete', 'end', 'page down', 'up', 'left', 'down', 'right', '`', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    #               '0', '−', '=', 'backspace', 'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'caps lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '#', 'shift', '|', 'z', '\\', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'ctrl', 'alt', 'alt gr', 'menu', 'space']

    targetKeys = ['a']

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

    testResult.setData("Keys pressed:" + \
        str(list(keysAlreadyRead.keys())) + "\n" + \
        "Keys not pressed: " + str(list(missingKeys)) + "\n")

    return testResult


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


curses.wrapper(main)
