import servo_motors
import esc

servos = servo_motors.init()

pi, mn, mx = esc.init()

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
port = 12345

server_socket.bind((host,port))

server_socket.listen(1)

print("Ready")

while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode()
        print("connected", addr)
        power = 0
        if data:
            if "-" in data:
                mvmt = data.split("-")[0]
                angle = int(data.split("-")[1])
                power = int(data.split("-")[2])

                if mvmt == "roll":
                    servos["left_aileron"].angle = angle
                    servos["right_aileron"].angle = angle
                    servos["rudder"].angle = angle
                if mvmt == "yaw":
                    servos["elevator"].angle = angle
                if mvmt == "cam_x":
                    servos["cam_x"].angle = angle
                if mvmt == "cam_y":
                    servos["cam_y"].angle = angle

                client_socket.send((mvmt + "-" + str(angle) + "-" + str(power)).encode())
        
        pi.set_servo_pulsewidth(4, power)
        client_socket.close()