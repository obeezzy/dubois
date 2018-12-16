import RPi.GPIO as GPIO

class LocomotionControl(object):
    LEFT_MOTOR_FORWARD_PIN = 18
    LEFT_MOTOR_REVERSE_PIN = 23
    RIGHT_MOTOR_FORWARD_PIN = 24
    RIGHT_MOTOR_REVERSE_PIN = 25

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LEFT_MOTOR_FORWARD_PIN, GPIO.OUT)
        GPIO.setup(self.LEFT_MOTOR_REVERSE_PIN, GPIO.OUT)
        GPIO.setup(self.RIGHT_MOTOR_FORWARD_PIN, GPIO.OUT)
        GPIO.setup(self.RIGHT_MOTOR_REVERSE_PIN, GPIO.OUT)

    def stop(self):
        GPIO.output(self.LEFT_MOTOR_FORWARD_PIN, GPIO.LOW)
        GPIO.output(self.LEFT_MOTOR_REVERSE_PIN, GPIO.LOW)
        GPIO.output(self.RIGHT_MOTOR_FORWARD_PIN, GPIO.LOW)
        GPIO.output(self.RIGHT_MOTOR_REVERSE_PIN, GPIO.LOW)

    def move_forward(self):
        self.stop()
        GPIO.output(self.LEFT_MOTOR_FORWARD_PIN, GPIO.HIGH)
        GPIO.output(self.RIGHT_MOTOR_FORWARD_PIN, GPIO.HIGH)

    def move_in_reverse(self):
        self.stop()
        GPIO.output(self.LEFT_MOTOR_REVERSE_PIN, GPIO.HIGH)
        GPIO.output(self.RIGHT_MOTOR_REVERSE_PIN, GPIO.HIGH)

    def move_counterclockwise(self):
        self.stop()
        GPIO.output(self.LEFT_MOTOR_REVERSE_PIN, GPIO.HIGH)
        GPIO.output(self.RIGHT_MOTOR_FORWARD_PIN, GPIO.HIGH)

    def move_clockwise(self):
        self.stop()
        GPIO.output(self.LEFT_MOTOR_FORWARD_PIN, GPIO.HIGH)
        GPIO.output(self.RIGHT_MOTOR_REVERSE_PIN, GPIO.HIGH)

    def shutdown(self):
        GPIO.cleanup()


