from servo import Servo
try:
    import config
except:
    import config_default as config
import cv2
from image import detect_qrcode
from socket_handler import SocketHandler
import time
import json
import util
socket_handler = SocketHandler(config.BACKEND_HOST, config.BACKEND_PORT)


def func():
    socket_handler.send_login(config.CLIENT_UUID)
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
        if time.time()-last_time < 10:
            continue
        last_time = time.time()
        # print("Got {}".format(decode_result.data.decode()))
        try:
            userid, bagtype = decode_result.data.decode().split(" ")
        except Exception as ex:
            print("Bad QR Code")
            continue
        print(userid, bagtype)
        # exit(0)
        ret = json.JSONDecoder().decode(util.send_http_request(
            config.WEB_URL+"/api/packet/process", {"userid": userid, "type": bagtype, "uuid": config.CLIENT_UUID}))
        if ret["code"]:
            print("Not allowed..")
            print(ret["message"])
            continue
        if bagtype == "dry":
            turn_to_left()
        else:
            turn_to_right()
        socket_handler.send_process_success(userid, ret["process_id"], bagtype)

        # import time
        # time.sleep(5)
    else:
        cv2.imshow("qwq", img)

socket_handler.close()
