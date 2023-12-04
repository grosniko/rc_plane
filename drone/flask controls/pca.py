from adafruit_servokit import ServoKit

def init(cam=7, elev=12, rud=13, la=14, ra=15, pulse_min = 500, pulse_max = 2500, channels=16):
    pca = ServoKit(channels=channels)
    left_aileron = pca.servo[la]
    right_aileron = pca.servo[ra]
    rudder = pca.servo[rud]
    elevator = pca.servo[elev]
    camera = pca.servo[cam]

    servos = [left_aileron, right_aileron, rudder, elevator, camera]

    for servo in servos:
            servo.set_pulse_width_range(pulse_min, pulse_max)

    servo_obj = {

        "left_aileron": left_aileron,
        "right_aileron": right_aileron,
        "rudder": rudder,
        "elevator": elevator,
        "camera": camera
    }

    return servo_obj
