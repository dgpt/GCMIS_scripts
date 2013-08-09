#$language = "python"
#$interface = "1.0"

def main():
    screen = crt.Screen
    dlg = crt.Dialog

    screen.Synchronous = True

    store = dlg.Prompt('Enter store number', 'Store Number')
# TODO: Better input checking here
    if store.isdigit() == False or store == '':
        return

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

    screen.Synchronous = False

main()
