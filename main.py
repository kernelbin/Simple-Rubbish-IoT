from servo import Servo
try:
    import config
except:
    import config_default as config
import cv2
from image import detect_qrcode
from socket_handler import SocketHandler
import time
socket_handler = SocketHandler(config.BACKEND_HOST, config.BACKEND_PORT)


def func():
    socket_handler.send_login("嘤嘤嘤qwq")
    # socket_handler.close()


socket_handler.on_connected = func
socket_handler.start()

video = cv2.VideoCapture(0)
BASE = 100
OFFSET = 45
servo1 = Servo(config.SERVO1)
servo2 = Servo(config.SERVO2)
print("Reseting servo...")
servo1.rotate(BASE)
servo2.rotate(BASE)


def turn_to_left():
    servo1.rotate(BASE-OFFSET)
    servo2.rotate(BASE+OFFSET)
    import time
    time.sleep(4)
    servo1.rotate(BASE)
    servo2.rotate(BASE)


def turn_to_right():
    servo1.rotate(BASE+OFFSET)
    servo2.rotate(BASE-OFFSET)
    import time
    time.sleep(4)
    servo1.rotate(BASE)
    servo2.rotate(BASE)


last_time = 0
while True:
    # continue
    ret, frame = video.read()
    img, decode_result = detect_qrcode(frame)

    if cv2.waitKey(1) == ord('q'):
        break
    if img is None and decode_result:
        if time.time()-last_time < 20:
            continue
        last_time = time.time()
        # print("Got {}".format(decode_result.data.decode()))
        userid, bagtype = decode_result.data.decode().split(" ")
        print(userid, bagtype)
        # exit(0)
        if bagtype == "dry":
            turn_to_left()
        else:
            turn_to_right()
        import time
        # time.sleep(5)
    else:
        cv2.imshow("qwq", img)

socket_handler.close()
