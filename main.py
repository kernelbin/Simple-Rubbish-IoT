try:
    import config

except:
    import config_default as config
import cv2
from image import detect_qrcode
from socket_handler import SocketHandler

socket_handler = SocketHandler(config.BACKEND_HOST, config.BACKEND_PORT)


def func():
    socket_handler.send_login("嘤嘤嘤qwq")
    # socket_handler.close()


socket_handler.on_connected = func
socket_handler.start()

video = cv2.VideoCapture(0)
BASE = 110
from servo import Servo
servo1 = Servo(config.SERVO1)
servo2 = Servo(config.SERVO2)
print("Reseting servo...")
servo1.rotate(BASE)
servo2.rotate(BASE)


def turn_to_left():
    servo1.rotate(BASE-50)
    servo2.rotate(BASE+50)
    import time
    time.sleep(4)
    servo1.rotate(BASE)
    servo2.rotate(BASE)


def turn_to_right():
    servo1.rotate(BASE+50)
    servo2.rotate(BASE-50)
    import time
    time.sleep(4)
    servo1.rotate(BASE)
    servo2.rotate(BASE)


while True:
    # continue
    ret, frame = video.read()
    img, decode_result = detect_qrcode(frame)

    if cv2.waitKey(1) == ord('q'):
        break
    if img is None and decode_result:
        # print("Got {}".format(decode_result.data.decode()))
        userid, bagtype = decode_result.data.decode().split(" ")
        print(userid, bagtype)
        # exit(0)
        if bagtype == "dry":
            turn_to_left()
        else:
            turn_to_right()
    else:
        cv2.imshow("qwq", img)

socket_handler.close()
