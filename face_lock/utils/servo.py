import time
import pigpio


class ServoController:
    
    def __init__(self, gpio):
        self.gpio = gpio
        self.rotated = False

    def rotate_servo(self, pulse_widths):
        pi = pigpio.pi()
        pi.set_mode(self.gpio, pigpio.OUTPUT)

        for pw in pulse_widths:
            pi.set_servo_pulsewidth(self.gpio, pw)
            time.sleep(5)

        self.rotated = True
        pi.stop()