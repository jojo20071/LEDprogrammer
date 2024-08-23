import tkinter as tk
from tkinter.colorchooser import askcolor

class LEDStripApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Strip Programmer")
        self.create_widgets()

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

    def start_program(self):
        pass

    def pick_color(self):
        color = askcolor()[1]
        if color:
            self.color_button.config(bg=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = LEDStripApp(root)
    root.mainloop()