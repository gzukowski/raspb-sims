import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


DATA=20
CLK=21
LE=22
OE1=23
OE2=24
OE3=25
SW1=26
SW2=27

# GPIO SETUP IN/OUT \/
#
#
#
# GPIO SETUP IN/OUT /\

vertical = [[16, 17, 18], [30, 29, 28], [32, 33, 34], [47, 46, 45]]

horizontal = [[8, 9, 10], [0, 1, 2]]

pedestraian_cross_hor = [[4, 5], [7, 6], [12, 13], [14, 15]]

pedestraian_cross_ver = [[20, 21], [24, 25], [22, 23], [27, 26], [36, 37], [38, 39], [41, 42], [44, 43]]


VER = 999
HOR = 998
STATE = VER
LOW = 0
HIGH = 1

GPIO.output(OE1, LOW)
GPIO.output(OE2, LOW)
GPIO.output(OE3, LOW)


def light_pins(pins: list):
    arr = [0 for _ in range(48)]

    for pin in pins:
        arr[pin] = HIGH

    for state in arr:
        GPIO.output(DATA, state)
        GPIO.output(CLK, HIGH)
        GPIO.output(LE, HIGH)
        GPIO.output(CLK, LOW)
        GPIO.output(LE, LOW)


def clear_pins():
    for _ in range(48):
        GPIO.output(DATA, LOW)
        GPIO.output(CLK, HIGH)
        GPIO.output(LE, HIGH)
        GPIO.output(CLK, LOW)
        GPIO.output(LE, LOW)


def turn_lights():
    final_array = []
    global STATE
    for index in range(3):
        if STATE == VER:
            for lights in vertical:
                final_array.append(lights[index])
            
            for lights in horizontal:
                temp = lights[::-1]
                final_array.append(temp[index])
            
            for duos in pedestraian_cross_ver:
                final_array.append(duos[0])
            
            for duos in pedestraian_cross_hor:
                final_array.append(duos[1])
            
        elif STATE == HOR:
            for lights in horizontal:
                final_array.append(lights[index])
            
            for lights in vertical:
                temp = lights[::-1]
                final_array.append(temp[index])

            for duos in pedestraian_cross_ver:
                final_array.append(duos[1])
            
            for duos in pedestraian_cross_hor:
                final_array.append(duos[0])
        clear_pins()
        light_pins(final_array)
        time.sleep(1)
        final_array = []

    if STATE == VER:
        STATE = HOR
    elif STATE == HOR:
        STATE = VER
    time.sleep(5)


def get_button():
    value = GPIO.input(SW1)
    time.sleep(0.1)

    if value == LOW:
        pass

while True:
    turn_lights()
