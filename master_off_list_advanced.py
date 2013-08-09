#$language = "python"
#$interface = "1.0"

import sys

def main():
    """ Enter a list of sessions to kill separated by spaces, script kills them and handles all possible scenarios 
        This version shows all sessions logged into store at the end (info.us -l store#)"""
    screen = crt.Screen
    dlg = crt.Dialog

    screen.Synchronous = True

    userInput = dlg.Prompt("Please enter store number followed by sessions to kill (separated by spaces).", "MASTER OFF")
    if userInput == "":
        sys.exit("No sessions entered")
    inputList = userInput.split(" ")
    sessionList = inputList[1:]
    store = inputList[0]

    for session in sessionList:
        screen.Send("\r")
        screen.WaitForString("GCM>")
        screen.Send("MASTER OFF " + session + "\r")
        sResult = screen.WaitForStrings(["(CR)", "ERR", "Unable to get shared memory ID", "GCM>"], 2)
        if sResult == 1:
            screen.Send("\r")
            screen.WaitForString("(Y/CR=N)")
            screen.Send("Y\r")
            screen.WaitForString("(Y/CR=N)")
            screen.Send("Y\r")
        if sResult == 2:
            sys.exit("MASTER OFF ERROR")

    screen.Send("TOP\rINFORM\r")
    screen.WaitForString("GCM>")
    screen.Send("info.us -l " + store + "\r")

    screen.Synchronous = False

main()
