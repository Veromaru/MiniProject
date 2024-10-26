import eel 
import time 
import plc2
import threading  # To allow tasks to run in the background

# Initialize Eel with the 'web' folder
eel.init('web')

# Flags to track if linda and palmcontrol are running
is_linda_running = False
is_palmcontrol_running = False

# Function to run linda voice assistant
@eel.expose
def say_hello_py():
    global is_linda_running
    
    if not is_linda_running:
        is_linda_running = True
        threading.Thread(target=run_linda, daemon=True).start()
    else:
        print("Linda is already running!")

def run_linda():
    import linda
    try:
        linda.run_linda_voice_assistant()
    finally:
        global is_linda_running
        is_linda_running = False  # Reset the flag when linda stops

# Function to run palmcontrol
@eel.expose
def notouch():
    global is_palmcontrol_running
    
    if not is_palmcontrol_running:
        is_palmcontrol_running = True
        threading.Thread(target=run_palmcontrol, daemon=True).start()
    else:
        print("Palm control is already running!")

def run_palmcontrol():
    try:
        plc2.hand_control()
    finally:
        global is_palmcontrol_running
        is_palmcontrol_running = False  # Reset the flag when palmcontrol stops

# Start Eel
eel.start('index.html', size=(1600, 900), block=True, icon='3378034.png')
