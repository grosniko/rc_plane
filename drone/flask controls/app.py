from flask import Flask, render_template, Response, request
# from camera import CameraStream
# import cv2
from time import sleep
import pca
import esc

app = Flask(__name__)



# quality = 20
# buffersize = 1
# fps = 30

# cap = CameraStream(0, buffersize, fps)
# encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]

servos = pca.init()
throttle, min_throttle, max_throttle = esc.init()

@app.route('/')
def index():
    """Video streaming home page."""
    # cap.start()
    return render_template('index.html', min_throttle  = min_throttle, max_throttle = max_throttle)


# def gen_frame():
#     """Video streaming generator function."""
#     while cap:
#         frame = cap.read()
#         convert = cv2.imencode('.jpg', frame, encode_param)[1].tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # concate frame one by one and show result


# @app.route('/video_feed')
# def video_feed():

#     return Response(gen_frame(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/move_servo', methods=['GET', 'POST'])
def move_servo():

    params = request.get_json()
    print(params)
    angle = int(params["angle"])
    if "aileron" in params["servo_name"]:
        
        if "right" in params["servo_name"]:
            opposite_aileron = "left_aileron"
        else:
            opposite_aileron = "right_aileron"

        servos[params["servo_name"]].angle = angle
        servos[opposite_aileron].angle = 180 - angle
           
    else:
        servos[params["servo_name"]].angle = angle
    return {"msg": "OK"}


@app.route('/throttle_control', methods=['GET', 'POST'])
def throttle_control():

    params = request.get_json()
    print(params)
    button = params["button"]
    variation = params["variation"]

    if button == "on":
        esc.arm(throttle)
        pulse = min_throttle
    elif button == "off":
        esc.stop(throttle)
        pulse = 0
    else :
        pulse = esc.change_pulse(throttle, variation)

    return {"msg": "OK", "pulse": pulse}

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
