# $language = "python"
# $interface = "1.0"

import sys

# Settings
TEMP_PASSWD = "gc"

def main():
    screen = crt.Screen
    dlg = crt.Dialog

    screen.Synchronous = True

    passwd = dlg.Prompt('Please enter your password', isPassword = True)
    userID = dlg.Prompt("Enter user's employee ID")

# Set up access to DRUM's session to verify LAST4
    drumTab = crt.GetTab(1)
    if drumTab.Caption == "DRUM":
        drum = drumTab.Screen
    else:
        sys.exit("Could not locate DRUM tab")

# Verify Last4 of user's social 
    drum.Send("TOP\rINFORM\rLAST4\r\r")
    drum.WaitForString("Employee #=")
    drum.Send(userID + '\r')
    drum.WaitForString("GCM>")
    last4Check = dlg.MessageBox("Last4: " + drum.Get(drum.CurrentRow - 2, 10, drum.CurrentRow - 2, 14) + "\nEmployee: " + userID + "\n\nIs this correct?", "LAST4 Check", ICON_QUESTION | BUTTON_YESNO | DEFBUTTON1)
    if last4Check != IDYES:
        sys.exit("Unauthorized User")

# Change Password to TEMP_PASSWD
    screen.Send("sudo passwd " + userID + "\r")
    passwdResult = screen.WaitForStrings(":")
    screen.Send(TEMP_PASSWD + "\r")
    screen.WaitForString(":")
    screen.Send(TEMP_PASSWD + "\r")

# Unlock User's account
    screen.WaitForString("GCM>")
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


    # I personally like to see what just happened...
    #screen.Send("TOP\rINFORM\rPASSWORD FOR " + userID + " RESET\rACCOUNT UNLOCKED\r")

    screen.Synchronous = False

main()
