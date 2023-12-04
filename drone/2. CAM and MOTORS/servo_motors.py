from adafruit_servokit import ServoKit

def init(cam_x=0, cam_y=1, elev=12, rud=13, la=14, ra=15, pulse_min = 500, pulse_max = 2500, channels=16):
    pca = ServoKit(channels=channels)
    left_aileron = pca.servo[la]
    right_aileron = pca.servo[ra]
    rudder = pca.servo[rud]
    elevator = pca.servo[elev]
    cam_x = pca.servo[cam_x]
    cam_y = pca.servo[cam_y]

    servos = [left_aileron, right_aileron, rudder, elevator, cam_x, cam_y]

    for servo in servos:
            servo.set_pulse_width_range(pulse_min, pulse_max)

    servo_obj = {

        "left_aileron": left_aileron,
        "right_aileron": right_aileron,
        "rudder": rudder,
        "elevator": elevator,
        "cam_x": cam_x,
        "cam_y": cam_y
    }

    return servo_obj