#libraries are imported to support the raspberry pi pin synchronisation0
import RPi.GPIO as GPIO 
import time 
import sys, tty, termios
from gpiozero import DistanceSensor #this is used for the ultrasonic sensor
import random

#the numbering mode is set to BCM instead og BOARD
GPIO.setmode(GPIO.BCM)

#a try break statement is included to break the code from its running point whenever the 'ctrl' + 'x' key is pressed
try:
	#input and outputt pins are set
        input_list = [20,26,6]
        output_list = [3,2,17,4,21,19,13,18,23]

        for i in input_list: GPIO.setup(i, GPIO.IN)
        for i in output_list: GPIO.setup(i, GPIO.OUT)

        NUM_CYCLES=10
	
	#the pin numbers are assigned to letters for ease 
        right_motor_pve = 3
        right_motor_nve = 2
        left_motor_pve = 17
        left_motor_nve = 4
        right_enable = 18
        left_enable = 23
        front_sensor_echo = 20
        front_sensor_trigger = 21
        back_sensor_echo = 19
        back_sensor_trigger = 26
        right_sensor_echo = 26
        right_sensor_trigger = 19
        left_sensor_echo = 6
        left_sensor_trigger = 13
        colorsensor_s0 = 25
        colorsensor_s1 = 8
        s2 = 16
        s3 = 12
        out = 25
        signal=25


        GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)

	front_ultrasonic = DistanceSensor(front_sensor_echo, front_sensor_trigger)
        right_ultrasonic = DistanceSensor(right_sensor_echo, right_sensor_trigger)
        left_ultrasonic = DistanceSensor(left_sensor_echo, left_sensor_trigger)
        
	#this allows the color sensor to shoot out certain rays and capture the incident light to determine the color that is seen.
	#different colors can be determined using their RGB code (red, green, blue and black are used in this instance)
	def loop():
	        temp=1
        	GPIO.output(s2, GPIO.LOW)
       		GPIO.output(s3, GPIO.LOW)
                time.sleep(0.3)
                start=time.time()
                for impulse_count in range(NUM_CYCLES):
                        GPIO.wait_for_edge(signal, GPIO.FALLING)
                duration- time.time() - start
                red = NUM_CYCLES/duration

                GPIO.output(s2, GPIO.LOW)
                GPIO.output(s3, GPIO.HIGH)
                time.sleep(0.3)
                start=time.time()
                for impulse_count in range(NUM_CYCLES):
                        GPIO.wait_for_edge(signal, GPIO.FALLING)
                duration- time.time() - start
                blue = NUM_CYCLES/duration

                GPIO.output(s2, GPIO.HIGH)
                GPIO.output(s3, GPIO.HIGH)
                time.sleep(0.3)
                start=time.time()
                for impulse_count in range(NUM_CYCLES):
                        GPIO.wait_for_edge(signal, GPIO.FALLING)
                duration- time.time() - start
                green = NUM_CYCLES/duration

                if green<7000 and blue<7000 and  red>12000:
                        print("red")
                        move_left()
                        time.sleep(1.2)

                elif green<7000 and blue>12000 and  red<7000:
                        print("blue")
                        move_right()
                        time.sleep(1.2)

                elif green>12000 and blue<7000 and  red<7000:
			print("green")
                        move_right()
                        time.sleep(1.2)

                elif green<5000 and blue<5000 and  red<5000:
                        print("Black")
                        move_backward()
                        time.sleep(0.5)

	#the conditions for forward movement are defined in this function
        def move_forward():
		print('moving forward')
                GPIO.output(right_enable, True)
                GPIO.output(left_enable, True)
                GPIO.output(right_motor_pve, True)
                GPIO.output(left_motor_pve, True)
                GPIO.output(right_motor_nve, False)
                GPIO.output(left_motor_nve, False)
		
	#the conditions for backward movement are defined in this function
        def move_backward():
		print('moving backward')
                GPIO.output(right_enable, True)
                GPIO.output(left_enable, True)
                GPIO.output(right_motor_pve, False)
                GPIO.output(left_motor_pve, False)
                GPIO.output(right_motor_nve, True)
                GPIO.output(left_motor_nve, True)

	#the conditions for turning 90 degrees to the left are defined in this function
        def move_left():
                print('moving left')
		if front_ultrasonic == 0:
			move_backward()
			time.sleep(0.2)
		GPIO.output(right_enable, True)
                GPIO.output(left_enable, True)
                GPIO.output(right_motor_pve, True)
                GPIO.output(left_motor_pve, False)
                GPIO.output(right_motor_nve, False)
                GPIO.output(left_motor_nve, True)
		time.sleep(0.8)
	
	#the conditions for turning 90 degrees to the right are defined in this function
        def move_right():
		print('moving right')
		if front_ultrasonic == 0:
			move_backward()
			time.sleep(0.2)
                GPIO.output(right_enable, True)
                GPIO.output(left_enable, True)
                GPIO.output(right_motor_pve, False)
                GPIO.output(left_motor_pve, True)
                GPIO.output(right_motor_nve, True)
                GPIO.output(left_motor_nve, False)
		time.sleep(0.8)
	
	#the conditions for stopping the robot are defined in this function
        def stop():
		print('stop')
                GPIO.output(right_motor_pve, False)
                GPIO.output(left_motor_pve, False)
                GPIO.output(right_motor_nve, False)
                GPIO.output(left_motor_nve, False)

	#this allows the ultrasonic sensor to shoot ultrasonic waves for a very short period of time and get a response
	#based on the time taken to get a response, an approximate value of distance is calculated
        def distance():
                GPIO.output(right_sensor_trigger, True)
                time.sleep(0.00001)
                GPIO.output(right_sensor_trigger, False)
                while GPIO.input(right_sensor_echo) == False:
                        pulse_start = time.time()
                while GPIO.input(right_sensor_echo) == True:
                        pulse_end = time.time()
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
                distance = round(distance, 2)
                return distance
        
	#this prints the value of the right, left and forward sensors to the screen respectively
	while True:
		right_sensor = int(right_ultrasonic.distance > 0.25)
		left_sensor = int(left_ultrasonic.distance > 0.25)
		forward_sensor = int(front_ultrasonic.distance > 0.15)

		print('right_sensor = {}, left_sensor = {}, middle_sensor = {}'.format(right_sensor, left_sensor, forward_sensor))



except KeyboardInterrupt:
        GPIO.cleanup()

