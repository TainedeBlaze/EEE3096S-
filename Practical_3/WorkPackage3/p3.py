# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import operator 
import time 
# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
user_guess = 0
num_of_guesses= 0 
# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    global value
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
    	os.system('clear')
    	print("Starting a new round!")
    	print("Use the buttons on the Pi to make and submit your guess!")
    	print("Press and hold the guess button to cancel your game")
    	value = generate_number()
    	PWM_LED.start(0)
    	PWM_Buzzer.start(50) 

    	while not end_of_game:
    		continue 

    	PWM_LED.stop() 
    	PWM_Buzzer.stop() 
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
	print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
	#loop through the scores and print them out 
	for i in raw_data:
		print( i + " : "+ str(raw_data[i]) ) 
 
    


# Setup Pins
def setup():
    # Setup board mode
	GPIO.setmode(GPIO.BOARD) 
    # Setup regular GPIO
	 
	 
	GPIO.setup(11, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)
	GPIO.setup(15 , GPIO.OUT)
	GPIO.setup(5 ,GPIO.OUT) 
	GPIO.setup(3 , GPIO.OUT) 
	GPIO.setup(LED_accuracy , GPIO.OUT)
	GPIO.setup(buzzer, GPIO.OUT)
	#GPIO.output(LED_accuracy , 1) 
    # Setup PWM channels
	for value in LED_value: 
		#pwm for the guess LEDs
		GPIO.output(value , 0) 
		#pi_pwm.start(100)
	#must be greater than 0 when started

	#need to be global so can be mentioned outside class
	global PWM_Buzzer
	global PWM_LED 
	 
	PWM_LED = GPIO.PWM(LED_accuracy ,100)
	PWM_LED.start(80)
	PWM_Buzzer = GPIO.PWM(buzzer, 100) 
        
  
    # Setup debouncing and callbacks
	GPIO.setup(btn_submit , GPIO.IN , pull_up_down =GPIO.PUD_UP)
	GPIO.setup(btn_increase , GPIO.IN , pull_up_down = GPIO.PUD_UP) 
	#add events 
	GPIO.add_event_detect(btn_submit , edge = GPIO.RISING , callback=btn_guess_pressed  , bouncetime =200) 
	GPIO.add_event_detect(btn_increase, edge = GPIO.RISING , callback=btn_increase_pressed  ,bouncetime = 200)  
	


# Load high scores
def fetch_scores():
    # get however many scores there are
	score_count = chr(eeprom.read_byte(0))  
    # Get the scores
	#Using dictionary with key as name and score as the value 
	score_dict = {}
    # convert the codes back to ascii
	for score in range (int(score_count)): 
		score_list =eeprom.readblock(score +1 , 4)
	#adding the now read data to the dictionary  
		score_dict[str(chr(score_list[0]))+str(chr(score_list[1]))+str(chr(scorelist[2]))]=int(chr(score_list[3])) 
    # return back the results
	return score_count, scores


# Save high scores
def save_scores(score_dict):
    # fetch scores
	counter = 0 
	
	#organize score in descending order 
	sorted_d = dict(sorted(score_dict.items() , key = operator.itemgetter(1), reverse = True))
	#loop through the scores and write them all to memory 
	for key in sorted_d:
		i=i+1
		eeprom.write_block(i, [(key[0]),ord(key[1]),ord(key[2]),ord(str(sorted_d[key]))])
    # include new score
	eeprom.write_byte(0, ord(str(len(score_dict))))
	print("Written")
    # sort btn_increase_pressed
    # update total amount of scores
    # write new scores
    


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
	global user_guess
	print("Button for increasing score is pressed")

	if(user_guess<7):
		user_guess = user_guess +1 

	else:
		user_guess = 0
	#invokes function that displays guess 
	LED_Score(user_guess)
	print("Current guess is: " + str(user_guess))  
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
	

