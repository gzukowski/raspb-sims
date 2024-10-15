import threading
import time
from simulator import GPIO

DATA_PIN = 1

def control_leds(app):
    counter = 0
    while True:
        counter += 1
        for i in range(48):
            if counter % 2:
                app.output(DATA_PIN, 1)
            else:
                app.output(DATA_PIN, 0)
        time.sleep(0.5)

if __name__ == "__main__":
    gpio = GPIO()

    led_thread = threading.Thread(target=control_leds, args=(gpio,))
    led_thread.daemon = True
    led_thread.start()
    gpio.mainloop()
