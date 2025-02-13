import tkinter as tk

class InfiniteCanvas(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Infinite Canvas with Zoom & Drawing")
        self.geometry("800x600")

        # Create a frame to hold the canvas and scrollbars
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        self.h_scroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure scrolling
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        # Set an initial large scrollable region
        self.scroll_size = 10000
        self.canvas.config(scrollregion=(-self.scroll_size, -self.scroll_size, self.scroll_size, self.scroll_size))

        # Bind mouse events for panning
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.do_pan)

        # Bind mouse wheel for zooming
        self.canvas.bind("<MouseWheel>", self.zoom)

        # Drawing functionality
        self.drawing = False
        self.start_x = self.start_y = None
        self.current_shape = None

        self.canvas.bind("<ButtonPress-3>", self.start_draw)
        self.canvas.bind("<B3-Motion>", self.draw_shape)
        self.canvas.bind("<ButtonRelease-3>", self.finish_draw)

        self.scale_factor = 1.0

    def start_pan(self, event):
        """Store the initial position for panning."""
        self.canvas.scan_mark(event.x, event.y)

    def do_pan(self, event):
        """Move the canvas by dragging the mouse."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event):
        """Zoom in or out with the mouse wheel."""
        zoom_factor = 1.1 if event.delta > 0 else 0.9
        self.scale_factor *= zoom_factor

        self.canvas.scale("all", event.x, event.y, zoom_factor, zoom_factor)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def start_draw(self, event):
        """Start drawing a shape with right mouse button."""
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="black", width=2)
        self.drawing = True

    def draw_shape(self, event):
        """Resize the shape as the user drags."""
        if self.drawing and self.current_shape:
            end_x = self.canvas.canvasx(event.x)
            end_y = self.canvas.canvasy(event.y)
            self.canvas.coords(self.current_shape, self.start_x, self.start_y, end_x, end_y)

    def finish_draw(self, event):
        """Finish drawing when the right mouse button is released."""
        self.drawing = False
        self.current_shape = None

if __name__ == "__main__":
    app = InfiniteCanvas()
    app.mainloop()
