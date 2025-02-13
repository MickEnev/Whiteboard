import tkinter as tk
from tkinter.colorchooser import askcolor

def start_drawing(event):
    global is_drawing, prev_x, prev_y, strokes, erase_strokes
    is_drawing = True
    prev_x, prev_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    strokes = []
    erase_strokes = []

def draw(event):
    global is_drawing, prev_x, prev_y, strokes, erase_strokes
    if is_drawing:
        current_x, current_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        line = canvas.create_line(prev_x, prev_y, current_x, current_y, fill=drawing_color, width=line_width, capstyle=tk.ROUND, smooth=True, tags="drawing")
        prev_x, prev_y = current_x, current_y
        strokes.append((line, line_width, drawing_color))
        erase_strokes.append((line, prev_x, prev_y, current_x, current_y, line_width, drawing_color))

def stop_drawing(event):
    global is_drawing, strokes
    is_drawing = False
    if strokes:
        undo_stack.append(list(strokes))
        redo_stack.clear()

def change_pen_color():
    global drawing_color
    color = askcolor()[1]
    if color:
        drawing_color = color

def change_pen_color_with_tab(event):
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

def undo(event=None):
    if undo_stack:
        last_item = undo_stack.pop()
        redo_stack.append([(item, canvas.coords(item), width, color) for item, width, color in last_item])
        for item, _, _ in last_item:
            canvas.delete(item)
        

def redo(event=None):
    if redo_stack:
        last_item = redo_stack.pop()
        restored_stroke = []
        for item, coords, og_width, og_color in last_item:
            if coords:
                new_line = canvas.create_line(coords, fill=og_color, width=og_width, capstyle=tk.ROUND, smooth=True, tags="drawing")
                restored_stroke.append((new_line, og_width, og_color))
        undo_stack.append(restored_stroke)

def start_pan(event):
        """Store the initial position for panning."""
        canvas.scan_mark(event.x, event.y)

def do_pan(event):
    """Move the canvas by dragging the mouse."""
    canvas.scan_dragto(event.x, event.y, gain=1)

def zoom(event):
    global scale_factor
    zoom_factor = 1.1 if event.delta > 0 else 0.9
    scale_factor *= zoom_factor

    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)

    canvas.scale("all", x, y, zoom_factor, zoom_factor)
    canvas.config(scrollregion=canvas.bbox("all"))

def erase(event):
    global undo_stack
    items_to_erase = []

    for stroke in undo_stack:
        new_stroke = []
        for item, x1, y1, x2, y2, width, color in stroke:
            if (x1 - 5 <= event.x <= x2 + 5) and (y1 - 5 <= event.y <= y2 + 5): 
                canvas.delete(item)  # Delete stroke if near cursor
            else:
                new_stroke.append((item, x1, y1, x2, y2, width, color)) 
        
        if new_stroke:
            items_to_erase.append(new_stroke)

    undo_stack = items_to_erase

def toggle_eraser():
    global eraser_mode
    eraser_mode = not eraser_mode
    if eraser_mode:
        canvas.bind("<B1-Motion>", erase)
    else:
        canvas.bind("<B1-Motion>", draw)
    eraser_button.config(text="Eraser ON" if eraser_mode else "Eraser OFF")

root = tk.Tk()
root.title("ME Paint (it's like ms paint but actually not terrible)")
root.config(cursor="plus")

canvas = tk.Canvas(root, bg="black")
canvas.pack(fill="both", expand=True)

is_drawing = False
drawing_color = "white"
line_width = 2
root.geometry("1920x1080")

controls_frame = tk.Frame(root)
controls_frame.pack(side="top", fill="x")

#color_button = tk.Button(controls_frame, text="Change Color", command=change_pen_color)
#clear_button = tk.Button(controls_frame, text="Clear Canvas", command=lambda: canvas.delete("all"))
eraser_button = tk.Button(controls_frame, text="Eraser OFF", command=toggle_eraser)
eraser_button.pack(side="left", padx=5, pady=5)

#color_button.pack(side="left", padx=5, pady=5)
#clear_button.pack(side="left", padx=5, pady=5)

#line_width_label = tk.Label(controls_frame, text="Line Width:")
#line_width_label.pack(side="left", padx=5, pady=5)

#line_width_slider = tk.Scale(controls_frame, from_=1, to=10, orient="horizontal", command=lambda val: change_line_width(val))
#line_width_slider.set(line_width)
#line_width_slider.pack(side="left", padx=5, pady=5)

undo_stack = []
redo_stack = []
strokes = []
erase_strokes = []
scale_factor = 1
eraser_mode = False

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)
canvas.bind("<Control-MouseWheel>", change_line_width_scroll)
root.bind("<Control-z>", undo)
root.bind("<Control-y>", redo)
root.bind("<Tab>", change_pen_color_with_tab)
canvas.bind("<Shift-ButtonPress-1>", start_pan)
canvas.bind("<Shift-B1-Motion>", do_pan)
canvas.bind("<MouseWheel>", zoom)

root.mainloop()