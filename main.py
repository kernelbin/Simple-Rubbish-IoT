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
    else:
        cv2.imshow("qwq", img)

socket_handler.close()
