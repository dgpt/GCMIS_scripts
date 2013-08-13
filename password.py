# $language = "python"
# $interface = "1.0"

"""
# BUG - Fixed:
GCM>sudo passwd 050913
Password:
3004-687 User "050913" does not exist.
"""

import sys

# Settings
TEMP_PASSWD = "gc"
DEBUG = False       # True to prevent completion message and screen clear at end


def topout(screen, msg = ""):
    screen.Send("TOP\rINFORM\rTOP\rINFORM\r")
    if msg != "":
        screen.WaitForString("GCM>")
        screen.Send(msg + "\r")

def wait(screen, string = "GCM>", timeout = 0):
    if timeout > 0:
        return screen.WaitForString(string, timeout)
    else:
        return screen.WaitForString(string)

def main():
    screen = crt.Screen
    dlg = crt.Dialog

    screen.Synchronous = True

    passwd = dlg.Prompt('Please enter your password.', isPassword = True)
    if passwd == "":
        return
    userID = dlg.Prompt("Enter user's employee ID")
    if len(str(userID)) != 6:
        sys.exit("Invalid employee ID")

    # Set up access to DRUM's session to verify LAST4 and pull Employee Name
    drumTab = crt.GetTab(1)
    if drumTab.Caption == "DRUM" and drumTab.Session.Connected:
        drum = drumTab.Screen
    else:
        sys.exit("Could not locate DRUM tab or DRUM not connected")

    # Get Employee Name from SY100
    topout(drum)
    wait(drum)
    drum.Send("*SY100\r")
    wait(drum, "Login Id")
    drum.Send(userID + "\r")
    wait(drum, "Cont")
    employee_name = drum.Get(4, 11, 4, 36)
    topout(drum)

    resetYesOrNo = dlg.MessageBox("Reset " + userID + "'s password to '" + TEMP_PASSWD + "'?\r\r" +
                                  employee_name + "\r\r" +
                                  "(Press No to only unlock)", "Reset and Unlock or Unlock Only?", ICON_WARN | BUTTON_YESNO | DEFBUTTON2)

# Following steps are only relevant if resetting passwd
    if resetYesOrNo == IDYES:
    # Verify Last4 of user's social
        drum.Send("TOP\rINFORM\rLAST4\r\r")
        drum.WaitForString("Employee #=")
        drum.Send(userID + '\r')
        drum.WaitForString("GCM>")
        last4Check = dlg.MessageBox("Last4: " + drum.Get(drum.CurrentRow - 2, 10, drum.CurrentRow - 2, 14) + "\nEmployee: " + userID + "\n\nIs this correct?", "LAST4 Check", ICON_QUESTION | BUTTON_YESNO | DEFBUTTON1)
        if last4Check != IDYES:
            sys.exit("Unauthorized User")
        drum.Send("TOP\rINFORM\r")

    # Change Password to TEMP_PASSWD
        screen.Send("sudo passwd " + userID + "\r")
        passwdResult = screen.WaitForStrings(["Password:", userID + "'s New password:", "does not exist"], 5)
        if passwdResult == 0:
            sys.exit("Password reset timed out!")
        if passwdResult == 1:
            screen.Send(passwd + "\r")
            passwdResult2 = screen.WaitForStrings(["Sorry, try again.", userID + "'s New password:", "does not exist"], 5)
            if passwdResult2 == 1:
                screen.Send("\r\r\rTOP\rINFORM\r")
                sys.exit("Incorrect password.")
            if passwdResult2 == 3:
                passwdResult = 3
        if passwdResult == 3:
            screen.Send("\rTOP\rINFORM\rTOP\rINFORM\r")
            sys.exit("User " + userID + " does not exist.")
        screen.Send(TEMP_PASSWD + "\r")
        screen.WaitForString(":")
        screen.Send(TEMP_PASSWD + "\r")
        screen.WaitForString("GCM>")

# Unlock User's account
    screen.Send("sudo gchelpdesk unlock " + userID + "\r")
    unlockResult = screen.WaitForStrings(["Password:", "Command unlock requested."], 10)
    if unlockResult == 0:
        sys.exit("Account unlock timed out!")
    if unlockResult == 1:
        screen.Send(passwd + "\r")
        unlockResult2 = screen.WaitForStrings(["Sorry, try again.", "Command unlock requested."], 5)
        if unlockResult2 == 1:
            screen.Send("\r\r\rTOP\rINFORM\r")
            sys.exit("Incorrect password.")

    screen.WaitForString("GCM>")
    screen.Send("ED\r")
    screen.WaitForString("Enter file number:")
    screen.Send("1\r")
    screen.WaitForString("Enter Record id:")
    screen.Send(userID + '\r')
    EDResult = screen.WaitForStrings(["Enter field number to edit:", "Record " + userID + " not found"], 10)
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
    if EDResult == 2:
        screen.WaitForString(":")
        screen.Send("\r")


    # Show completion message
    if DEBUG == False:
        screen.Send("TOP\rINFORM\r")
        if resetYesOrNo == IDYES:
            screen.Send("PASSWORD FOR " + userID + " RESET\r")
        screen.Send("ACCOUNT UNLOCKED\r")

    screen.Synchronous = False

main()
