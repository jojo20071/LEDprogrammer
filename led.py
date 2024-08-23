import tkinter as tk
from tkinter.colorchooser import askcolor
import board
import neopixel
import time

class LEDStripApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Strip Programmer")
        self.create_widgets()

        self.pixels = neopixel.NeoPixel(board.D18, 30, auto_write=False)

    def create_widgets(self):
        self.label = tk.Label(self.root, text="LED Strip Programmer")
        self.label.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_program)
        self.start_button.pack()

        self.color_button = tk.Button(self.root, text="Pick Color", command=self.pick_color)
        self.color_button.pack()

        self.brightness_label = tk.Label(self.root, text="Brightness")
        self.brightness_label.pack()
        
        self.brightness_slider = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL)
        self.brightness_slider.pack()

        self.pattern_label = tk.Label(self.root, text="Pattern")
        self.pattern_label.pack()

        self.pattern_var = tk.StringVar(value="Solid")
        self.pattern_menu = tk.OptionMenu(self.root, self.pattern_var, "Solid", "Blink", "Chase")
        self.pattern_menu.pack()

        self.speed_label = tk.Label(self.root, text="Speed")
        self.speed_label.pack()
        
        self.speed_slider = tk.Scale(self.root, from_=1, to_=10, orient=tk.HORIZONTAL)
        self.speed_slider.pack()

        self.duration_label = tk.Label(self.root, text="Duration (s)")
        self.duration_label.pack()
        
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.pack()

    def start_program(self):
        color = self.color_button.cget("bg")
        brightness = self.brightness_slider.get() / 100
        pattern = self.pattern_var.get()
        speed = self.speed_slider.get()
        duration = float(self.duration_entry.get())

        self.apply_settings(color, brightness, pattern, speed, duration)

    def pick_color(self):
        color = askcolor()[1]
        if color:
            self.color_button.config(bg=color)

    def apply_settings(self, color, brightness, pattern, speed, duration):
        if pattern == "Solid":
            self.solid_pattern(color, brightness)
        elif pattern == "Blink":
            self.blink_pattern(color, brightness, speed, duration)
        elif pattern == "Chase":
            self.chase_pattern(color, brightness, speed, duration)

    def solid_pattern(self, color, brightness):
        r, g, b = self.hex_to_rgb(color)
        r, g, b = int(r * brightness), int(g * brightness), int(b * brightness)
        self.pixels.fill((r, g, b))
        self.pixels.show()

    def blink_pattern(self, color, brightness, speed, duration):
        r, g, b = self.hex_to_rgb(color)
        r, g, b = int(r * brightness), int(g * brightness), int(b * brightness)
        end_time = time.time() + duration
        while time.time() < end_time:
            self.pixels.fill((r, g, b))
            self.pixels.show()
            time.sleep(1 / speed)
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
            time.sleep(1 / speed)

    def chase_pattern(self, color, brightness, speed, duration):
        r, g, b = self.hex_to_rgb(color)
        r, g, b = int(r * brightness), int(g * brightness), int(b * brightness)
        end_time = time.time() + duration
        while time.time() < end_time:
            for i in range(len(self.pixels)):
                self.pixels.fill((0, 0, 0))
                self.pixels[i] = (r, g, b)
                self.pixels.show()
                time.sleep(1 / speed)
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        length = len(hex_color)
        return tuple(int(hex_color[i:i + length // 3], 16) for i in range(0, length, length // 3))

if __name__ == "__main__":
    root = tk.Tk()
    app = LEDStripApp(root)
    root.mainloop()