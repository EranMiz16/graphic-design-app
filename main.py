from canvas import DrawingCanvas
from brush import Brush
from shapes import Shapes
from text_box import TextBox
from file_manager import FileManager
from object_manipulator import ObjectManipulator
import tkinter as tk
import argparse


BUTTONS_BG = 'white'
FRAME_BG = 'light blue'


class MainWindow(tk.Tk):
    """
    Main Window class and main operator of graphic paintin and desing program.
    Containing all the GUI features (buttons, menus, etc.)
    """
    def __init__(self):
        """
        Constructor of main window of an illustraion and design progarm.
        This class handles widgets creation and transformation between modes.
        """

        super().__init__()
        self.title("Graphic Painting And Design Program ")
        self.geometry("1000x600")
        self.tooltip_window = None
        self.active_button = None

        self.modes_frame = tk.Frame(self, background=FRAME_BG)
        self.modes_frame.pack(side="top",fill=tk.BOTH, expand=False)
        self.buttons_frame = tk.Frame(self.modes_frame, bg=FRAME_BG)
        self.buttons_frame.pack(anchor='center')

        self.drawing_canvas = DrawingCanvas(self, width=800, height=600)
        self.brush = Brush()
        self.file_manager = FileManager(self.drawing_canvas)
        self.text_box = TextBox(self.drawing_canvas.canvas)
        self.shapes = Shapes(self.drawing_canvas)
        self.object_manipulator = ObjectManipulator(self.drawing_canvas, self.text_box, self.shapes, self.file_manager)


        self.drawing_canvas.set_brush(self.brush)
        self.tools_widgets()
        self.buttons_widgets()




    def create_button(self, frame, image_path, command, tooltip_text, pack_side="left", pack_padx=(0,5), image_subsample=8):
        """
        Create the buttons according to given variabels.
        """
        button_photo = tk.PhotoImage(file=image_path).subsample(image_subsample)
        button = tk.Button(frame, image=button_photo, command=command, bg=BUTTONS_BG)
        button.pack(side=pack_side, padx=pack_padx)
        self.create_tooltip(button, tooltip_text)
        button.image = button_photo 
        return button




    def buttons_widgets(self) -> None:
        """
        Creates the buttons for the varioud modes of the program.
        """
        self.bg_button = self.create_button(self.buttons_frame, "bg_image.png", lambda: self.modes_modifying('bg'), "Background \n Press to change the background's color.")
        
        self.brush_button = self.create_button(self.buttons_frame, "brush_image.png", lambda: self.modes_modifying("brush"), "Brush \n Press to move to brush mode.")
        
        self.eraser_button = self.create_button(self.buttons_frame, "eraser_image.png", lambda: self.modes_modifying("eraser"), "Eraser \n Press to move to eraser mode.", image_subsample=7)
        
        self.fill_button = self.create_button(self.buttons_frame, "fill_image.png", lambda: self.modes_modifying("fill"), "Fill \n Press to fill an object with color.")
        
        self.dots_button = self.create_button(self.buttons_frame, "dots_line.png", lambda: self.modes_modifying('dots'), "Dots \n Press to move to dots mode.")
        
        self.custom_rectangle_button = self.create_button(self.buttons_frame, "custom_rectangle.png", lambda: self.modes_modifying("custom_rectangle"), "Custom Rectangle \n Press left click and drag until desired size.")

        self.custom_oval_button = self.create_button(self.buttons_frame, "custom_circle.png", lambda: self.modes_modifying("custom_oval"), "Custom Oval \n Press left click and drag until desired size.", image_subsample=32)

        self.polygon_button = self.create_button(self.buttons_frame, "dots_polygon.png", lambda: self.modes_modifying("polygon"), "Polygon Maker \n Press left click for vertices, scroll wheel click for creation.", image_subsample=12)
        
        self.drag_button = self.create_button(self.buttons_frame, "drag_image.png", lambda: self.modes_modifying("drag"), "Drag Mode \n Press to drag objectes in the canvas.")
      
        self.text_button = self.create_button(self.buttons_frame, "text_image.png", lambda: self.modes_modifying("text"), "Text box \n Make a quick text box.")
        
        self.triangle_button = self.create_button(self.buttons_frame, "triangle_image.png", lambda: self.modes_modifying("triangle"), "Quick Triangle", image_subsample=7)

        self.oval_button = self.create_button(self.buttons_frame, "circle_image.png", lambda: self.modes_modifying("oval"), "Quick Circle", image_subsample=13)
        
        self.rectangle_button = self.create_button(self.buttons_frame, "square_image.png", lambda: self.modes_modifying("rectangle"), "Quick Square", image_subsample=16)
        


    def tools_widgets(self) -> None:
        """
        Create the menu bar, and the menus containing tools to the various of objects in the program.
        """

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0, background="light blue")
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.file_manager.reset_canvas_dialog)
        file_menu.add_command(label="Save", command=self.file_manager.save_to_file)
        file_menu.add_command(label="Load", command=self.file_manager.load_from_file)
        file_menu.add_command(label="Load Image", command=self.file_manager.open_image)
        file_menu.add_command(label="Export To jpeg", command=lambda: self.file_manager.export_to_graphic_file("JPEG"))
        file_menu.add_command(label="Export To GIF", command=lambda: self.file_manager.export_to_graphic_file("GIF"))


        brush_tools_menu = tk.Menu(self.menu_bar, tearoff=0, background="light blue")
        self.menu_bar.add_cascade(label="Brush Tools", menu=brush_tools_menu)
        brush_tools_menu.add_command(label="Change Color", command=self.brush.choose_color)
        brush_tools_menu.add_command(label="Change Thickness", command=self.brush.set_thickness)
        brush_tools_menu.add_command(label="Change Dot's Color", command=self.shapes.ask_for_dot_color)
        brush_tools_menu.add_command(label="Change Dots' Thickness", command=self.shapes.ask_for_dot_radius)

        eraser_menu = tk.Menu(self.menu_bar, tearoff=0, background="light blue")
        self.menu_bar.add_cascade(label='Eraser Size', menu=eraser_menu)
        eraser_menu.add_command(label='Choose Size', command=self.drawing_canvas.change_eraser_size)

        text_box_tools = tk.Menu(self.menu_bar, tearoff=0, background="light blue")
        self.menu_bar.add_cascade(label='Text Box', menu=text_box_tools)
        text_box_tools.add_command(label='Choose Font', command=self.text_box.choose_font_family)
        text_box_tools.add_command(label='Choose Color', command=self.text_box.choose_text_color)
        text_box_tools.add_command(label='Choose Size', command=self.text_box.choose_text_size)
        text_box_tools.add_command(label='Add Text Box', command=self.text_box.choose_text)


        shapes_menu = tk.Menu(self.menu_bar, tearoff=0, background="light blue")
        self.menu_bar.add_cascade(label="Shapes Tools", menu=shapes_menu)
        shapes_menu.add_command(label="Shape's Color", command= self.shapes.set_shape_color)
        shapes_menu.add_command(label="Cricle's Size", command=lambda: self.shapes.set_shape_size('oval'))
        shapes_menu.add_command(label="Rectangle's Size", command=lambda: self.shapes.set_shape_size('rectangle'))
        shapes_menu.add_command(label="Triangle's Size", command=lambda: self.shapes.set_shape_size('polygon'))
        shapes_menu.add_command(label="Fill Color", command= self.shapes.set_fill_color)





    def modes_modifying(self, mode: str) -> None:
        """
        Method that responsible of the transition between modes in the program.
        """
        self.drawing_canvas.clear_bindings()
        self.object_manipulator.unbind_objects()

        if self.active_button:
            self.active_button.config(bg=BUTTONS_BG)

        if mode in ['custom_rectangle', 'custom_oval']:
            shape = (mode.split('_'))[1]
            self.shapes.draw_shape_by_drag(shape)
            self.active_button = getattr(self, mode + '_button')


        elif mode in ['brush', 'eraser', 'fill']:
            getattr(self.drawing_canvas, 'set_mode')(mode)
            self.active_button = getattr(self, mode + '_button')


        elif mode in ['triangle', 'rectangle', 'oval', 'dots', 'polygon']:
            getattr(self.shapes, 'set_current_shape')(mode)
            self.active_button = getattr(self, mode + '_button')


        elif mode == 'drag':
            self.object_manipulator.bind_objects()
            self.active_button = getattr(self, mode + '_button')


        elif mode == 'bg':
            self.drawing_canvas.change_bg()
            self.active_button = getattr(self, mode + '_button')

        
        elif mode == 'text':
            self.text_box.choose_text()
            self.active_button = getattr(self, mode + '_button')


        if self.active_button:
            self.active_button.config(bg='gray')



        
    def create_tooltip(self, widget, text: str) -> None:
        """
        Attaches a tooltip to a widget.
        """
        def on_enter(event, self=self, text=text, widget=widget):
            self.show_tooltip(text, widget)
        def on_leave(event, self=self):
            self.hide_tooltip()

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)




    def show_tooltip(self, text: str, widget) -> None:
        """
        Make the tooltip to be shown near the widget.
        """
        if hasattr(self, 'tooltip_window'):
            self.hide_tooltip()

        self.tooltip_window = tk.Toplevel()
        self.tooltip_window.wm_overrideredirect(True)
        x = widget.winfo_rootx() + 20
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=text, background="light gray", borderwidth=1, relief="solid")
        label.pack()



    def hide_tooltip(self) -> None:
        """
        Closes the tooltip window when the mouse off the widget.
        """
        if hasattr(self, 'tooltip_window') and self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""This is graphic illustraion and design progarm.
                In this program you will be able to draw with line and shapes with special effects and uploading pictures.
                To be able to use this program, you have diffrent buttons (for modifying the various modes of the program),
                and menu for tools to change the features as you like (color, thickness, size, etc).
                Enjoy!""")        
    args = parser.parse_args()

    app = MainWindow()
    app.mainloop()