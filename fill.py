import tkinter as tk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw, ImageTk

def fill_area(event):
    """Perform flood fill using PIL on the clicked area."""
    global image, img_tk
    x, y = int(canvas.canvasx(event.x)), int(canvas.canvasy(event.y))
    target_color = image.getpixel((x, y))

    if target_color == drawing_color_rgb:
        return  # No need to fill if it's already the same color

    ImageDraw.floodfill(image, (x, y), drawing_color_rgb, thresh=5)

    # Update the canvas with the modified image
    img_tk = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_on_canvas, image=img_tk)

def change_pen_color_with_tab(event):
    """Change the pen color using the color chooser."""
    global drawing_color, drawing_color_rgb
    color = askcolor()[1]
    if color:
        drawing_color = color
        drawing_color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))  # Convert hex to RGB

# Main window setup
root = tk.Tk()
root.title("ME Paint with True Fill Tool")

canvas = tk.Canvas(root, bg="black")
canvas.pack(fill="both", expand=True)

# Create a blank white image
width, height = 800, 600
image = Image.new("RGB", (width, height), "white")
img_tk = ImageTk.PhotoImage(image)
image_on_canvas = canvas.create_image(0, 0, anchor="nw", image=img_tk)

drawing_color = "#000000"  # Default fill color (black)
drawing_color_rgb = (0, 0, 0)  # RGB equivalent

canvas.bind("<Button-1>", fill_area)  # Bind fill tool to left-click
root.bind("<Tab>", change_pen_color_with_tab)

root.mainloop()