def  LED_Score(number): 
	#first convert guess to binary number 
	bin_number = bin(number).replace("0b" , "") 
	#will use length of binary guess to determine score 
	if(len(bin_number)==1):
		GPIO.output(LED_value[0],int(bin_number))
		GPIO.output(LED_value[1],0)
		GPIO.output(LED_value[2],0)

	#if binarry is length 2 then adjust lights
	elif(len(bin_number)==2):
		GPIO.output(LED_value[0],int(bin_number[1]))
		GPIO.output(LED_value[1],int(bin_number[0]))
		GPIO.output(LED_value[2],0)


	#if binarry is length 3 then adjust lights
	else:
		GPIO.output(LED_value[0],int(bin_number[2]))
		GPIO.output(LED_value[1],int(bin_number[1]))
		GPIO.output(LED_value[2],int(bin_number[0]))

def exact_guess():
	global no_of_guesses
	#Disable the PWM LED and the Buzzer
	PWM_LED.stop()
	PWM_Buzzer.stop()
	
	#Prompt the user to enter a name
	print("You have guessed the correct answer in ",num_of_guesses," attempts")
	name=input("Enter your 3 letter nickname: ")
	#assuming the aser must input a name of 3 letters only- while loops repeats until this is done.
	while(len(name)!=3):
		print("Name Must be 3 letter")
		name=input("Enter your 3 letter nickname: ")
	#initializing dictionary that will be sttored to null
	score_dict={}		
	#if the EEprom has no highscores then :
	if(int(chr(eeprom.read_byte(0)))==0):
		#store user answer and name in local dictionary
		score_dict[name]=num_of_guesses
		#Saves the dictionary back in the eeprom
		save_scores(score_dict)
	# else if the eeprom has less than 3 value - i.e 1 or 2 values
	elif(int(chr(eeprom.read_byte(0)))<3):
		
		score_dict=fetch_scores()
		
		score_dict[name]=num_of_guesses
		#Saves the dictionary back in the eeprom
		save_scores(score_dict)
	#else the eeprom already has 3 highscores, thus must remove the largest highscore if it is bigger than
	#users answer and replace
	else:
		#fetching scores and storing in local dictionary
		score_dict=fetch_scores()
		#finding the key(name) with the maximum value (highscore)
		max_key=max(score_dict,key=score_dict.get)
		# if users guess fits in top 3 then add it and replace the smallest
		if(score_dict[max_key]>num_of_guesses):
			#delete the biggest value
			del score_dict[max_key]		
			#Saves the dictionary back in the eeprom
			score_dict[name]=num_of_guesses
			print("You are in the top 3")
			#only change data in eeprom if user is in top3
			save_scores(score_dict)
			
		else:
			print("Try again to be in the top 3")



# Guess button
def btn_guess_pressed(channel):
	global end_of_game 
	global num_of_guesses
	num_of_guesses= num_of_guesses +1 

	start_time = time.time() 
	while GPIO.input(channel) ==0: 
		pass 

	presstime = time.time() - start_time 

	if presstime > 1: 
		PWM_LED.ChangeFrequency(100)
		PWM_LED.stop()
		PWM_Buzzer.stop() 
		end_of_game = True 

	else: 
		#check if exact guess is met and end game 
		if(value==user_guess): 
			exact_guess() 
			end_of_game=True 

		else:	 
		#trigger the events for the accuracy and buzzer based on guess 
			trigger_buzzer()

			accuracy_leds()
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
   


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
	if ((user_guess > value) or (value ==0)):
		PWM_LED.ChangeDutyCycle(((8-user_guess)/(8-value))*100) 

	else: 
		PWM_LED.ChangeDutyCycle((user_guess/value)*100)    # - The % brightness should be directly proportional to the % "closeness"
	#if((value ==0) or user_guess > value)): 


# Sound Buzzer
def trigger_buzzer():

    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
	if(abs(user_guess - value) == 3):
		PWM_Buzzer.ChangeFrequency(1) 
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
	if(abs(user_guess - value) == 2):
		PWM_Buzzer.ChangeFrequency(2)

    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
	if(abs(user_guess - value) == 1):
		PWM_Buzzer.ChangeFrequency(4)



if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass 
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
