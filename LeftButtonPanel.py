from __future__ import print_function
from __future__ import division
from fractions import Fraction

from tkinter import *
import tkinter as tk

from PIL import Image, ImageDraw, ImageFont, ImageTk

import sys, os

import dot_globals as globals

# LeftButtonPanel Class
class LeftButtonPanel(tk.Frame):
    # def __init__(self, imOut, x, y, size, pixelsPerInch, maxHoleSize, fontSize, fontColor, flagDrawRanges, flagDrawSizes):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=25, bd=1, relief=RIDGE)
        # self.pack_propagate(False)
        self.pack(expand=1, anchor="nw")
        
        self.tickbox_sizes_var = IntVar()
        self.tickbox_sizes = Checkbutton(
            self, 
            text="Toggle Sizes",
            variable=self.tickbox_sizes_var,
            ) #command=self.tickbox_sizes_cb)
        self.tickbox_sizes.pack(side="top")
        
        w = tk.Label(self, text="left_button_frame", bg="green", fg="black")
        w.pack(side="top", expand=1, fill="y")
        
        # --- function end ---

# --------------------------- class end ---------------------------