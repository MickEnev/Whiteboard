import tkinter as tk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw, ImageTk, ImageColor

def start_drawing(event):
    global is_drawing, prev_x, prev_y, strokes, fill_mode
    if fill_mode:
        fill_area(event)
        return
    is_drawing = True
    prev_x, prev_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    strokes = []

def draw(event):
    global is_drawing, prev_x, prev_y, strokes, fill_mode
    if is_drawing and not fill_mode:
        current_x, current_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        line = canvas.create_line(prev_x, prev_y, current_x, current_y, fill=drawing_color, width=line_width, capstyle=tk.ROUND, smooth=True, tags="drawing")
        prev_x, prev_y = current_x, current_y
        strokes.append((line, line_width, drawing_color))

def stop_drawing(event):
    global is_drawing, strokes
    is_drawing = False
    if strokes:
        undo_stack.append(list(strokes))
        redo_stack.clear()

def change_pen_color_with_tab(event):
    global drawing_color
    if erase_mode:
        return
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
    global drawing_color, canvas, erase_mode, old_color
    if not erase_mode:
        old_color = drawing_color
        drawing_color = canvas.cget("bg")
        erase_mode = True
    else:
        drawing_color = old_color
        erase_mode = False

def fill_area(event):
    global image, img_tk

    x, y = int(canvas.canvasx(event.x)), int(canvas.canvasy(event.y))
    target_color = image.getpixel((x, y))  # Get the color at the clicked point

    # Convert hex or color names to RGB
    fill_rgb = ImageColor.getrgb(drawing_color)  

    # Ensure we're not filling an already-colored area
    if target_color == fill_rgb:
        return  

    # Apply flood fill with the converted RGB color
    ImageDraw.floodfill(image, (x, y), fill_rgb, thresh=5)

    # Update the canvas with the new image
    img_tk = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_on_canvas, image=img_tk)

def resize_canvas(event):
    """Resizes the background image dynamically when the window is resized."""
    global image, img_tk, image_on_canvas

    # Get new canvas dimensions
    new_width = event.width
    new_height = event.height

    # Resize the image while maintaining original drawing
    image_resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Convert to Tkinter format and update canvas
    img_tk = ImageTk.PhotoImage(image_resized)
    canvas.itemconfig(image_on_canvas, image=img_tk)
    canvas.config(scrollregion=canvas.bbox("all"))

def toggle_fill_mode(event):
    global fill_mode
    if fill_mode:
        fill_mode = False
    else:
        fill_mode = True


root = tk.Tk()
root.title("ME Paint (it's like ms paint but actually not terrible)")

canvas = tk.Canvas(root, bg="black")
canvas.pack(fill="both", expand=True)

initial_width, initial_height = 800, 600
image = Image.new("RGB", (initial_width, initial_height), "white")
img_tk = ImageTk.PhotoImage(image)
image_on_canvas = canvas.create_image(0, 0, anchor="nw", image=img_tk)

is_drawing = False
erase_mode = False
fill_mode = False
drawing_color = "white"
old_color = "white"
line_width = 2
root.geometry("1920x1080")

#controls_frame = tk.Frame(root)
#controls_frame.pack(side="top", fill="x")

#color_button = tk.Button(controls_frame, text="Change Color", command=change_pen_color)
#clear_button = tk.Button(controls_frame, text="Clear Canvas", command=lambda: canvas.delete("all"))

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
scale_factor = 1

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
root.bind("<e>", erase)
root.bind("<f>", toggle_fill_mode)

root.mainloop()