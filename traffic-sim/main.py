import threading
import time
from simulator import GPIO

DATA_PIN = 1

vertical = [[16, 17, 18], [30, 29, 28], [32, 33, 34], [47, 46, 45]]

horizontal = [[8, 9, 10], [0, 1, 2]]

pedestraian_cross_hor = [[4, 5], [7, 6], [12, 13], [14, 15]]

pedestraian_cross_ver = [[20, 21], [24, 25], [22, 23], [27, 26], [36, 37], [38, 39], [41, 42], [44, 43]]


VER = 999
HOR = 998
STATE = VER


def light_pins(pins: list, app):
    arr = [0 for _ in range(48)]

    for pin in pins:
        arr[pin] = 1

    for state in arr:
        app.output(DATA_PIN, state)


def clear_pins(app):
    for _ in range(48):
        app.output(DATA_PIN, 0)


def turn_lights(all_lights, app):
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
        clear_pins(app)
        light_pins(final_array, app)
        time.sleep(1)
        final_array = []

    if STATE == VER:
        STATE = HOR
    elif STATE == HOR:
        STATE = VER
    time.sleep(5)


def control_leds(app):
    while True:
        turn_lights(vertical, app)

if __name__ == "__main__":
    gpio = GPIO()

    led_thread = threading.Thread(target=control_leds, args=(gpio,))
    led_thread.daemon = True
    led_thread.start()
    gpio.mainloop()
