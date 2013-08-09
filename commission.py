# $language = "python"
# $interface = "1.0"

import sys


"""
NOTES
Assumes all skus are in the same store
Must be on store server when running script

SKUS
- 10 digits long
- last 3 digits = store number

Topout
Log into store
topout
Send *IC200
Send Sku + enter

here's the tricky part
replace mode:
see if 22.1 is occupied
if it is, delete field
if not, send employee id
    if other ids present send 22.n for each id

add mode:
see if 22.1 is occupied
if it is, see if 22.2 is occupied
if it is, send C22
see if 22.3 is occupied
keep going until no slot is occupied, send employee number to the slot


"""

def topout(screen):
    screen.Send("TOP\rINFORM\r")
    screen.WaitForString("GCM>", 5)


def main():
    screen = crt.Screen
    dlg = crt.Dialog

    screen.Synchronous = True

    skuList_raw = dlg.Prompt("Enter SKUs to process \n (Separated by spaces or periods)", "Commission Update")
    if skuList_raw == "":
        return screen
    skuList = skuList_raw.replace(".", " ").split(" ")

    # Validate skus
    for sku in skuList:
        if len(sku) != 10 or not sku.isdigit():
            sys.exit("Invalid SKU entered (" + sku + ")... Exiting")

    employeeList_raw = dlg.Prompt("Enter employee ID's for commission", "Commsion Update")
    if employeeList_raw == "":
        return screen
    employeeList = employeeList_raw.replace(".", " ").split(" ")

    # Validate employee ids
    for eid in employeeList:
        if len(eid) != 6 or not eid.isdigit():
            sys.exit("Invalid employee ID (" + eid + ")... Exiting")

    # Either IDYES or IDNO
    replaceMode = dlg.MessageBox("Do you want to replace all existing users on SKUs? \n (Select 'No' to add users to SKU)", "Commission Update", BUTTON_YESNO)

    store = skuList[0][-3:]

    topout(screen)
    screen.Send("L" + store + "\r")

    for sku in skuList:
        topout(screen)
        screen.Send("*IC200\r")
        screen.WaitForString("Sku no")
        screen.Send(sku + "\r")

        if replaceMode == IDYES:
            # Go through all 22 spots, delete any that exist, add new eids

        else:
            # Go through all 22 spots, add to any blank ones.






    screen.Synchronous = False

    return screen


main()
