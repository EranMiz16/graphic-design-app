from tkinter import colorchooser, Scale, Button
import tkinter as tk


class Brush:
    """
    Class of brush object, can be used for illustration programs.
    """
    def __init__(self, color: str ='black', thickness: float =2.0) -> None:
        """
        A constructor of the brush object.
        """
        self.color = color
        self.thickness = thickness


    def choose_color(self) -> None:
        """
        Open a brush's color choosing dialog
        """
        color_code = colorchooser.askcolor(title="Choose Color")
        if color_code[1]:
            self.set_color(color_code[1])


            
    def set_color(self, color: str) -> None:
        """
        Sets a new brush's color
        """
        self.color = color



    def set_thickness(self) -> None:
        """
        Open a new thickness dialog with the user, gets new value and changes brush's thickness
        """
        def update_thickness() -> None:
            self.thickness = float(scale.get() / 10)
            thickness_dialog.destroy()

        thickness_dialog = tk.Toplevel()
        thickness_dialog.title("Set Thickness")


        scale = Scale(thickness_dialog, from_=0, to=100, orient='horizontal', label=f"Currrent Thickness: {self.thickness * 10}", length=300)
        scale.pack(padx=10, pady=10)

        ok_button = Button(thickness_dialog, text="OK", command=update_thickness)
        ok_button.pack()





