## Toggle an LED when the GUI button is pressed ##
import time
import tk_tools
from tkinter import *
import tkinter.font
from tkinter import messagebox
from gpiozero import LED
import RPi.GPIO
RPi.GPIO.setmode(RPi.GPIO.BCM)
import random
from w1thermsensor import W1ThermSensor

### HARDWARE DEFINITIONS ###
env_sensor = W1ThermSensor()
led=LED(14)

### GUI DEFINITIONS ###
win = Tk()
win.attributes('-fullscreen', 1)
win.title("Thermowood")
myFont = tkinter.font.Font(family = 'Helvetica', size = 8, weight = "bold")

pump_led = tk_tools.Led(win, size=25)
pump_led.grid(row=2, column=2)
pump_label=Label(win, text="Pump",font=("Helvetica", 10), bg="yellow", fg="black")
pump_label.grid(row=2,column=1)

boiler_led = tk_tools.Led(win, size=25)
boiler_led.grid(row=1, column=2)
boiler_label=Label(win, text="Boiler",font=("Helvetica", 10), bg="yellow", fg="black")
boiler_label.grid(row=1,column=1)

ac_led = tk_tools.Led(win, size=25)
ac_led.grid(row=3, column=2)
ac_label=Label(win, text="A/C",font=("Helvetica", 10), bg="yellow", fg="black")
ac_label.grid(row=3,column=1)

date_label=Label(win, text="NULL",font=("Helvetica", 13), bg="green", fg="white")
date_label.grid(row=0,column=0)

main_temp = tk_tools.Gauge(win, max_value=250.0,
label='Temperature', unit=' °C', width=200, height=100,divisions=10,
 yellow=70, red=80, yellow_low=45, red_low=0,bg='lightgrey')
main_temp.grid(row=1,column=0)
#main_temp.set_value(100)

inlet = tk_tools.Gauge(win, max_value=130.0,
label='Inlet', unit=' Litre', width=200, height=100,divisions=20,
 yellow=60, red=90, yellow_low=0, red_low=0,bg='lightgrey')
inlet.grid(row=2,column=0)
#inlet.set_value(100)


env_temp = tk_tools.Gauge(win, max_value=60.0,label='Temperature', unit=' °C',
red=60, red_low=0)
env_temp.grid(row=3,column=0)

#env_temp.set_value(random.randint(1,50))

#env_humidity = tk_tools.Gauge(win, max_value=100.0,label='Humidity', unit=' %',
#red=75, red_low=0)
#env_humidity.grid()
#env_humidity.set_value(100)


### Event Functions ###
def ledToggle():
    if led.is_lit:
       # led.off()
        wood_type["text"]="Wood: SASNA Thickness: 5Cm" # Change only the button text property
    else:
        #led.on()
        ledButton["text"]="Wood: SASNA Thickness: 5Cm"

def close():
   if messagebox.askokcancel("Quit", "You want to quit now?"): 
       RPi.GPIO.cleanup()
       win.destroy()

def update_elements():
    main_temp.set_value(random.randint(1,50))
    inlet.set_value(100)
    env_temp.set_value(env_sensor.get_temperature())
    #env_humidity.set_value(80)
    now = time.strftime("%c")
    timestamp = time.strftime("%y%m%d%H%M%S")
    date_label.configure(text=now)
    win.after(100,update_elements)

### WIDGETS ###

# Button, triggers the connected command when it is pressed
wood_type = Button(win, text='Wood: SASNA Thickness: 5Cm', font=myFont, command=ledToggle, bg='bisque2', height=1, width=24)
wood_type.grid(row=4,column=0)

exitButton = Button(win, text='Exit', font=("Helvetica", 7), command=close, bg='red', height=1, width=2)
exitButton.grid(row=5, column=0)

win.protocol("WM_DELETE_WINDOW", close) # cleanup GPIO when user closes window
update_elements()
win.mainloop() # Loops forever

