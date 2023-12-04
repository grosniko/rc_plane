# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?
# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient


import pigpio #importing GPIO library



def init(ESC=4, max_value=2000, min_value = 700):
    #Connect the ESC in this GPIO pin, 4 by default
    #min/max value set for 1400KV motor

    pi = pigpio.pi();
    pi.set_servo_pulsewidth(ESC, 0)


    print("For first time launch, invoke esc.options() and type calibrate")

    return pi, min_value, max_value

def manual_drive(pi, ESC=4): #You will use this function to program your ESC if required
    print("You have selected manual option so give a value between 0 and you max value")
    while True:
        inp = input()
        if inp == "stop":
            stop(pi)
            break
        elif inp == "control":
            control(pi)
            break
        elif inp == "arm":
            arm(pi, control=True)
            break
        else:
            pi.set_servo_pulsewidth(ESC,inp)

def change_pulse(pi, pulse_variation, ESC=4, max_value = 2000, min_value = 700):
    pulse = pi.get_servo_pulsewidth(ESC)
    pulse = pulse + pulse_variation
    if pulse > max_value:
        pi.set_servo_pulsewidth(ESC, max_value)
    elif pulse < min_value:
        pi.set_servo_pulsewidth(ESC, min_value)
    else:
        pi.set_servo_pulsewidth(ESC, pulse)

    print("Throttle: ", pulse, " | Max: ", max_value, " Min: ", min_value)
    return pulse



def calibrate(pi, ESC=4, max_value=2100, min_value = 1000):   #This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will hear two beeps, then wait for a gradual rising tone then press Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, min_value)
            print("Weird eh! Special tone")
            time.sleep(7)
            print("Wait for it ....")
            time.sleep (5)
            print("Im working on it, DONT WORRY JUST WAIT.....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print("Arming ESC now...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print("See.... uhhhhh")
            control(pi) # You can change this to any other function you want


def control(pi, ESC=4):
    print("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
    time.sleep(1)
    speed = 700    # change your speed if you want to.... it should be between 700 - 2000
    print("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()

        if inp == "q":
            speed -= 100    # decrementing the speed like hell
            print("speed = %d" % speed)
        elif inp == "e":
            speed += 100    # incrementing the speed like hell
            print("speed = %d" % speed)
        elif inp == "d":
            speed += 10     # incrementing the speed
            print("speed = %d" % speed)
        elif inp == "a":
            speed -= 10     # decrementing the speed
            print("speed = %d" % speed)
        elif inp == "stop":
            stop(pi)          #going for the stop function
            break
        elif inp == "manual":
            manual_drive(pi)
            break
        elif inp == "arm":
            arm(pi, control=True)
            break
        else:
            print("WHAT DID I SAID!! Press a,q,d or e")

def arm(pi, ESC=4, max_value=2000, min_value = 700, control=False): #This is the arming procedure of an ESC
    pi.set_servo_pulsewidth(ESC, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, max_value)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, min_value)
    time.sleep(1)
    if control:
        control(pi)
    else:
        pi.set_servo_pulsewidth(ESC, min_value)

def stop(pi, ESC=4): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

def options(ESC = 4, max_value=2000, min_value = 700):
    print("Type the exact word for the function you want")
    print("calibrate OR manual OR control OR arm OR stop")
    pi = init(ESC=ESC, max_value=max_value, min_value = min_value)
    #This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.
    inp = input()
    if inp == "manual":
        manual_drive(pi)
    elif inp == "calibrate":
        calibrate(pi)
    elif inp == "arm":
        arm(pi, control=True)
    elif inp == "control":
        control(pi)
    elif inp == "stop":
        stop(pi)
    else :
        print("Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!")
