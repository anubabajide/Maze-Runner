import RPi.GPIO as GPIO
import time
import sys, tty, termios
from gpiozero import DistanceSensor
import random

GPIO.setmode(GPIO.BCM)

try:
        input_list = [20,26,6]
        output_list = [3,2,17,4,21,19,13,18,23]

        for i in input_list: GPIO.setup(i, GPIO.IN)
        for i in output_list: GPIO.setup(i, GPIO.OUT)

        NUM_CYCLES=10

        right_motor_pve = 3
        right_motor_nve = 2
        left_motor_pve = 17
        left_motor_nve = 4
        right_enable = 18
        left_enable = 23
        front_sensor_echo = 20
        front_sensor_trigger = 21
        #back_sensor_echo = 19
        #back_sensor_trigger = 26
        right_sensor_echo = 26
        right_sensor_trigger = 19
        left_sensor_echo = 6
        left_sensor_trigger = 13
        #colorsensor_s0 = 25
        #colorsensor_s1 = 8
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
        #back_ultrasonic = DistanceSensor(back_sensor_echo, back_sensor_trigger)

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

        def move_forward():
		print('moving forward')
                GPIO.output(right_enable, True)
                GPIO.output(left_enable, True)
                GPIO.output(right_motor_pve, True)
                GPIO.output(left_motor_pve, True)
                GPIO.output(right_motor_nve, False)
                GPIO.output(left_motor_nve, False)

        def move_backward():
		print('moving backward')
                GPIO.output(right_enable, True)
                GPIO.output(left_enable, True)
                GPIO.output(right_motor_pve, False)
                GPIO.output(left_motor_pve, False)
                GPIO.output(right_motor_nve, True)
                GPIO.output(left_motor_nve, True)

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

        def stop():
		print('stop')
                GPIO.output(right_motor_pve, False)
                GPIO.output(left_motor_pve, False)
                GPIO.output(right_motor_nve, False)
                GPIO.output(left_motor_nve, False)

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
        
        track = []
	current_checkpoint = None
	track_direction = []
	reverse = False
	while True:
		right_sensor = int(right_ultrasonic.distance > 0.25)
		left_sensor = int(left_ultrasonic.distance > 0.25)
		middle_sensor = int(front_ultrasonic.distance > 0.15)

		print('right_sensor = {}, left_sensor = {}, middle_sensor = {}'.format(right_sensor, left_sensor, middle_sensor))
		if right_sensor == 1 or left_sensor == 1:
			check_points = {}
                        if right_sensor == 1:
                                check_points['r'] = 0

                        if left_sensor == 1:
                                check_points['l'] = 0

                        if len(check_points) > 0:
                                track.append(check_points)
                                track_direction.append(None)
                                current_checkpoint = len(track) - 1
                                print('setting checkpoint')

                        if right_sensor == 1:
                                check_points['r'] = 0

                        if left_sensor == 1:
                                check_points['l'] = 0

                        if len(check_points) > 0:
                                track.append(check_points)
                                track_direction.append(None)
                                current_checkpoint = len(track) - 1
                                print('setting checkpoint')

			if reverse and current_checkpoint != None:
				last_direction = track_direction[current_checkpoint]
				if last_direction == 'r':
					move_left()

				else:
					move_right()
				reverse = False

		if reverse or (right_sensor == left_sensor == middle_sensor == 0):
			reverse = True
			move_backward()

		elif current_checkpoint != None:
			check_point = track[current_checkpoint]
			available_paths = [x for x in check_point if check_point[x] == 0]
			if len(available_paths) > 0:
				if 'r' in available_paths:
					path = 'r'
				else:
					path = available_paths[random.randint(0, len(available_paths)-1)]
				track[current_checkpoint][path] = 1
				track_direction[current_checkpoint] = path
				if path == 'r':
					move_right()

				else:
					move_left()

			move_forward()

		elif right_sensor == 0 and left_sensor == 0:
			move_forward()


except KeyboardInterrupt:
        GPIO.cleanup()

