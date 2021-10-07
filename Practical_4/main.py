import busio
import digitalio
import board
import threading 
import time
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# adding button implementation
button_pin = 16 
modes = [1 , 5 , 10]
level = 0
period = modes[level]

# create the mcp object
mcp = MCP.MCP3008(spi, cs)



#print out neccessary columns and initiate button 
def setup():
    GPIO.setup(button_pin , GPIO.IN , pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button_pin , GPIO.FALLING , callback = increment_period , bouncetime = 200) 
    pass
#fetches all the variables used for testing 
def fetch_temp() :  
	print("Raw ADC Value: ", chan0.value)
	print("ADC Voltage for temp sens: " + str(temp_voltage) + "V")
	print("ADC voltage for LDR: " +str(LDR_voltage) + "V")
	print("Current Ambient Temperature is: " ,round(temp, 2), "C" )


#Creating counter that uses thread and prints based on period 
def sens_thread():

	global runtime

	period = modes[level]
	thread = threading.Timer(period, sens_thread)
	# threading being used to implement the timer
	thread.daemon = True
	# Daemon threads exit when the program does

	thread.start() # starts timer
	runtime = time.time() - startTime #time lapesed calculated
	printvalues() # invoke the print function to print the various sensor values
	pass

#function that prints values
def printvalues():
    # create an analog input channel on pin 1
    chan0 = AnalogIn(mcp, MCP.P1)
    #create an analog channel for pin 2
    chan1 = AnalogIn(mcp, MCP.P2) 




    #tidying up variables for printing
    temp_voltage = round(chan0.voltage,4)
    LDR_voltage = round(chan1.voltage,4)
    #defining temperature based on voltage
    temp = (chan0.voltage-(0.5))/(0.01)
    
    print('{:<1}{:<9}{:>7}{:>12}{:>1}{:>9}'.format(round(runtime,0) , "s" , str(temp_voltage), round(temp, 2) , "C" ,  str(LDR_voltage)))
    



#function that increments period 
def increment_period(self):
    global level
    global modes 
    if (level ==2):
        level = 0
    else:
        level = level +1
    print("Button pushed, new sample rate is: " + str(modes[level]) + "s" ) 
    pass 
    
    

if __name__ == "__main__":
    try:
        # Call setup function
        print ("Runtime    "+ "Temp Reading    "+ "Temp    " + "Light Reading" )
        setup()
        startTime = time.time()
        sens_thread() 
        while True:
            pass 
           
    except Exception as e:
        print(e)
        
    finally:
        GPIO.cleanup()





