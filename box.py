#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep, gmtime, strftime
import picamera
import circuits

led1_pin = 37 # LED 1
led2_pin = 15 # LED 2
led3_pin = 38 # LED 3
led4_pin = 33 # LED 4
button1_pin = 16 # pin for the big red button
button2_pin = 35 # pin for button to shutdown the pi
button3_pin = 36 # pin for button to end the program, but not shutdown the pi

def setupGPIOs():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led1_pin, GPIO.OUT) # LED 1
    GPIO.setup(led2_pin, GPIO.OUT) # LED 2
    GPIO.setup(led3_pin, GPIO.OUT) # LED 3
    GPIO.setup(led4_pin, GPIO.OUT) # LED 4

    GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button1_pin, GPIO.RISING)
    GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class Application():
    def __init__(self):
        setupGPIOs()
        self.setup_camera()
        self.camera.start_preview()
        self.counter = 0

    def setup_camera(self):
        self.camera = picamera.PiCamera()
        self.camera.framerate = 24
        self.camera.vflip = True
        self.camera.hflip = False
        self.camera.rotation = 270

    def cleanup(self):
        GPIO.cleanup()

    def run(self):
        try:
            while True:
                sleep(2)
                self.handle_events()
        except KeyboardInterrupt:
            self.cleanup()       # clean up GPIO on CTRL+C exit
        self.cleanup()       # clean up GPIO on CTRL+C exit

    def handle_events(self):
        self.on_button_1()

    def make_photo(self, file_path):
        self.camera.stop_preview()
        original_resoulution = self.camera.resolution
        original_rotation = self.camera.rotation
        original_vflip = self.camera.vflip
        original_hflip = self.camera.hflip
        self.camera.vflip = False
        self.camera.hflip = False
        self.camera.rotation = 0
        self.camera.resolution = (3280, 2464)
        self.camera.capture(file_path)
        self.camera.rotation = original_rotation
        self.camera.resolution = original_resoulution
        self.camera.vflip = original_vflip
        self.camera.hflip = original_hflip
        self.camera.start_preview()

    def on_button_1(self):
        if self.button_1_was_down():
            self.counter = self.counter + 1
            print "Button 1 Pressed " + str(self.counter)
            self.make_photo("/home/pi/image_{}.jpg".format(strftime("%Y-%m-%d-%H:%M:%S", gmtime())))

    def button_1_was_down(self):
        return GPIO.event_detected(button1_pin)


app = Application()
app.run()
