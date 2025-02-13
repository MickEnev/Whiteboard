import tkinter as tk
from tkinter.colorchooser import askcolor

def start_drawing(event):
    global is_drawing, prev_x, prev_y
    is_drawing = True
    prev_x, prev_y = event.x, event.y

def draw(event):
    global is_drawing, prev_x, prev_y
    if is_drawing:
        current_x, current_y = event.x, event.y
        canvas.create_line(prev_x, prev_y, current_x, current_y, fill=drawing_color, width=line_width, capstyle=tk.ROUND, smooth=True)
        prev_x, prev_y = current_x, current_y

def stop_drawing(event):
    global is_drawing
    is_drawing = False

def change_pen_color():
    global drawing_color
    color = askcolor()[1]
    if color:
        drawing_color = color
         

def change_line_width(value):
    global line_width
    line_width = int(value)

def change_line_width_scroll(event):
    global line_width
    if event.delta > 0:
        line_width += 1
    elif event.delta < 0 and line_width > 1:
        line_width -= 1

root = tk.Tk()
root.title("ME Paint (it's like ms paint but actually not terrible)")

canvas = tk.Canvas(root, bg="black")
canvas.pack(fill="both", expand=True)

is_drawing = False
drawing_color = "white"
line_width = 2
root.geometry("1920x1080")


controls_frame = tk.Frame(root)
controls_frame.pack(side="top", fill="x")

color_button = tk.Button(controls_frame, text="Change Color", command=change_pen_color)
clear_button = tk.Button(controls_frame, text="Clear Canvas", command=lambda: canvas.delete("all"))

color_button.pack(side="left", padx=5, pady=5)
clear_button.pack(side="left", padx=5, pady=5)

line_width_label = tk.Label(controls_frame, text="Line Width:")
line_width_label.pack(side="left", padx=5, pady=5)

line_width_slider = tk.Scale(controls_frame, from_=1, to=10, orient="horizontal", command=lambda val: change_line_width(val))
line_width_slider.set(line_width)
line_width_slider.pack(side="left", padx=5, pady=5)

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)
canvas.bind("<Control-MouseWheel>", change_line_width_scroll)

root.mainloop()