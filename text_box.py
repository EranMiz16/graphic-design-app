import tkinter as tk
from tkinter import simpledialog, colorchooser, font, Canvas
from typing import Dict, Tuple, List, Optional, Any


class TextBox:
    """
    A class that responsible of text box creation and modifying them.
    """
    def __init__(self, canvas: Canvas, index_x: int=500, index_y: int=200, text: str="Text", font: Tuple=("Helvetica", 14), color: str="black"):
        """
        A constructor to the text box class.
        """
        self.canvas = canvas
        self.x = index_x
        self.y = index_y
        self.text = text
        self.font = font
        self.color = color

        self.text_styles: Dict[int, Dict[str, bool]] = {}
        self.text_boxes: Dict[int, Dict[str, Any]] = {}
        
        
    def update_text(self, new_text: str) -> None:
        """
        This method updates the text value if created.
        """
        self.text = new_text



    def update_color(self, new_color: str) -> None:
        """
        This method updates the text's color.
        """
        self.color = new_color
        


    def choose_text(self) -> None:
        """
        This method creates a dailog for new text creation.
        """
        new_text = simpledialog.askstring("Text Box", "Enter new text:", parent=self.canvas)
        if new_text:
            self.update_text(new_text)
            self.create_text_box()



    def choose_text_color(self, clicked_text: Optional[int] =None) -> None:
        """
        This method creates a dailog text's color change.
        """
        new_color = colorchooser.askcolor(title="Choose text color")[1]
        if new_color:

            if clicked_text:
                self.canvas.itemconfig(clicked_text, fill=new_color)

            else:
                self.update_color(new_color)   



    def choose_text_size(self, clicked_text: Optional[int] =None) -> None:
        """
        This method creates a dailog for new text size.
        """        
        size = simpledialog.askinteger("Input", "Enter font size: (from 1: to 400)", parent=self.canvas, minvalue=1, maxvalue=400)
        if size:

            if clicked_text:
                font_attributes = self.text_font_sync(clicked_text)
                font_attributes[1] = size
                self.canvas.itemconfig(clicked_text, font=tuple(font_attributes))

            else:
                self.font = (self.font[0], size)




    def create_text_box(self) -> None:
        """
        This method creates a the id for new text box created.
        Stores it in a dictionary.
        """
        text_id = self.canvas.create_text(
        self.x, 
        self.y, 
        text=self.text, 
        font=self.font, 
        fill=self.color, 
        tags=("movable", "erasable", "text_box"))
        self.text_boxes[text_id] = {"text": self.text, "font": self.font, "fill": self.color}
        self.text_styles[text_id] = {"bold": False, "italic": False}


    
    def split_text_font_attributes(self, clicked_text: int) -> Tuple[str, Optional[int], Optional[str], Optional[str]]:
        """
        This method will help to keep track on text's font attributes.
        """
        font_attr_string = self.canvas.itemcget(clicked_text, "font")
        font_attributes = font_attr_string.split()
        
        font_name_parts: List[str]= []
        font_size: Optional[int] = None
        font_style_1: Optional[str] = None
        font_style_2: Optional[str]

        for attr in font_attributes:
            if attr.isdigit():
                font_size = attr
                break 
            else:
                font_name_parts.append(attr)
        
        font_name = " ".join(font_name_parts)
        
        size_index = font_attributes.index(str(font_size))
        styles = font_attributes[size_index + 1:]
        
        font_style_1 = styles[0] if len(styles) > 0 else None
        font_style_2 = styles[1] if len(styles) > 1 else None
        
        return font_name, font_size, font_style_1, font_style_2



    def text_font_sync(self, clicked_text: int) -> List[Any]:
        """
        Making list of font attirbutes of text box.
        """
        font_name, font_size, font_style_1, font_style_2 = self.split_text_font_attributes(clicked_text)
        font_attributes: List[Any] = [font_name, font_size]

        if self.text_styles[clicked_text]["bold"]:
            font_attributes.append("bold")

        if self.text_styles[clicked_text]["italic"]:
            font_attributes.append("italic")
        
        return font_attributes




    def change_text_style(self, clicked_text: int, style: str) -> None:
        """
        This method changes the text's style to bold or italic.
        """
        if clicked_text not in self.text_styles:
            self.text_styles[clicked_text] = {"bold": False, "italic": False}

        self.text_styles[clicked_text][style] = not self.text_styles[clicked_text][style]
        font_attributes = self.text_font_sync(clicked_text)

        self.canvas.itemconfig(clicked_text, font=tuple(font_attributes))



    def choose_font_family(self, clicked_text: Optional[int] =None) -> None:
        """
        This method open window of scroll bar for font choosing.
        """
        self.font_window = tk.Toplevel(self.canvas)
        self.font_window.title("Choose Font")
        

        self.font_listbox = tk.Listbox(self.font_window)
        self.font_listbox.pack(side="right", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.font_window, orient="vertical", command=self.font_listbox.yview)
        scrollbar.pack(side="top", fill="y")
        self.font_listbox.config(yscrollcommand=scrollbar.set)

        for family in font.families():
            self.font_listbox.insert("end", family)
        self.font_listbox.bind("<<ListboxSelect>>", lambda event: self.update_font(event, clicked_text))



    def update_font(self, event=None, clicked_text: Optional[int] =None) -> None:
        """
        This method updates the font attribute of the text.
        """
        if not self.font_listbox.curselection():
            return
        
        selected_font = self.font_listbox.get(self.font_listbox.curselection())
        if clicked_text:
            font_attributes = self.text_font_sync(clicked_text)
            font_attributes[0] = selected_font
            self.canvas.itemconfig(clicked_text, font=tuple(font_attributes))

        else:
            self.font = selected_font
        self.font_window.destroy()

    

