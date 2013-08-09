#$language = "python"
#$interface = "1.0"

INFOUS = False   # True to send 'info.us -l ' when complete

def main():
    """ Enter a list of sessions to kill separated by spaces, script kills them and handles all possible scenarios """

    screen = crt.Screen
    dlg = crt.Dialog
    errorList = []

    screen.Synchronous = True

    userInput = dlg.Prompt("Please enter sessions to kill separated by spaces.", "MASTER OFF")
    if userInput == "":
        return
    userInput2 = userInput.replace(".", " ")
    sessionList = userInput2.split(" ")
    
    screen.Send("TOP\rINFORM\r")
    for session in sessionList:
        if session == "":
            continue
        screen.Send("MASTER OFF " + session)
        screen.WaitForString("MASTER OFF " + session)   # must wait for the Send before returning, otherwise the sResult goes before the MASTER OFF
        screen.Send("\r")
        sResult = screen.WaitForStrings(["(CR)", "ERR", "GCM>"], 1)
        if sResult == 1:
            screen.Send("\rY\rY\r")
            screen.WaitForString("GCM>")
        if sResult == 2:
            errorList.append(session)
            continue

    screen.Send("TOP\rINFORM\r")
    if len(errorList) > 0:
        screen.Send("Errors occurred with the following sessions:\r")
        screen.Send(", ".join(errorList) + "\r")
    if INFOUS:
        screen.WaitForString("GCM>")
        screen.Send("info.us -l ")

    screen.Synchronous = False

main()
