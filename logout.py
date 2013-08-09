#$language = "python"
#$interface = "1.0"

def main():
    screen = crt.Screen
    screen.Synchronous = True

    screen.Send("TOP\rINFORM\r")
    screen.WaitForString("GCM>")
    screen.Send("L000\r")
    screen.WaitForCursor()
    screen.Send("\r\r\rTOP\rINFORM\r")
    
    screen.Synchronous = False

main()
