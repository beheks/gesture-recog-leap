from CaptureFrame import CaptureFrame
import sys
import lib.Leap.Leap as Leap

def main():
    windowArg = ""
    if len(sys.argv) > 1:
        windowArg = sys.argv[1]
        
    # Create a listener and controller
    listener = CaptureFrame(windowArg)
    controller = Leap.Controller()

    # Have the listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    sys.stdin.readline()

    # Remove the listener when done
    controller.remove_listener(listener)

if __name__ == "__main__":
    main()
    
