#$language = "python"
#$interface = "1.0"

"""
Cycles through every store and turns Sales Ticket Recovery Mode off for each store.

Servers must be loaded in SecureCRT in the following order:
    DRUM, BASS, ROCK, GUITAR, MUSIC, CYMBAL, JAZZ, PIANO, and LUTE
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

# Make sure all tabs are loaded (exit if not)
    if crt.GetTabCount() != 9:
        topout(screen, "You must have all servers loaded to run this script.\r
                        DRUM, BASS, ROCK, GUITAR, MUSIC, CYMBAL, JAZZ, PIANO, and LUTE (in that order).")
        return

    startTab = 2
    endTab = 8

# Do some lazy order checking to make sure tabs are in the right order
    if crt.GetTab(startTab).Caption != "BASS" or crt.GetTab(endTab).Caption != "PIANO":
        topout(screen, "You must have all servers loaded to run this script.\r
                        DRUM, BASS, ROCK, GUITAR, MUSIC, CYMBAL, JAZZ, PIANO, and LUTE (in that order).")
        return

# Loop through tabs BASS to PIANO

# topout to INFORM

# Send TOP to get to main menu

# Send 13, 5, 9 to get to GC453 menu

# Send MANUAL.MODE to activate STRM

# Loop i in 2.i until the selection is blank (no store under cursor)
# Check selection black by screen.Get(screen.CurrentRow, screen.CurrentColumn, screen.CurrentRow + 2, screen.CurrentColumn)


main()
