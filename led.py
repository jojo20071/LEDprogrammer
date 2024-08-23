import tkinter as tk
from tkinter.colorchooser import askcolor
import board
import neopixel
import time
import json
import random
from tkinter import filedialog

class LEDStripApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Strip Programmer")
        self.create_widgets()
        self.num_strips = 2
        self.pixels = [neopixel.NeoPixel(board.D18, 30, auto_write=False) for _ in range(self.num_strips)]
        self.current_config = {}

    def create_widgets(self):
        self.label = tk.Label(self.root, text="LED Strip Programmer")
        self.label.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_program)
        self.start_button.pack()

        self.save_button = tk.Button(self.root, text="Save Config", command=self.save_config)
        self.save_button.pack()

        self.load_button = tk.Button(self.root, text="Load Config", command=self.load_config)
        self.load_button.pack()

        self.color_button = tk.Button(self.root, text="Pick Color", command=self.pick_color)
        self.color_button.pack()

        self.random_color_button = tk.Button(self.root, text="Random Color", command=self.random_color)
        self.random_color_button.pack()

        self.r_label = tk.Label(self.root, text="Red")
        self.r_label.pack()
        self.r_entry = tk.Entry(self.root)
        self.r_entry.pack()

        self.g_label = tk.Label(self.root, text="Green")
        self.g_label.pack()
        self.g_entry = tk.Entry(self.root)
        self.g_entry.pack()

        self.b_label = tk.Label(self.root, text="Blue")
        self.b_label.pack()
        self.b_entry = tk.Entry(self.root)
        self.b_entry.pack()

        self.brightness_label = tk.Label(self.root, text="Brightness")
        self.brightness_label.pack()
        
        self.brightness_slider = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL)
        self.brightness_slider.pack()

        self.pattern_label = tk.Label(self.root, text="Pattern")
        self.pattern_label.pack()

        self.pattern_var = tk.StringVar(value="Solid")
        self.pattern_menu = tk.OptionMenu(self.root, self.pattern_var, "Solid", "Blink", "Chase", "Fade", "Cycle")
        self.pattern_menu.pack()

        self.speed_label = tk.Label(self.root, text="Speed")
        self.speed_label.pack()
        
        self.speed_slider = tk.Scale(self.root, from_=1, to_=10, orient=tk.HORIZONTAL)
        self.speed_slider.pack()

        self.duration_label = tk.Label(self.root, text="Duration (s)")
        self.duration_label.pack()
        
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.pack()

        self.preview_label = tk.Label(self.root, text="Pattern Preview")
        self.preview_label.pack()

        self.preview_canvas = tk.Canvas(self.root, width=200, height=50, bg='black')
        self.preview_canvas.pack()

        self.strip_count_label = tk.Label(self.root, text="Number of Strips")
        self.strip_count_label.pack()
        self.strip_count_entry = tk.Entry(self.root)
        self.strip_count_entry.pack()

    def start_program(self):
        try:
            self.num_strips = int(self.strip_count_entry.get())
        except ValueError:
            self.num_strips = 2
        self.pixels = [neopixel.NeoPixel(board.D18, 30, auto_write=False) for _ in range(self.num_strips)]
        
        color = self.color_button.cget("bg")
        r = int(self.r_entry.get() or 0)
        g = int(self.g_entry.get() or 0)
        b = int(self.b_entry.get() or 0)
        brightness = self.brightness_slider.get() / 100
        pattern = self.pattern_var.get()
        speed = self.speed_slider.get()
        duration = float(self.duration_entry.get())

        if not color or (r == 0 and g == 0 and b == 0):
            color = "#{:02x}{:02x}{:02x}".format(r, g, b)

        config = {
            'color': color,
            'brightness': brightness,
            'pattern': pattern,
            'speed': speed,
            'duration': duration,
            'num_strips': self.num_strips
        }
        self.current_config = config
        self.apply_settings(color, brightness, pattern, speed, duration)
        self.update_preview(color, pattern)

    def pick_color(self):
        color = askcolor()[1]
        if color:
            self.color_button.config(bg=color)

    def random_color(self):
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.color_button.config(bg=color)

    def update_preview(self, color, pattern):
        self.preview_canvas.delete("all")
        r, g, b = self.hex_to_rgb(color)
        if pattern == "Solid":
            self.preview_canvas.create_rectangle(0, 0, 200, 50, fill=color)
        elif pattern == "Blink":
            self.preview_canvas.create_rectangle(0, 0, 200, 50, fill=color)
        elif pattern == "Chase":
            for i in range(0, 200, 20):
                self.preview_canvas.create_rectangle(i, 0, i + 20, 50, fill=color)
        elif pattern == "Fade":
            for i in range(0, 200, 20):
                fade_color = "#{:02x}{:02x}{:02x}".format(int(r * i / 200), int(g * i / 200), int(b * i / 200))
                self.preview_canvas.create_rectangle(i, 0, i + 20, 50, fill=fade_color)
        elif pattern == "Cycle":
            for i in range(0, 200, 20):
                cycle_color = "#{:02x}{:02x}{:02x}".format((i * 255 // 200) % 255, (255 - i * 255 // 200) % 255, (i * 2) % 255)
                self.preview_canvas.create_rectangle(i, 0, i + 20, 50, fill=cycle_color)

    def apply_settings(self, color, brightness, pattern, speed, duration):
        for strip in self.pixels:
            if pattern == "Solid":
                self.solid_pattern(strip, color, brightness)
            elif pattern == "Blink":
                self.blink_pattern(strip, color, brightness, speed, duration)
            elif pattern == "Chase":
                self.chase_pattern(strip, color, brightness, speed, duration)
            elif pattern == "Fade":
                self.fade_pattern(strip, color, brightness, speed, duration)
            elif pattern == "Cycle":
                self.cycle_pattern(strip, speed, duration)

    def save_config(self):
        if self.current_config:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump(self.current_config, f)

    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                config = json.load(f)
                self.color_button.config(bg=config['color'])
                self.brightness_slider.set(config['brightness'] * 100)
                self.pattern_var.set(config['pattern'])
                self.speed_slider.set(config['speed'])
                self.duration_entry.delete(0, tk.END)
                self.duration_entry.insert(0, config['duration'])
                self.r_entry.delete(0, tk.END)
                self.r_entry.insert(0, self.hex_to_rgb(config['color'])[0])
                self.g_entry.delete(0, tk.END)
                self.g_entry.insert(0, self.hex_to_rgb(config['color'])[1])
                self.b_entry.delete(0, tk.END)
                self.b_entry.insert(0, self.hex_to_rgb(config['color'])[2])
                self.strip_count_entry.delete(0, tk.END)
                self.strip_count_entry.insert(0, config.get('num_strips', 2))
                self.current_config = config
                self.update_preview(config['color'], config['pattern'])

    def solid_pattern(self, strip, color, brightness):
        r, g, b = self.hex_to_rgb(color)
        r, g, b = int(r * brightness), int(g * brightness), int(b * brightness)
        strip.fill((r, g, b))
        strip.show()

    def blink_pattern(self, strip, color, brightness, speed, duration):
        r, g, b = self.hex_to_rgb(color)
        r, g, b = int(r * brightness), int(g * brightness), int(b * brightness)
        end_time = time.time() + duration
        while time.time() < end_time:
            strip.fill((r, g, b))
            strip.show()
            time.sleep(1 / speed)
            strip.fill((0, 0, 0))
            strip.show()
            time.sleep(1 / speed)

    def chase_pattern(self, strip, color, brightness, speed, duration):
        r, g, b = self.hex_to_rgb(color)
        r, g, b = int(r * brightness), int(g * brightness), int(b * brightness)
        end_time = time.time() + duration
        while time.time() < end_time:
            for i in range(len(strip)):
                strip.fill((0, 0, 0))
                strip[i] = (r, g, b)
                strip.show()
                time.sleep(1 / speed)
        strip.fill((0, 0, 0))
        strip.show()

    def fade_pattern(self, strip, color, brightness, speed, duration):
        r, g, b = self.hex_to_rgb(color)
        r, g, b = int(r * brightness), int(g * brightness), int(b * brightness)
        fade_steps = 100
        step_delay = duration / fade_steps
        for step in range(fade_steps):
            intensity = int((step / fade_steps) * 255)
            color_step = (intensity, intensity, intensity)
            strip.fill(color_step)
            strip.show()
            time.sleep(step_delay)
        strip.fill((0, 0, 0))
        strip.show()

    def cycle_pattern(self, strip, speed, duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            for color in range(0, 255, 5):
                strip.fill((color, 255 - color, (color * 2) % 255))
                strip.show()
                time.sleep(1 / speed)
        strip.fill((0, 0, 0))
        strip.show()

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        length = len(hex_color)
        return tuple(int(hex_color[i:i + length // 3], 16) for i in range(0, length, length // 3))

if __name__ == "__main__":
    root = tk.Tk()
    app = LEDStripApp(root)
    root.mainloop()