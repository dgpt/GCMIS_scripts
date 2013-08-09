#$language = "python"
#$interface = "1.0"

def main():
    screen = crt.Screen
    dlg = crt.Dialog

    screen.Synchronous = True

    exceptionList = []
    sessionList = []
    errorList = []

    store = dlg.Prompt('Enter store number', 'Store Number')
# TODO: Better input checking here
    if store.isdigit() == False or store == '':
        return screen

# Get exceptions from user

    userInput = dlg.Prompt('Please enter sessions to ignore. Enter 0 to clear all logged in sessions.', 'Exceptions')
    if userInput == '':
        return screen
    userInput = userInput.replace('.', ' ')
    exceptionList = userInput.split(' ')

    # Make sure all tabs are there before trying to activate relevant tab
    if crt.GetTabCount() == 9:
        tabNum = int(str(store)[0], 10)
        scriptTab = crt.GetScriptTab().Index
        # tab numbers need to be adjusted according to normal setup
        if tabNum < 6:
            tabNum += 1
        # Change tab, screen to tab of store selected if selected store is on different server
        if tabNum != scriptTab:
            currentTab = crt.GetTab(tabNum)
            currentTab.Activate()
            screen = currentTab.Screen
    screen.Send('TOP\rINFORM\r')
    screen.WaitForString('GCM>')
    screen.Send('info.us -l ' + store + '\r')
    r = screen.WaitForStrings(['(CR)', 'GCM>'], 10)
    if r == 2:
        return screen

# Gathering Loop

    colMin = 54     # should be at start of session id
    colMax = 57     # should be at end of session id
    row = 3         # start at row 3
    finished = False
    while not finished:
        get = screen.Get(row, colMin, row, colMax)
        if get.strip() not in exceptionList:
            if get.isspace():
                screen.Send('\r')
                r = screen.WaitForStrings(['(CR) to continue', 'GCM>'], 10)
                if r == 1:
                    row = 3
                elif r == 2:
                    finished = True
            sessionList.append(get.strip())
        row += 1

# Master Off Loop

    screen.Send('TOP\rINFORM\r')
    for session in sessionList:
        if session == '':
            continue
        screen.Send('MASTER OFF ' + session)
        screen.WaitForString('MASTER OFF ' + session)   # must wait for the Send before returning, otherwise the sResult goes before the MASTER OFF
        screen.Send('\r')
        sResult = screen.WaitForStrings(['(CR)', 'ERR', 'GCM>'], 1)
        if sResult == 1:
            screen.Send('\rY\rY\r')
            screen.WaitForString('GCM>')
        if sResult == 2:
            errorList.append(session)
            continue


    screen.Send('TOP\rINFORM\r')
    if len(errorList) > 0:
        screen.Send('Errors occurred with the following sessions:\r')
        screen.Send(', '.join(errorList) + '\r')

    screen.Synchronous = False
    return screen

main().Send('TOP\rINFORM\r')
