from __future__ import print_function
from __future__ import division
from fractions import Fraction

# from tkinter import *
# import tkinter as tk

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
    import Tkinter as tk
except ImportError:
    # for Python3
    from tkinter import *   ## notice here too
    import Tkinter as tk

# from PIL import Image, ImageDraw, ImageFont, ImageTk
from PIL import Image, ImageDraw, ImageFont, ImageTk

import sys, os

import dottizerFunctions as df
import dot_globals as globals
import LeftButtonPanel as lbp

class Dottizer(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()

        # Generate available drill sizes
        globals.generate_global_drill_sizes()

        # Create Dot Panel
        self.dot_image = df.DotPanel(globals.input_image,
                                    globals.drill_sizes,
                                    globals.dist_between_holes,
                                    globals.border_x,
                                    globals.border_y,
                                    globals.dots_wide,
                                    globals.pixels_per_inch,
                                    globals.font_size,
                                    globals.font_color,
                                    globals.grid_color,
                                    globals.inset_border_color,
                                    False,
                                    False,
                                    False,
                                    False)
        # self.dot_image.draw()

        self.create_widgets()

    def create_widgets(self):

        # Output Image Window
        # self.image_window = Toplevel()
        # self.image_window.geometry(str(globals.out_view_x) + 'x' + str(globals.out_view_y))
        # self.image_window.title("Dottizer Image Output")
        # self.image_window.protocol("WM_DELETE_WINDOW", self.master.destroy)     # Allows output image window to also close program when X button is hit

        # w = tk.Label(self.image_window, text="image_window", bg="blue", fg="white")
        # w.pack(expand=1, fill="both")



        # Entry box for dots_wide
        Label(self, text="Dots Wide:").grid(column=0, columnspan=2, sticky=E)
        self.entry_dots_wide = Entry(self)
        self.entry_dots_wide.grid(row=0, column=2, columnspan=2, sticky=W)
        self.entry_dots_wide.insert(0,"50")
        self.entry_dots_wide.bind("<Return>",self.validate_dots_wide)
        self.entry_dots_wide.bind("<Tab>",self.validate_dots_wide)

        # Entry box for dist_between_holes
        Label(self, text="Hole Spacing:").grid(column=0, columnspan=2, sticky=E)
        self.entry_dist_between_holes = Entry(self)
        self.entry_dist_between_holes.grid(row=1, column=2, columnspan=2, sticky=W)
        self.entry_dist_between_holes.insert(0,"0.4")
        self.entry_dist_between_holes.bind("<Return>",self.validate_dist_between_holes)
        self.entry_dist_between_holes.bind("<Tab>",self.validate_dist_between_holes)

        # Ranges Tickbox
        self.tickbox_ranges_var = IntVar()
        self.tickbox_ranges = Checkbutton(
            self,
            text="Toggle Ranges",
            variable=self.tickbox_ranges_var,
            command=self.tickbox_ranges_CB)
        self.tickbox_ranges.grid(columnspan=4)

        # Sizes Tickbox
        self.tickbox_sizes_var = IntVar()
        self.tickbox_sizes = Checkbutton(
            self,
            text="Toggle Sizes",
            variable=self.tickbox_sizes_var,
            command=self.tickbox_sizes_CB)
        self.tickbox_sizes.grid(columnspan=4)

        # Invert Tickbox
        self.tickbox_invert_var = IntVar()
        self.tickbox_invert = Checkbutton(
            self,
            text="Invert Colors",
            variable=self.tickbox_invert_var,
            command=self.tickbox_invert_CB)
        self.tickbox_invert.grid(columnspan=4)

        # Draw Grid Tickbox
        self.tickbox_grid_var = IntVar()
        self.tickbox_grid = Checkbutton(
            self,
            text="Draw Grid",
            variable=self.tickbox_grid_var,
            command=self.tickbox_grid_CB)
        self.tickbox_grid.grid(columnspan=4)

        # ======================================
        # Drill Size Tickboxes
        # ======================================

        # Label
        Label(self, text="Available Drill Bits").grid(column=0, columnspan = 4, sticky=W)

        # Use 1" Tickbox
        self.tickbox_1_1_bit_var = IntVar()
        self.tickbox_1_1_bit_var.set(globals.optional_drill_sizes[12][1])
        self.tickbox_1_1_bit = Checkbutton(
            self,
            text="1\"",
            variable=self.tickbox_1_1_bit_var,
            command=self.tickbox_1_1_bit_CB)
        self.tickbox_1_1_bit.grid(column=0, sticky=W)

        # Use 7/8" Tickbox
        self.tickbox_7_8_bit_var = IntVar()
        self.tickbox_7_8_bit_var.set(globals.optional_drill_sizes[11][1])
        self.tickbox_7_8_bit = Checkbutton(
            self,
            text="7/8\"",
            variable=self.tickbox_7_8_bit_var,
            command=self.tickbox_7_8_bit_CB)
        self.tickbox_7_8_bit.grid(row=7, column=1, sticky=W)

        # Use 3/4" Tickbox
        self.tickbox_3_4_bit_var = IntVar()
        self.tickbox_3_4_bit_var.set(globals.optional_drill_sizes[10][1])
        self.tickbox_3_4_bit = Checkbutton(
            self,
            text="3/4\"",
            variable=self.tickbox_3_4_bit_var,
            command=self.tickbox_3_4_bit_CB)
        self.tickbox_3_4_bit.grid(row=7, column=2, sticky=W)

        # Use 5/8" Tickbox
        self.tickbox_5_8_bit_var = IntVar()
        self.tickbox_5_8_bit_var.set(globals.optional_drill_sizes[9][1])
        self.tickbox_5_8_bit = Checkbutton(
            self,
            text="5/8\"",
            variable=self.tickbox_5_8_bit_var,
            command=self.tickbox_5_8_bit_CB)
        self.tickbox_5_8_bit.grid(row=7, column=3, sticky=W)

        # Use 1/2" Tickbox
        self.tickbox_1_2_bit_var = IntVar()
        self.tickbox_1_2_bit_var.set(globals.optional_drill_sizes[8][1])
        self.tickbox_1_2_bit = Checkbutton(
            self,
            text="1/2\"",
            variable=self.tickbox_1_2_bit_var,
            command=self.tickbox_1_2_bit_CB)
        self.tickbox_1_2_bit.grid(column=0, sticky=W)

        # Use 3/8" Tickbox
        self.tickbox_3_8_bit_var = IntVar()
        self.tickbox_3_8_bit_var.set(globals.optional_drill_sizes[7][1])
        self.tickbox_3_8_bit = Checkbutton(
            self,
            text="3/8\"",
            variable=self.tickbox_3_8_bit_var,
            command=self.tickbox_3_8_bit_CB)
        self.tickbox_3_8_bit.grid(row=8, column=1, sticky=W)

        # Use 5/16" Tickbox
        self.tickbox_5_16_bit_var = IntVar()
        self.tickbox_5_16_bit_var.set(globals.optional_drill_sizes[6][1])
        self.tickbox_5_16_bit = Checkbutton(
            self,
            text="5/16\"",
            variable=self.tickbox_5_16_bit_var,
            command=self.tickbox_5_16_bit_CB)
        self.tickbox_5_16_bit.grid(row=8, column=2, sticky=W)

        # Use 1/4" Tickbox
        self.tickbox_1_4_bit_var = IntVar()
        self.tickbox_1_4_bit_var.set(globals.optional_drill_sizes[5][1])
        self.tickbox_1_4_bit = Checkbutton(
            self,
            text="1/4\"",
            variable=self.tickbox_1_4_bit_var,
            command=self.tickbox_1_4_bit_CB)
        self.tickbox_1_4_bit.grid(row=8, column=3, sticky=W)

        # Use 3/16" Tickbox
        self.tickbox_3_16_bit_var = IntVar()
        self.tickbox_3_16_bit_var.set(globals.optional_drill_sizes[4][1])
        self.tickbox_3_16_bit = Checkbutton(
            self,
            text="3/16\"",
            variable=self.tickbox_3_16_bit_var,
            command=self.tickbox_3_16_bit_CB)
        self.tickbox_3_16_bit.grid(column=0, sticky=W)

        # Use 5/32" Tickbox
        self.tickbox_5_32_bit_var = IntVar()
        self.tickbox_5_32_bit_var.set(globals.optional_drill_sizes[3][1])
        self.tickbox_5_32_bit = Checkbutton(
            self,
            text="5/32\"",
            variable=self.tickbox_5_32_bit_var,
            command=self.tickbox_5_32_bit_CB)
        self.tickbox_5_32_bit.grid(row=9, column=1, sticky=W)

        # Use 9/64" Tickbox
        self.tickbox_9_64_bit_var = IntVar()
        self.tickbox_9_64_bit_var.set(globals.optional_drill_sizes[2][1])
        self.tickbox_9_64_bit = Checkbutton(
            self,
            text="9/64\"",
            variable=self.tickbox_9_64_bit_var,
            command=self.tickbox_9_64_bit_CB)
        self.tickbox_9_64_bit.grid(row=9, column=2, sticky=W)

        # Use 1/8" Tickbox
        self.tickbox_1_8_bit_var = IntVar()
        self.tickbox_1_8_bit_var.set(globals.optional_drill_sizes[1][1])
        self.tickbox_1_8_bit = Checkbutton(
            self,
            text="1/8\"",
            variable=self.tickbox_1_8_bit_var,
            command=self.tickbox_1_8_bit_CB)
        self.tickbox_1_8_bit.grid(row=9, column=3, sticky=W)

        # info_text_box
        self.info_text_box = Label(self, justify="left", relief=SUNKEN)
        self.set_info_text()
        self.info_text_box.grid(columnspan=4)

        # Reload Button
        self.reload_button = tk.Button(self, text="Reload Input", command=self.reload_src_image)
        self.reload_button.grid(row=11, column=0)

        # Save Button
        self.reload_button = tk.Button(self, text="Save Output", command=self.save_out_image)
        self.reload_button.grid(row=11, column=1)

        # Source Image view
        self.src_view = Label(self)
        self.src_view.grid(row=12, columnspan=4)

        # Output Image view
        self.out_view = Label(self)
        # self.out_view.pack(side="left", expand=1, fill="both")
        self.out_view.grid(row=0, column=4, rowspan=13, sticky=W)
        # Finally draw!
        # self.redraw_out_view()
        self.reload_src_image()

    def validate_dots_wide(self,event):
        """ Someone Pressed Enter or Tab """
        s = self.entry_dots_wide.get()
        print("You entered >> " + s )
        try:
            val = int(s)
            if((val > 0) & (val < 200)):
                print('dots: ' + str(val))
                # self.dot_image.set_new_dotWidth( int(val) )
                self.dot_image.dots_wide = val
                self.redraw_out_view()
            else:
                self.entry_dots_wide.delete(0, END)
                self.entry_dots_wide.insert(0,self.dot_image.dots_wide)

        except ValueError:
            print('"' + s + '" is not an integer input!')
            self.entry_dots_wide.delete(0, END)
            self.entry_dots_wide.insert(0,self.dot_image.dots_wide)

    def validate_dist_between_holes(self,event):
        """ Someone Pressed Enter or Tab """
        s = self.entry_dist_between_holes.get()
        print("You entered >> " + s )
        try:
            val = float(s)
            if(val >= 0):
                print('dist between holes: ' + str(val))
                # self.dot_image.set_new_dotWidth( int(val) )
                self.dot_image.dist_between_holes = val
                self.redraw_out_view()
            else:
                self.entry_dist_between_holes.delete(0, END)
                self.entry_dist_between_holes.insert(0,self.dot_image.dist_between_holes)

        except ValueError:
            print('"' + s + '" is not a float input!')
            self.entry_dist_between_holes.delete(0, END)
            self.entry_dist_between_holes.insert(0,self.dot_image.dist_between_holes)

    def redraw_out_view(self):
        self.dot_image.draw()

        temp_image = self.dot_image.out_image.copy()
        temp_image.thumbnail((globals.out_view_x, globals.out_view_y), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(temp_image)
        self.out_view.configure(image=photo)
        self.out_view.image = photo # keep a reference!
        # self.srcView.pack(side="left")
        del photo
        self.set_info_text()

    def reload_src_image(self):
        self.dot_image.reload_image()

        temp_image = self.dot_image.src_image.copy()
        temp_image.thumbnail((320, 240), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(temp_image)
        self.src_view.configure(image=photo)
        self.src_view.image = photo # keep a reference!

        self.redraw_out_view()







        # self.setDotWidth()

        # temp_image = self.dot_image.srcImage
        # temp_image.thumbnail((srcViewX, srcViewY), Image.ANTIALIAS)
        # photo = ImageTk.PhotoImage(temp_image)
        # self.srcView.configure(image=photo)
        # self.srcView.image = photo # keep a reference!
        # self.srcView.pack(side="left")

        # temp_image = self.dot_image.outImage
        # temp_image.thumbnail((outViewX, outViewY), Image.ANTIALIAS)
        # photo = ImageTk.PhotoImage(temp_image)
        # self.outView.configure(image=photo)
        # self.outView.image = photo # keep a reference!
        # self.srcView.pack(side="left")

        # del photo

    def save_out_image(self):
        temp_dot_panel = df.DotPanel(self.dot_image.input_image,
                                    self.dot_image.drill_sizes,
                                    self.dot_image.dist_between_holes,
                                    self.dot_image.border_x,
                                    self.dot_image.border_y,
                                    self.dot_image.dots_wide,
                                    globals.pixels_per_inch_render,                                    # pixels per inch
                                    self.dot_image.font_size,
                                    self.dot_image.font_color,
                                    self.dot_image.grid_color,
                                    self.dot_image.inset_border_color,
                                    self.dot_image.flag_draw_ranges,
                                    self.dot_image.flag_draw_sizes,
                                    self.dot_image.flag_invert_colors,
                                    self.dot_image.flag_draw_grid)

        temp_dot_panel.draw()
        temp_dot_panel.out_image.save('out.png')

        del temp_dot_panel

    def tickbox_ranges_CB(self):

        val = self.tickbox_ranges_var.get()
        print('variable is' + str(val))
        if val == 1:
            self.dot_image.flag_draw_ranges = True
        else:
            self.dot_image.flag_draw_ranges = False
        self.redraw_out_view()

    def tickbox_sizes_CB(self):

        val = self.tickbox_sizes_var.get()
        print('variable is' + str(val))
        if val == 1:
            self.dot_image.flag_draw_sizes = True
        else:
            self.dot_image.flag_draw_sizes = False
        self.redraw_out_view()

    def tickbox_invert_CB(self):

        val = self.tickbox_invert_var.get()
        print('variable is' + str(val))
        if val == 1:
            self.dot_image.flag_invert_colors = True
        else:
            self.dot_image.flag_invert_colors = False
        self.redraw_out_view()

    def tickbox_grid_CB(self):

        val = self.tickbox_grid_var.get()
        print('variable is' + str(val))
        if val == 1:
            self.dot_image.flag_draw_grid = True
        else:
            self.dot_image.flag_draw_grid = False
        self.redraw_out_view()

    # Callback for tickbox_1_1_bit tickbox
    def tickbox_1_1_bit_CB(self):
        val = self.tickbox_1_1_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[12][1] = True
        else:
            globals.optional_drill_sizes[12][1] = False
        self.redraw_out_view()

    # Callback for tickbox_7_8_bit tickbox
    def tickbox_7_8_bit_CB(self):
        val = self.tickbox_7_8_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[11][1] = True
        else:
            globals.optional_drill_sizes[11][1] = False
        self.redraw_out_view()

    # Callback for tickbox_3_4_bit tickbox
    def tickbox_3_4_bit_CB(self):
        val = self.tickbox_3_4_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[10][1] = True
        else:
            globals.optional_drill_sizes[10][1] = False
        self.redraw_out_view()

    # Callback for tickbox_5_8_bit tickbox
    def tickbox_5_8_bit_CB(self):
        val = self.tickbox_5_8_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[9][1] = True
        else:
            globals.optional_drill_sizes[9][1] = False
        self.redraw_out_view()

    # Callback for tickbox_1_2_bit tickbox
    def tickbox_1_2_bit_CB(self):
        val = self.tickbox_1_2_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[8][1] = True
        else:
            globals.optional_drill_sizes[8][1] = False
        self.redraw_out_view()

    # Callback for tickbox_3_8_bit tickbox
    def tickbox_3_8_bit_CB(self):
        val = self.tickbox_3_8_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[7][1] = True
        else:
            globals.optional_drill_sizes[7][1] = False
        self.redraw_out_view()

    # Callback for tickbox_5_16_bit tickbox
    def tickbox_5_16_bit_CB(self):
        val = self.tickbox_5_16_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[6][1] = True
        else:
            globals.optional_drill_sizes[6][1] = False
        self.redraw_out_view()

    # Callback for tickbox_1_4_bit tickbox
    def tickbox_1_4_bit_CB(self):
        val = self.tickbox_1_4_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[5][1] = True
        else:
            globals.optional_drill_sizes[5][1] = False
        self.redraw_out_view()

    # Callback for tickbox_3_16_bit tickbox
    def tickbox_3_16_bit_CB(self):
        val = self.tickbox_3_16_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[4][1] = True
        else:
            globals.optional_drill_sizes[4][1] = False
        self.redraw_out_view()

    # Callback for tickbox_5_32_bit tickbox
    def tickbox_5_32_bit_CB(self):
        val = self.tickbox_5_32_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[3][1] = True
        else:
            globals.optional_drill_sizes[3][1] = False
        self.redraw_out_view()

    # Callback for tickbox_9_64_bit tickbox
    def tickbox_9_64_bit_CB(self):
        val = self.tickbox_9_64_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[2][1] = True
        else:
            globals.optional_drill_sizes[2][1] = False
        self.redraw_out_view()

    # Callback for tickbox_1_8_bit tickbox
    def tickbox_1_8_bit_CB(self):
        val = self.tickbox_1_8_bit_var.get()
        print('variable is' + str(val))
        if val == 1:
            globals.optional_drill_sizes[1][1] = True
        else:
            globals.optional_drill_sizes[1][1] = False
        self.redraw_out_view()

    # updates info_text_box with new info
    def set_info_text(self):

        self.info_text_box["text"] = 'Image Info:\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Input File:    ' + self.dot_image.input_image + '\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Input Dimensions: ' + str(self.dot_image.src_x) + ' x ' + str(self.dot_image.src_y) + '\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Image Format:  ' + self.dot_image.src_image.format + '\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Image Mode:    ' + self.dot_image.src_image.mode + '\n\n'

        #Print Grid Info
        self.info_text_box["text"] = self.info_text_box["text"] + 'Using the following grid parameters:\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Grid Width:    ' + str(self.dot_image.dots_wide) + ' dots\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Grid Height:    ' + str(self.dot_image.dots_tall) + ' dots\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Grid Border X:    ' + str(self.dot_image.border_x) + ' inches\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Grid Border Y:    ' + str(self.dot_image.border_y) + ' inches\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Max Hole Size:    ' + str(self.dot_image.max_hole_size) + ' inches\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Grid Spacing (edge to edge):    ' + str(self.dot_image.dist_between_holes) + ' inches\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Grid Spacing (dot to dot):    ' + str(self.dot_image.grid_spacing) + ' inches\n\n'
        self.info_text_box["text"] = self.info_text_box["text"] + '    Number of dots:    ' + str(self.dot_image.dot_count) + ' dots\n\n'


        #Print Physical Dimensions
        self.info_text_box["text"] = self.info_text_box["text"] + 'Physical Dimensions:    ' + str(self.dot_image.dots_wide*self.dot_image.max_hole_size + (self.dot_image.dots_wide-1)*self.dot_image.dist_between_holes + 2*self.dot_image.border_x) + '" x ' + str(self.dot_image.dots_tall*self.dot_image.max_hole_size + (self.dot_image.dots_tall-1)*self.dot_image.dist_between_holes + 2*self.dot_image.border_y) + '"\n\n'

        #Print available drill sizes
        self.info_text_box["text"] = self.info_text_box["text"] + 'Using the following drill sizes:\n'
        for i in self.dot_image.drill_sizes:
            #     + '    ' + str(Fraction(str(i[0]))) + '"'
                self.info_text_box["text"] = self.info_text_box["text"] + '    ' + str(Fraction(str(i[0]))) + '"     (' + str(i[1]) + ' scaled)\n'
    # --- function end ---


# ==============================================================================
# Script Start
# ==============================================================================

root = tk.Tk()
# root.geometry("1280x720")
root.title("Dottizer Controls")
app = Dottizer(master=root)
app.mainloop()