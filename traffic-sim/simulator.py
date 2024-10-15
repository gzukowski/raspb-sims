import tkinter as tk

VERTICAL = 999
HORIZONTAL = 998
DATA_PIN = 1


class GPIO(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Symulacja skrzyżowania z diodami LED")
        self.geometry("800x800")
        
        self.canvas = tk.Canvas(self, width=800, height=800, bg="white")
        self.canvas.pack()
        
        self.create_circuit()
        self.create_switches()
        self.pin_index = 0
        
        
    def create_circuit(self):
        self.draw_paths()
        self.leds = {}
        self.led_colors = {}  # Store LED original colors here
        self.create_leds()
        
    def draw_paths(self):
        # top
        self.canvas.create_line(300, 0, 300, 300, width=4, fill="blue")
        self.canvas.create_line(350, 0, 350, 150, width=4, fill="blue")
        self.canvas.create_line(500, 0, 500, 300, width=4, fill="blue")
        self.canvas.create_line(550, 0, 550, 300, width=4, fill="blue")

        # left top
        self.canvas.create_line(400, 150, 400, 300, width=4, fill="blue")
        self.canvas.create_line(350, 150, 400, 150, width=4, fill="blue")

        # bottom
        self.canvas.create_line(300, 800, 300, 500, width=4, fill="blue")
        self.canvas.create_line(350, 800, 350, 500, width=4, fill="blue")
        self.canvas.create_line(500, 800, 500, 650, width=4, fill="blue")
        self.canvas.create_line(550, 800, 550, 500, width=4, fill="blue")

        # left bottom
        self.canvas.create_line(450, 650, 450, 500, width=4, fill="blue")
        self.canvas.create_line(450, 650, 500, 650, width=4, fill="blue")

        # left
        self.canvas.create_line(0, 300, 300, 300, width=4, fill="blue")
        self.canvas.create_line(0, 500, 300, 500, width=4, fill="blue")

        # right
        self.canvas.create_line(800, 300, 550, 300, width=4, fill="blue")
        self.canvas.create_line(800, 500, 550, 500, width=4, fill="blue")

        # horizontal 
        self.canvas.create_line(0, 400, 300, 400, dash=(10, 10), width=4, fill="blue")
        self.canvas.create_line(800, 400, 500, 400, dash=(10, 10), width=4, fill="blue")

        # vertical 
        self.canvas.create_line(350, 150, 350, 300, dash=(10, 10), width=4, fill="blue")
        self.canvas.create_line(500, 650, 500, 500, dash=(10, 10), width=4, fill="blue")

    def create_leds(self):
        self.create_led_group(560, 280, [('red', 0), ('yellow', 1), ('green', 2), ('green', 3)], HORIZONTAL)
        self.create_led_group(700, 280, [('red', 4), ('green', 5)], VERTICAL)
        self.create_led_group(700, 540, [('green', 6), ('red', 7)], VERTICAL)
        self.create_led_group(200, 520, [('green', 11), ('green', 10), ('yellow', 9), ('red', 8)], HORIZONTAL)
        self.create_led_group(100, 540, [('red', 12), ('green', 13)], VERTICAL)
        self.create_led_group(100, 280, [('green', 14), ('red', 15)], VERTICAL)
        self.create_led_group(280, 280, [('red', 16), ('yellow', 17), ('green', 18), ('green', 19)], VERTICAL)
        self.create_led_group(260, 50, [('red', 20), ('green', 21)], HORIZONTAL)
        self.create_led_group(360, 130, [('green', 23), ('red', 22)], HORIZONTAL)
        self.create_led_group(470, 50, [('red', 24), ('green', 25)], HORIZONTAL)
        self.create_led_group(560, 130, [('green', 26), ('red', 27)], HORIZONTAL)
        self.create_led_group(420, 280, [('red', 30), ('yellow', 29), ('green', 28)], VERTICAL)
        self.create_led_group(560, 580, [('green', 35), ('green', 34), ('yellow', 33), ('red', 32)], VERTICAL)
        self.create_led_group(560, 750, [('green', 37), ('red', 36)], HORIZONTAL)
        self.create_led_group(460, 660, [('red', 38), ('green', 39)], HORIZONTAL)
        self.create_led_group(360, 750, [('green', 42), ('red', 41)], HORIZONTAL)
        self.create_led_group(260, 660, [('red', 44), ('green', 43)], HORIZONTAL)
        self.create_led_group(360, 560, [('green', 45), ('yellow', 46), ('red', 47)], VERTICAL)
    
    def create_led_group(self, x, y, led_specs, layout):

        if layout == HORIZONTAL:
            for color, number in led_specs:
                led = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="gray", outline=color, width=2)
                self.canvas.create_text(x, y, text=str(number), fill="black")
                self.leds[number] = led
                self.led_colors[number] = color
                x += 20
        elif layout == VERTICAL:
            for color, number in led_specs:
                led = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="gray", outline=color, width=2)
                self.canvas.create_text(x, y, text=str(number), fill="black")
                self.leds[number] = led
                self.led_colors[number] = color
                y -= 20

    def create_switches(self):
        self.switch1 = tk.Button(self, text="SW1", command=self.toggle_switch1)
        self.switch1.place(x=750, y=600)
        
        self.switch2 = tk.Button(self, text="SW2", command=self.toggle_switch2)
        self.switch2.place(x=50, y=100)
        
    def toggle_switch1(self):
        for i in range(48):
            self.output(DATA_PIN, 1)
        
    def toggle_switch2(self):
        for i in range(48):
            self.output(DATA_PIN, 0)
        
    def output(self, pin_number, state):
        if pin_number == DATA_PIN:
            led_num = self.pin_index
            if led_num == 31 or led_num == 40: # these LEDs are skipped
                self.pin_index += 1
                return
            print(f"Pin {pin_number} (LED {led_num}), State: {'ON' if state else 'OFF'}")
            
            color = self.led_colors[led_num] if state else "gray"
            self.canvas.itemconfig(self.leds[led_num], fill=color)

            self.pin_index += 1
            if self.pin_index == 48:
                self.pin_index = 0
