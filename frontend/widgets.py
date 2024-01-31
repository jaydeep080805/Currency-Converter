import customtkinter as ctk
from settings import *


class OptionMenu(ctk.CTkOptionMenu):
    def __init__(self, parent, **kwargs):
        super().__init__(master=parent, **kwargs)


class EntryBox(ctk.CTkEntry):
    def __init__(self, parent, **kwargs):
        super().__init__(master=parent, **kwargs)


class Frame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(master=parent, fg_color=TRANSPARENT, **kwargs)
