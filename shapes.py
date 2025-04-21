from tkinter import colorchooser, Scale, Button
import tkinter as tk
from typing import Tuple, Optional, List, Dict, Any
from canvas import DrawingCanvas

class Shapes:
    """
    Class of creation of shapes. used to create various shapes
    in iilustration program.
    """
    def __init__(self, canvas: DrawingCanvas):
        """
        A constructor of shapes class.
        """
        self.canvas = canvas
        self.current_shape: Optional[str] = None  
        self.shape_color = "black"
        self.fill_color = "white"

        self.triangle_size = 50.0
        self.rectangle_size = 50.0
        self.oval_size = 50.0

        self.drawn_shapes: Dict[int, Any] = {}
        self.current_dot: List[int] = []
        self.drawn_dots: List[List[int]] = []

        self.dot_radius = 2.0
        self.dot_color = "black"
        self.dot_spacing = 10
        self.last_dot_position: Optional[Tuple[int, int]] = None
    


    def set_current_shape(self, shape_type: str) -> None:
        """
        This method modifying between shapes, and bind the events
        for creating them.
        """
        self.canvas.set_mode('shapes')
        self.current_shape = shape_type

        if shape_type == 'dots':
            self.last_dot_position = None
            self.canvas.canvas.bind('<B1-Motion>', self.dot_drawing_helper)

            if len(self.current_dot) > 0:
                self.drawn_dots.append(self.current_dot)
                self.current_dot.clear()

        elif shape_type == 'polygon':
            self.polygon_vertices: List[Tuple[int, int]] = []
            self.canvas.canvas.bind("<Button-1>", self.add_polygon_vertex)
            self.canvas.canvas.bind("<Button-2>", self.complete_polygon)

        else:
            self.canvas.canvas.bind("<Button-1>", self.regular_shapes)



    def regular_shapes(self, event) -> None:
        """
        This method responsible for creating simple shapes.
        """
        if self.current_shape == "rectangle":
            self.draw_rectangle(event.x, event.y)

        elif self.current_shape == "oval":
            self.draw_oval(event.x, event.y)
            
        elif self.current_shape == "triangle":
            self.draw_triangle(event.x, event.y)



    def draw_rectangle(self, x: int, y: int) -> None:
        """
        Method for creating rectangle.
        """
        shape_id = self.canvas.canvas.create_rectangle(x - self.rectangle_size/2, y - self.rectangle_size/2, x + self.rectangle_size/2, y + self.rectangle_size/2,
                                      outline=self.shape_color, fill=self.fill_color, tags=("movable", "erasable", "shape"))
        self.drawn_shapes[shape_id] = self




    def draw_oval(self, x: int, y: int) -> None:
        """
        Method for creating circle.
        """
        shape_id = self.canvas.canvas.create_oval(x - self.oval_size/2, y - self.oval_size/2, x + self.oval_size/2, y + self.oval_size/2,
                                outline=self.shape_color, fill=self.fill_color, tags=("movable", "erasable", "shape"))
        self.drawn_shapes[shape_id] = self







    def draw_triangle(self, x: int, y: int) -> None:
        """
        Method for creating triangle.
        """
        height = (self.triangle_size * (3 ** 0.5)) / 2
        vertex1 = (x, y - 2 * height / 3)
        vertex2 = (x - self.triangle_size / 2, y + height / 3)
        vertex3 = (x + self.triangle_size / 2, y + height / 3)

        shape_id = self.canvas.canvas.create_polygon(vertex1, vertex2, vertex3, outline=self.shape_color,
                                fill=self.fill_color, tags=("movable", "erasable", "shape"))
        
        self.drawn_shapes[shape_id] = self





    def set_shape_color(self, clicked_shape: Optional[int] =None) -> None:
        """
        This method opens a dialog with the user to change the outline color of shapes.
        """
        color_code = colorchooser.askcolor(title="Choose Color")
        if color_code[1]:

            if clicked_shape:
                self.canvas.canvas.itemconfig(clicked_shape, outline=color_code[1])
            else:
                self.shape_color = color_code[1]
    



    def set_fill_color(self, clicked_shape: Optional[int] =None) -> None:
        """
        This method opens a dialog with the user to change the color of shapes.
        """
        color_code = colorchooser.askcolor(title="Choose Color")
        if color_code[1]:

            if clicked_shape:
                self.canvas.canvas.itemconfig(clicked_shape, fill=color_code[1])

            else:
                self.fill_color = color_code[1]
    





    def change_specific_triangle(self, clicked_shape: int, new_size: float, coords: List[float]) -> None:
        """
        Changing specific triangle's size on canvas.
        """
        height = (new_size * (3 ** 0.5)) / 2

        center_x = sum(coords[::2]) / 3
        center_y = sum(coords[1::2]) / 3

        vertex1 = (center_x, center_y - 2 * height / 3)
        vertex2 = (center_x - new_size / 2, center_y + height / 3)
        vertex3 = (center_x + new_size / 2, center_y + height / 3)

        new_coords = [coord for vertex in [vertex1, vertex2, vertex3] for coord in vertex]

        self.canvas.canvas.coords(clicked_shape, *new_coords)





    def change_specific_oval_rectangle(self, clicked_shape: int, new_size: float, coords: List[float]) -> None:
        """
        Changing specific shape's size on canvas.
        """
        center_x = (coords[0] + coords[2]) / 2
        center_y = (coords[1] + coords[3]) / 2
                
        new_coords = [center_x - new_size / 2, center_y - new_size / 2, center_x + new_size / 2, center_y + new_size / 2]
        self.canvas.canvas.coords(clicked_shape, new_coords)





    def adjust_size_to_shape(self, shape_type: str, size: float) -> None:
        """
        Method that responsible to change the desired shape's size.
        """
        if shape_type == 'polygon':
            self.triangle_size = size

        if shape_type == 'rectangle':
            self.rectangle_size = size

        if shape_type == 'oval':
            self.oval_size = size




    def set_shape_size(self, shape_type: str, clicked_shape: Optional[int] =None) -> None:
        """
        Open a new size dialog with the user, gets new value and changes shapes size
        """
        def update_shape_size() -> None:
            new_size = scale.get()

            if clicked_shape:

                coords = self.canvas.canvas.coords(clicked_shape)
                print(coords)
                if len(coords) == 4:
                    self.change_specific_oval_rectangle(clicked_shape, new_size, coords)

                elif len(coords) == 6:
                    self.change_specific_triangle(clicked_shape, new_size, coords)
            else:
                self.adjust_size_to_shape(shape_type, new_size)

            size_dialog.destroy()

        size_dialog = tk.Toplevel()
        size_dialog.title("Set Shapes Size")


        scale = Scale(size_dialog, from_=0, to=100, orient='horizontal', label=f"Change Shape's Size", length=300)
        scale.pack(padx=10, pady=10)

        ok_button = Button(size_dialog, text="OK", command=update_shape_size)
        ok_button.pack()



    def draw_dots(self, start: Tuple[int, int], end: Optional[Tuple[int, int]] =None) -> None:
        """
        This method draw dots on the canvas.
        Been used for drawing dots line and polygon figures.
        """
        if end:
            dx, dy = end[0] - start[0], end[1] - start[1]
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            steps = max(1, int(distance / self.dot_spacing))


            for step in range(steps + 1):
                x = start[0] + (dx * step / steps)
                y = start[1] + (dy * step / steps)
                self.place_dot((x, y))
        else:
            self.place_dot(start)



    def place_dot(self, position: Tuple[float, float]) -> None:
        """
        Places a single dot at the given position.
        """
        dot_id = self.canvas.canvas.create_oval(
                position[0] - self.dot_radius, position[1] - self.dot_radius,
                position[0] + self.dot_radius, position[1] + self.dot_radius,
                fill=self.dot_color, outline=self.dot_color,
                tags=("movable", "erasable", "polygon"))
                
        self.current_dot.append(dot_id)



    def dot_drawing_helper(self, event) -> None:
        """
        Helper method for draw_dots method.
        """
        current_x, current_y = event.x, event.y
    
        if self.last_dot_position:
            distance = ((current_x - self.last_dot_position[0])**2 + (current_y - self.last_dot_position[1])**2)**0.5
            if distance > self.dot_spacing:
                self.draw_dots((current_x, current_y))

            else:
                self.draw_dots(self.last_dot_position, (current_x, current_y))

        else:
            self.draw_dots((current_x, current_y))
        self.last_dot_position = (current_x, current_y)
        self.canvas.canvas.bind("<ButtonRelease-1>", self.add_current_dot)



    def add_current_dot(self, event=None) -> None:
        """
        This methods add the dotted line to a list which stores all lines.
        """
        if self.current_dot:
            self.drawn_dots.append(self.current_dot)
            self.current_dot = []



    def ask_for_dot_radius(self) -> None:
        """
        Open a new thickness dialog with the user, gets new value and changes dotted line's thickness.
        """
        def update_dot_radius() -> None:
            self.dot_radius = float(scale.get() / 20)
            thickness_dialog.destroy()

        thickness_dialog = tk.Toplevel()
        thickness_dialog.title("Set Thickness")


        scale = Scale(thickness_dialog, from_=0, to=100, orient='horizontal', label=f"Currrent Dot's Size: {self.dot_radius * 20}", length=300)
        scale.pack(padx=10, pady=10)

        ok_button = Button(thickness_dialog, text="OK", command=update_dot_radius)
        ok_button.pack()



    def ask_for_dot_color(self) -> None:
        """
        Open a new color dialog with the user, gets new value and changes dotted line's color.
        """
        new_color = colorchooser.askcolor(title="Choose Dots Color")[1]
        if new_color:
            self.dot_color = new_color





    def add_polygon_vertex(self, event) -> None:
        """
        Adds a vertex to the polygon.
        """
        self.polygon_vertices.append((event.x, event.y))
        polygon_id = self.canvas.canvas.create_oval(event.x - self.dot_radius, event.y - self.dot_radius, event.x + self.dot_radius, event.y + self.dot_radius,
                                 fill=self.dot_color, outline=self.dot_color, tags=("movable", "erasable", "polygon"))
        
        self.current_dot.append(polygon_id)



    def complete_polygon(self, event) -> None:
        """
        This method completes the polygon creation.
        """
        if len(self.polygon_vertices) > 2:

            self.polygon_vertices.append(self.polygon_vertices[0])

            for i in range(len(self.polygon_vertices) - 1):

                self.draw_dots(self.polygon_vertices[i], self.polygon_vertices[i + 1])
            self.drawn_dots.append(self.current_dot)
            self.polygon_vertices.clear()




    def draw_shape_by_drag(self, shape_type: str) -> None:
        """
        Binds event for custom rectangle and oval drawings.
        """
        self.dragged_shape_name = shape_type
        self.canvas.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.canvas.bind("<ButtonRelease-1>", self.on_release)

        

    def on_press(self, event) -> None:
        """
        Starts the custom shapes drawing
        """
        self.start_x = event.x
        self.start_y = event.y
        self.dragged_shape = getattr(self.canvas.canvas, "create_" + self.dragged_shape_name)(self.start_x, self.start_y, event.x, event.y, fill=self.fill_color, outline='black', tags=("movable", "erasable", "shape"))




    def on_drag(self, event) -> None:
        """
        Updates the custom shapes's coords while dragging.
        """
        self.canvas.canvas.coords(self.dragged_shape, self.start_x, self.start_y, event.x, event.y)



    def on_release(self, event) -> None:
        """
        Finishes the drawing of the shapes.
        """
        self.canvas.canvas.coords(self.dragged_shape, self.start_x, self.start_y, event.x, event.y)
        self.drawn_shapes[self.dragged_shape] = self
