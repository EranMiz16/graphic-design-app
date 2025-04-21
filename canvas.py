import tkinter as tk
from tkinter import colorchooser, Scale, Button
from brush import Brush
from typing import List, Tuple, Dict



class  DrawingCanvas:
    """
    A class of canvas object, that will be used for illustrations and grahic design program.
    Handles creation of simple lines and the erasion of objects.
    """

    def __init__(self, master, width: int, height: int, bg: str="white", mode: str ='brush') -> None:
        """
        A cunstractor of the canvas object.
        """
        self.root = master
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=bg, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.bg = bg
        self.width = width
        self.height = height
        self.mode = mode
        self.eraser_size: float = 5.0
        self.eraser_detector = self.canvas.create_oval(0, 0, 0, 0, outline="black", fill='white', state="hidden")

        self.is_drawing = False
        self.start_x, self.start_y = None, None


        self.current_segment: List[int] = []
        self.item_to_segment_group: Dict[int, List[int]] = {}
        self.current_segment_coord: List[Tuple[int, int]] = []
        self.segment_groups_coord: Dict[int, List[Tuple[int, int]]]= {}

        self.begin_drawing()



    def get_mode(self) -> str:
        """
        To get the mode value from another classes.
        """
        return self.mode
    


    def change_bg(self) -> None:
        """
        Color chosing dialog to get a new deisred background color
        of the canvas from the user.
        """
        new_bg = colorchooser.askcolor(title="Choose Background Color")[1]
        if new_bg:
            self.update_background(new_bg)



    def update_background(self, new_bg: str) -> None:
        """
        Updates the background color of the canvas.
        """
        self.bg = new_bg
        self.canvas.config(bg=new_bg)   


    def set_brush(self, brush: Brush) -> None:
        """
        Sets a brush for the cavnas.
        """
        self.current_brush = brush


    def clear_bindings(self) -> None:
        """
        Unbind drawings and erasing binds.
        Used in transitioning between modes.
        """
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")


    def begin_drawing(self) -> None:
        """
        Bind events for drawing
        """
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)

    

    def start_drawing(self, event) -> None:
        """
        Starts the drawing action.
        Changes the current coords to the event ones.
        """
        self.is_drawing = True
        self.start_x, self.start_y = event.x, event.y
        self.current_segment = []
        self.current_segment_coord = []

    def draw(self, event) -> None:
        """
        Responsible for the drawing proccess;
        Creats the line.
        """
        if self.is_drawing and self.start_x and self.start_y:

            segment = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                        fill=self.current_brush.color, width=self.current_brush.thickness, tags=("movable", "erasable", "line"))
            
            self.current_segment.append(segment)
            self.current_segment_coord.append((event.x, event.y))

            self.item_to_segment_group[segment] = self.current_segment
            self.segment_groups_coord[segment] = self.current_segment_coord

            self.start_x, self.start_y = event.x, event.y



    def stop_drawing(self, event) -> None:
        """
        Stops the drawing action.
        """
        self.is_drawing = False
        


    

    def erase(self, event) -> None:
        """
        Making the erase action.
        """
        top_left_x = event.x - self.eraser_size
        top_left_y = event.y - self.eraser_size
        bottom_right_x = event.x + self.eraser_size
        bottom_right_y = event.y + self.eraser_size
        overlap_items = self.canvas.find_overlapping(top_left_x, top_left_y, bottom_right_x, bottom_right_y)

        for item in overlap_items:
            if "erasable" in self.canvas.gettags(item):
                self.canvas.delete(item)
      
        self.update_eraser_detector(event)



    def change_eraser_size(self) -> None:
        """
        Open's dialog window to get a new size value from
        the user, and changes erase's size.
        """
        def update_eraser() -> None:
            self.eraser_size = float(scale.get())
            eraser_dialog.destroy()

        eraser_dialog = tk.Toplevel()
        eraser_dialog.title("Set Eraser's Size")

        scale = Scale(eraser_dialog, from_=0, to=30, orient='horizontal', label=f"Currrent Size: {self.eraser_size}", length=300)
        scale.pack(padx=10, pady=10)

        ok_button = Button(eraser_dialog, text="OK", command=update_eraser)
        ok_button.pack()


        
    def update_eraser_detector(self, event) -> None:
        """
        Update the position and size of the eraser detector according to the mouse cursor and eraser size.
        """
        radius = self.eraser_size
        self.canvas.coords(self.eraser_detector, event.x - radius, event.y - radius, event.x + radius, event.y + radius)



    def fill_with_color(self, event) -> None:
        """
        Fill feature that can fill shapes, texts and canvas with color.
        """
        if self.fill_color:
            item = self.canvas.find_closest(event.x, event.y)[0]
            item_tags = self.canvas.gettags(item)

            if 'line' in item_tags:
                segment_group = self.segment_groups_coord.get(item, [])
                if self.is_shape_closed(segment_group):
                    self.canvas.create_polygon(segment_group, outline="black", fill=self.fill_color, tags=("movable", "erasable", "shape"))

            elif 'shape' in item_tags or 'text_box' in item_tags:
                self.canvas.itemconfig(item, fill=self.fill_color)

            else:
                self.canvas.config(bg=self.fill_color)



 
    def set_mode(self, mode: str) -> None:
        """
        Reponisble for modes transition
        """
        self.clear_bindings()
        self.mode = mode
        self.canvas.itemconfig(self.eraser_detector, state='hidden')

        if mode == 'eraser':
            self.canvas.itemconfig(self.eraser_detector, state='normal')
            self.canvas.bind("<B1-Motion>", self.erase)
            self.canvas.bind("<Motion>", self.update_eraser_detector)
            self.canvas.bind("<Button-1>", self.update_eraser_detector)

        if mode == 'brush':
            self.begin_drawing()

        elif mode == 'fill':
            self.fill_color = colorchooser.askcolor(title="Choose Fill Color")[1]
            self.canvas.bind("<Button-1>", self.fill_with_color)

        else:
            pass



    def reset_canvas(self) -> None:
        """
        Resets the canvas data.
        Used for starting again from blank canvas.
        """
        self.canvas.delete("all")

        self.is_drawing = False
        self.start_x, self.start_y = None, None
        self.current_segment = []
        self.item_to_segment_group = {}
        self.set_mode('brush')
    


    def is_shape_closed(self, points: List[Tuple[int, int]]) -> bool:
        """
        Determine if the shape is closed based on the distance between the first and last points.
        """
        if len(points) < 3:
            return False

        start_x, start_y = points[0]
        end_x, end_y = points[-1]

        distance = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5

        return distance <= 10

