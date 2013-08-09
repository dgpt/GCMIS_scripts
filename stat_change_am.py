#$language = "python"
#$interface = "1.0"

"""
Input: Employee ID
Output: Green Screen Automation and Information pull

Performs all stat change related information in Green Screen for Assistant Managers.

Drum:
Menu Level 6
Approval Level 6
Dial
Printer Group store#.MGR
Mgmt Cd = D
Remote = Y

At end of script show the following in a MessageBox

"Create a GC Stores Profile for User.
- script looks up the following info from *MA050
Ops Region
Ops Distr.
User First Name
User Last Name
Employee ID
"""

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

    employee = dlg.Prompt("Enter employee ID", "AM Stat Change")
    passwd = dlg.Prompt("Enter your POS Approval Password", "AM Stat Change", "", True)

# Error Checking
# Make sure employee number is valid (in string format)
    if len(employee) != 6 or not employee.isdigit():
        topout(screen, "Invalid Employee ID")
        return

# Make sure script is running on DRUM server
    if crt.GetScriptTab().Caption.lower() != "drum":
        topout(screen, "Please run this script on DRUM")
        return
# End Error Checking

    topout(screen)
    wait(screen)

# Open SY100, select Employee
    screen.Send("*SY100\r")
    wait(screen, "Login Id")
    screen.Send(employee + "\r")

# Wait for shit to load
    screen.WaitForCursor()
    wait(screen, "Cont")

# Get store number from Loc id field and employee name (to return)
    store = screen.Get(5, 11, 5, 13)
    employee_name = screen.Get(4, 11, 4, 36)

# Group Cd
    screen.Send("5\r\rASST.MGR\r")

# Printer Group
    wait(screen, "Cont")
    screen.Send("6\r" + store + ".MGR\r")

# Remote
    wait(screen, "Cont")
    screen.Send("11\rY\r")

# Mgmt Cd
    wait(screen, "Cont")
    screen.Send("12\rD\r")

# Dial
    gcstudios_raw = screen.Get(12, 7, 12, 20)
    gcstudios = gcstudios_raw == "GC Studio Menu"

    r3 = "\r" * 3
    r4 = "\r" * 4

    if gcstudios:
        screen.Send("19.2" + r4 + "2" + r3 +
                    "19.4" + r4 + "6" + r3 +
                    "19.5" + r4 + "1" + r3 +
                    "19.6" + r4 + "6" + r3 +
                    "19.8" + r4 + "6" + r3 +
                    "19.9" + r4 + "4" + r3 +
                    "19.17" + r4 + "6" + r3)
    else:
        screen.Send("19.2" + r4 + "2" + r3 +
                    "19.3" + r4 + "6" + r3 +
                    "19.4" + r4 + "1" + r3 +
                    "19.5" + r4 + "6" + r3 +
                    "19.7" + r4 + "6" + r3 +
                    "19.8" + r4 + "4" + r3 +
                    "19.16" + r4 + "6" + r3)

    screen.Send("\r")

    if not wait(screen, "MANAGER APPROVAL REQUIRED", 3):
        topout(screen, "Stat change already completed.")
        return

    screen.Send(passwd + "\r\r")

    pwresult = screen.WaitForStrings(["MANAGER APPROVAL REQUIRED", "GCM>"])
    if pwresult == 1:
        dlg.MessageBox("Error: invalid POS Approval Password", "Error", 16)
        topout(screen)
        return
    if pwresult == 2:
        topout(screen)
        return (store, employee_name, employee)

    screen.Synchronous = False

def getdistreg(store, employee_name, employee_id):
    screen = crt.Screen
    dlg = crt.Dialog

    screen.Synchronous = True

    screen.Send("*MA050\r")
    wait(screen, "Loc#")
    screen.Send(store + "\r")
    wait(screen, "Cont")
    district = screen.Get(22, 33, 22, 35)
    region = screen.Get(21, 33, 21, 35)

    topout(screen,
            "Create a GC Stores Profile for AM\r" +
            "Name:        " + employee_name + "\r" +
            "Store:       " + store + "\r" +
            "District:    " + district + "\r" +
            "Region:      " + region + "\r" +
            "Employee ID: " + employee_id)

    screen.Synchronous = False

result = main()
if result:
    getdistreg(result[0], result[1], result[2])
