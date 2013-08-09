# $language = "python"
# $interface = "1.0"

import sys

def main():
    screen = crt.Screen
    dlg = crt.Dialog

    screen.Synchronous = True

    passwd = dlg.Prompt('Please enter your password', isPassword = True)
    userID = dlg.Prompt("Enter user's employee ID")


# Unlock User's account
    screen.Send("sudo gchelpdesk unlock " + userID + "\r")
    unlockResult = screen.WaitForStrings(["Password:", "Command unlock requested."], 15)
    if unlockResult == 0:
        sys.exit("Account unlock timed out!")
    if unlockResult == 1:
        screen.Send(passwd + "\r")
    
    screen.WaitForString("GCM>")
    screen.Send("ED\r")
    screen.WaitForString("Enter file number:")
    screen.Send("1\r")
    screen.WaitForString("Enter Record id:")
    screen.Send(userID + '\r')
    EDResult = screen.WaitForStrings(["Enter field number to edit:", "Record " + userID + "not found"], 15)
    if EDResult == 0:
        sys.exit("ED timed out!")
    if EDResult == 1:
        screen.Send("1\r")
        screen.WaitForString("change value:")
        screen.Send(" \r")
        screen.Send("2\r")
        screen.WaitForString("change value:")
        screen.Send(" \r")
        screen.Send("9\r")
        screen.WaitForString("change value:")
        screen.Send(" \r\r")

    screen.Synchronous = False

main()
