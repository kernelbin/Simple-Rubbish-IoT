import RPi.GPIO as GPIO


class Servo:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.gpio = GPIO.PWM(pin, 50)
        self.gpio.start(90)

    def rotate(self, deg):
        duty = deg/180*2.5/20*100
        # print(duty)
        self.gpio.ChangeDutyCycle(duty)

    def __del__(self):
        self.gpio.stop()
        GPIO.cleanup()
