try:
    import config

except:
    import config_default as config
import cv2
from image import detect_qrcode
from socket_handler import SocketHandler

socket_handler = SocketHandler(config.BACKEND_HOST, config.BACKEND_PORT)


def func():
    pass


socket_handler.on_connected = func
socket_handler.start()

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    img, decode_result = detect_qrcode(frame)
    if img is not None:
        print("Got %s".format(decode_result.data.decode()))
        import time
        time.sleep(5)
