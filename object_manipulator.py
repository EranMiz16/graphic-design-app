import tkinter as tk
from tkinter import messagebox
from canvas import DrawingCanvas
from shapes import Shapes
from text_box import TextBox
from file_manager import FileManager
from typing import Dict, Any, Optional, List
from PIL import Image, ImageTk


MOVABLE_TAG = "movable"

class ObjectManipulator:
    """
    A class that responsible all the obect manipulation, such
    as removing, moving, and special features to each kind of object.
    """
    def __init__(self, canvas: DrawingCanvas, text_box: TextBox, shapes: Shapes, images: FileManager) -> None:
        """
        A constructor for the object maniplator class.
        """
        self.canvas = canvas.canvas
        self.drawing_canvas = canvas
        self.text_box = text_box
        self.shapes = shapes
        self.images = images
        self.drag_data: Dict[str, Any] = {"item": None, "x": 0, "y": 0}

        self.grouped_items: Dict[int, Any] = {}
        self.item_to_group: Dict[int, Any] = {}
        self.clipboard: Optional[Any] = None
        self.current_item: Optional[Any] = None

        self.small_menu = tk.Menu(self.canvas, tearoff=0)
        self.small_menu.add_command(label="Remove", command=self.remove_item)
        self.canvas.bind("<Button-3>", self.right_click_menu)





    def bind_objects(self) -> None:
        """
        This method bind events by the tag: movable, in order to move objects.
        """
        self.canvas.tag_bind(MOVABLE_TAG, "<ButtonPress-1>", self.on_item_press)
        self.canvas.tag_bind(MOVABLE_TAG, "<ButtonRelease-1>", self.on_item_release)
        self.canvas.tag_bind(MOVABLE_TAG, "<B1-Motion>", self.on_item_move)


    def unbind_objects(self) -> None:
        """
        This method unbinds the events when user done moving.
        """
        self.canvas.tag_unbind(MOVABLE_TAG, "<ButtonPress-1>")
        self.canvas.tag_unbind(MOVABLE_TAG, "<ButtonRelease-1>")
        self.canvas.tag_unbind(MOVABLE_TAG, "<B1-Motion>")



    def raise_or_lower_item(self, item: int, command: str) -> None:
        """
        Raise or lower the selected item one level higher or lower in the stack.
        """
        if item:
            if item in self.drawing_canvas.item_to_segment_group:
                group = self.drawing_canvas.item_to_segment_group[item]
                for item in group:
                    getattr(self.canvas, f"tag_{command}")(item)
            else:
                getattr(self.canvas, f"tag_{command}")(item)





    def right_click_menu(self, event) -> None:
        """
        Show menu of features on objects, if the user right-clicks on or near an object.
        """
        self.small_menu.delete(0, tk.END)
        closest_item = self.canvas.find_closest(event.x, event.y, halo=1)[0]

        if closest_item is not None:
            item_tags = self.canvas.gettags(closest_item)
            bbox = self.canvas.bbox(closest_item)
            item_type = self.canvas.type(closest_item)

            if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                self.current_item = closest_item

                self.small_menu.add_command(label="Remove", command=self.remove_item)
                self.small_menu.add_command(label="Move To The Front", command=lambda: self.raise_or_lower_item(closest_item, 'raise'))
                self.small_menu.add_command(label="Move To The Back", command=lambda: self.raise_or_lower_item(closest_item, 'lower'))
                self.small_menu.add_command(label="Copy", command=lambda: self.copy_object(closest_item, item_type))
                    
                if "shape" in item_tags:
                    self.shape_options_menu(closest_item, item_type)

                elif "text_box" in item_tags:
                    self.text_options_menu(closest_item)

                elif "image" in item_tags:
                    self.image_options_menu(closest_item)
            else:
                self.background_options_menu()
        else:
            self.background_options_menu()

        self.small_menu.post(event.x_root, event.y_root)


    def text_options_menu(self, closest_item: int) -> None:
        self.small_menu.add_command(label="Bold", command=lambda: self.text_box.change_text_style(closest_item, 'bold'))
        self.small_menu.add_command(label="Italic", command=lambda: self.text_box.change_text_style(closest_item, 'italic'))
        self.small_menu.add_command(label="Change Text's Size", command=lambda: self.text_box.choose_text_size(closest_item))
        self.small_menu.add_command(label="Change Text's Color", command=lambda: self.text_box.choose_text_color(closest_item))
        self.small_menu.add_command(label="Change Text's Font", command=lambda: self.text_box.choose_font_family(closest_item))


    def shape_options_menu(self, closest_item: int, item_type: str) -> None:
        self.small_menu.add_command(label="Outline Color", command=lambda:  self.shapes.set_shape_color(closest_item))
        self.small_menu.add_command(label="Shape's Size", command=lambda:  self.shapes.set_shape_size(item_type, closest_item))
        self.small_menu.add_command(label="Fill Color", command=lambda:  self.shapes.set_fill_color(closest_item))


    def image_options_menu(self, closest_item: int) -> None:
        self.small_menu.add_command(label="Change Image's Size", command=lambda: self.images.image_manipulation(closest_item, 'resize'))
        self.small_menu.add_command(label="Rotate Image", command=lambda: self.images.image_manipulation(closest_item, 'rotate'))
        self.small_menu.add_command(label="Mirror Image", command=lambda: self.images.image_manipulation(closest_item, 'mirror'))
                    
    def background_options_menu(self) -> None:
        self.small_menu.add_command(label="Paste", command=self.paste_object)
        self.small_menu.add_command(label="Change Background", command=self.drawing_canvas.change_bg)



    def remove_item(self) -> None:
        """
        Remove the selected item from the canvas.
        """
        if self.current_item:
            item_tags = self.canvas.gettags(self.current_item)

            if "line" in item_tags:
                segment_group = self.drawing_canvas.item_to_segment_group.get(self.current_item)
                if segment_group:
                    for segment in segment_group:
                        self.canvas.delete(segment)
                        del self.drawing_canvas.item_to_segment_group[segment]

            else:          
                self.canvas.delete(self.current_item)

        self.current_item = None



    def on_item_press(self, event) -> None:
        """
        Executed when an item is pressed, drags the item.
        """
        item = self.canvas.find_closest(event.x, event.y)[0]
        item_tags = self.canvas.gettags(item)
        if MOVABLE_TAG in item_tags:
            if 'polygon' in item_tags:
                self.drag_data["item"] = next((line for line in self.shapes.drawn_dots if item in line), None)
                
            if 'line' in item_tags:
                segment_group = self.drawing_canvas.item_to_segment_group.get(item)
                if segment_group:
                    self.drag_data["item"] = segment_group
 
            else:
                if not self.drag_data["item"]:
                    self.drag_data["item"] = item

            self.drag_data["x"], self.drag_data["y"] = event.x, event.y




    def on_item_release(self, event) -> None:
        """
        Executed when the item being dragged is released, ends the drag.
        Resets the drag information.
        """
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0



    def on_item_move(self, event) -> None:
        """
        Executed when the item is being dragged.
        Updates the drag data.
        """
        if self.drag_data["item"]:
            index_x = event.x - self.drag_data["x"]
            index_y = event.y - self.drag_data["y"]


            if isinstance(self.drag_data["item"], int):
                self.canvas.move(self.drag_data["item"], index_x, index_y)

            else:
                for segment in self.drag_data["item"]:
                    self.canvas.move(segment, index_x, index_y)

            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y



    def copy_object(self, item: int, item_type: str) -> None:
        """
        Copying item and his attributes to a clipboard.
        """
        if item_type == 'line':
            self.clipboard = self.get_line_data(item)

        elif item_type == 'image':
            self.clipboard = {
                'type': 'image',
                'attributes': self.images.uploaded_images[item]}
            
        else:
            config = self.get_item_config(item, item_type)
            self.clipboard = {
                'type': item_type,
                'config': config,
                'coords': self.canvas.coords(item)}


    def get_line_data(self, item: int) -> Dict[str, Any]:
        """
        Collects full line's data, for copy and paste.
        """
        segments_data = []
        if item in self.drawing_canvas.item_to_segment_group:
            line_segments = self.drawing_canvas.item_to_segment_group[item]

            for segment in line_segments:

                segment_data = {
                    'coords': self.canvas.coords(segment),
                    'config': self.get_item_config(segment, 'line')}
                segments_data.append(segment_data)

        return {'type': 'line', 'segments': segments_data}




    def get_item_config(self, item: int, item_type: str) -> Dict[str, Any]:
        """
        This methods creates a dictonary with the configures details of an object.
        """
        if item_type == 'image':
            config = self.images.uploaded_images[item]

        else:
            config_options = self.canvas.itemconfig(item)
            if config_options:
                config = {option: self.canvas.itemcget(item, option) for option in config_options if self.canvas.itemcget(item, option)}

                if item_type == 'text':
                    config['text'] = self.canvas.itemcget(item, 'text')
                    config['font'] = self.canvas.itemcget(item, 'font')

        return config
    



    def paste_object(self) -> None:
        """
        Paste copied object.
        """
        if not self.clipboard:
            return
    
        item_type = self.clipboard.get('type')

        if item_type == 'line':
            self.paste_line()

        elif item_type == "image":
            self.paste_image()

        else:

            adjusted_coords = [coord + 100 for coord in self.clipboard['coords']]
            if item_type in ['line', 'rectangle', 'oval', 'polygon', 'text', 'triangle']:
                getattr(self.canvas, 'create_' + item_type)(*adjusted_coords, **self.clipboard['config'])
            


    def paste_image(self) -> None:
        """
        Pastes an image into the canvas.
        """
        if self.clipboard is not None:
            file_path = self.clipboard["attributes"]['path']
            image_size = self.clipboard["attributes"]['size']
            rotation = self.clipboard["attributes"]['rotation']

            try:
                image = Image.open(file_path)

                if rotation != 0:
                    image = image.rotate(rotation, expand=True)

                image.thumbnail(image_size)
                photo_image = ImageTk.PhotoImage(image)
                image_id = self.canvas.create_image((100, 100), image=photo_image, anchor='center', tags=("image", "movable"))
                self.images.uploaded_images[image_id] = {'photo_image': photo_image, 'path': file_path, 'size': image_size, 'rotation': rotation}
            
            except Exception as error:
                messagebox.showerror("Error", f"Failed to paste image. Error: {error}")



    def paste_line(self):
        """
        Pastes full line to the canvas.
        """
        if self.clipboard:
            previous_end_coords = None
            segments_lst = []
            for segment_data in self.clipboard['segments']:

                if previous_end_coords:
                    dx = previous_end_coords[2] - segment_data['coords'][0]
                    dy = previous_end_coords[3] - segment_data['coords'][1]
                    adjusted_coords = [segment_data['coords'][0] + dx, segment_data['coords'][1] + dy, segment_data['coords'][2] + dx, segment_data['coords'][3] + dy]
                
                else:
                    adjusted_coords = [coord + 100 for coord in segment_data['coords']]
                
                currnet_line = self.canvas.create_line(*adjusted_coords, **segment_data['config'])
                segments_lst.append(currnet_line)
                self.drawing_canvas.item_to_segment_group[currnet_line] = segments_lst
                previous_end_coords = adjusted_coords
            