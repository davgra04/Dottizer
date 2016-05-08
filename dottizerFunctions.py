# This file contains a set of functions that will create a python image object.
# This object can then be used with PIL, or converted to a Tkinter PhotoImage
# object for use in a GUI

from __future__ import print_function
from __future__ import division
from fractions import Fraction
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sys, os

import dot_globals as globals






# ==============================================================================
# Objects
# ==============================================================================

# Drill Hole Class
class DrillHole:
    def __init__(self, out_image, x, y, size, pixels_per_inch, max_hole_size, font_size, font_color, flag_draw_ranges, flag_draw_sizes):
        self.xInches        = x
        self.yInches        = y
        self.size_inches     = size
        self.pixels_per_inch  = pixels_per_inch
        self.out_image          = out_image

        self.x = x * pixels_per_inch
        self.y = y * pixels_per_inch
        self.size = size * pixels_per_inch

        self.max_hole_size = max_hole_size

        self.flag_draw_ranges = flag_draw_ranges
        self.flag_draw_sizes = flag_draw_sizes


        self.font = ImageFont.truetype("RobotoMono-Regular.ttf", font_size)
        # self.font = ImageFont.truetype("cour.ttf", font_size)
        self.font_color = font_color
    # --- function end ---

    def draw(self):
        if self.size == 0.0:
            return

        draw = ImageDraw.Draw(self.out_image)
        # Draw range
        if self.flag_draw_ranges:
            draw.ellipse((self.x - (self.max_hole_size*self.pixels_per_inch/2.0), self.y - (self.max_hole_size*self.pixels_per_inch/2.0), self.x + (self.max_hole_size*self.pixels_per_inch/2.0), self.y + (self.max_hole_size*self.pixels_per_inch/2.0)), outline=(255, 255, 255, 255))
        # Draw individual dot
        draw.ellipse((self.x - (self.size/2.0), self.y - (self.size/2.0), self.x + (self.size/2.0), self.y + (self.size/2.0)), fill=(0, 80, 255, 255))
        # Draw text size
        if self.size > 1.0:
            sizeText = str(Fraction(str(self.size_inches))) + '"'
            # draw.text((self.x, self.y), sizeText, fill=(255,255,255,255), font=font)
            if self.flag_draw_sizes:
                draw.text((self.x - (self.max_hole_size*self.pixels_per_inch/2.0), self.y - (self.max_hole_size*self.pixels_per_inch/2.0)), str(Fraction(str(self.size_inches))) + '"', fill=self.font_color, font=self.font)


        del draw
    # --- function end ---
# --------------------------- class end ---------------------------

# DotPanel Class
class DotPanel:
    def __init__(self, input_image, drill_sizes, dist_between_holes, border_x, border_y, dots_wide, pixels_per_inch, font_size, font_color, grid_color, inset_border_color, flag_draw_ranges, flag_draw_sizes, flag_invert_colors, flag_draw_grid):

        self.input_image          = input_image             # input image for dottizing
        self.dist_between_holes   = dist_between_holes      # the distance between holes (edge to edge in inches)
        self.border_x             = border_x                # border width (in inches)
        self.border_y             = border_y                # border height (in inches)
        self.dots_wide            = dots_wide               # number of drill holes wide the image should be
        self.pixels_per_inch      = pixels_per_inch         # scaling of rendered image
        self.font_size            = font_size               # size of global font
        self.font_color           = font_color              # color of font
        self.grid_color           = grid_color              # color of background dot grid
        self.inset_border_color   = inset_border_color      # color of edge border line
        self.original_drill_sizes = globals.drill_sizes             # Temp storage for later calculating weights of drill sizes

        # Drawing flags
        self.flag_draw_ranges = flag_draw_ranges
        self.flag_draw_sizes = flag_draw_sizes
        self.flag_invert_colors = flag_invert_colors
        self.flag_draw_grid = flag_draw_grid

        self.dot_count = 0

        self.calculate_params()
    # --- function end ---

    # Initializes calculated values (that might need recalculation)
    def calculate_params(self):
        # Open image
        self.src_image   = Image.open(self.input_image)
        self.src_x       = self.src_image.size[0]
        self.src_y       = self.src_image.size[1]

        # number of drill holes tall the image should be
        self.dots_tall       = int(self.dots_wide * self.src_y / self.src_x)

        globals.generate_global_drill_sizes()
        self.original_drill_sizes = globals.drill_sizes
        self.max_hole_size    = max(self.original_drill_sizes)                    #inches
        print('max hole size: ' + str(self.max_hole_size))

        if self.pixels_per_inch == 0:
            self.pixels_per_inch = 640 / (self.dots_wide*self.max_hole_size + (self.dots_wide-1)*self.dist_between_holes + 2*self.border_x)

        # output image and dimensions
        self.out_x       = int((self.dots_wide*self.max_hole_size + (self.dots_wide-1)*self.dist_between_holes + 2*self.border_x ) * self.pixels_per_inch)
        self.out_y       = int((self.dots_tall*self.max_hole_size + (self.dots_tall-1)*self.dist_between_holes + 2*self.border_y ) * self.pixels_per_inch)
        self.out_image   = Image.new("RGBA", (self.out_x, self.out_y), "black")

        self.grid_spacing    = self.max_hole_size + self.dist_between_holes    #inches
        # Create combined drill_sizes array/tuple
        self.drill_sizes     = []                            # available drill bits when creating images
        for x in self.original_drill_sizes:
            self.drill_sizes.append( (x, x * 255.0 / self.max_hole_size) )
    # --- function end ---


    # Function for determining nearest drill size (rounds up)
    def find_nearest_drill_size(self, pixel_value):
        if pixel_value == 0.0:
            return 0.0
        #determine drill size
        lowest_diff = 9999999.0
        diff = 0.0
        return_size = 0.0
        # print('about to iterate through drill_sizesCombined')
        for size in self.drill_sizes:
            # print('comparing to size: ' + str(size[1]))
            diff = abs((pixel_value - size[1]))
            if diff < lowest_diff:
                lowest_diff = diff
                return_size = size[0]
        # print('pixel value: ' + str(pixel_value) + '        diff: ' + str(lowest_diff) + '        return size: ' + str(return_size))

        return return_size
    # --- function end ---

    # Draws holes, grid, boundaries, etc
    def draw(self):
        print('\n\nDrawing image...')

        self.dot_count = 0

        self.calculate_params()
        draw = ImageDraw.Draw(self.out_image)

        image_scaled = self.src_image.copy()
        image_scaled.thumbnail((self.dots_wide, self.dots_tall), Image.ANTIALIAS)
        # image_scaled.thumbnail((self.dots_wide, self.dots_tall), Image.NEAREST)
        # image_scaled.thumbnail((self.dots_wide, self.dots_tall), Image.BILINEAR)
        # image_scaled.thumbnail((self.dots_wide, self.dots_tall), Image.BICUBIC)

        for j in range(self.dots_tall):
            # Draw horizontal grid lines
            if self.flag_draw_grid:
                draw.line((self.border_x * self.pixels_per_inch, (self.border_y + self.max_hole_size/2.0 + j * self.grid_spacing) * self.pixels_per_inch, self.out_image.size[0] - self.border_x * self.pixels_per_inch, (self.border_y + self.max_hole_size/2.0 + j * self.grid_spacing) * self.pixels_per_inch), fill=self.grid_color)

            for i in range(self.dots_wide):
                # Get alpha val
                # pixelVal = image_scaled.getpixel((i,j))[3]
                # Get RGB intensity
                pixelVal = image_scaled.getpixel((i,j))
                if self.flag_invert_colors:
                    pixelVal = 256 - int( (pixelVal[0] + pixelVal[1] + pixelVal[2]) / 3 )
                else:
                    pixelVal = int( (pixelVal[0] + pixelVal[1] + pixelVal[2]) / 3 )
                # Calculate nearest drill size
                currentDotSize = self.find_nearest_drill_size(pixelVal)
                # print('PixelValue: ' + str(pixelVal) + '   currentDotSize: ' + str(currentDotSize))

                # Draw vertical grid lines
                if (j == 0) & self.flag_draw_grid:
                    draw.line(( (self.border_x + self.max_hole_size/2.0 + i * self.grid_spacing) * self.pixels_per_inch, self.border_y * self.pixels_per_inch, (self.border_x + self.max_hole_size/2.0 + i * self.grid_spacing) * self.pixels_per_inch, self.out_image.size[1] - self.border_y * self.pixels_per_inch), fill=self.grid_color)

                if currentDotSize == 0:
                    continue

                # Draw drill hole
                hole = DrillHole(
                    self.out_image,
                    self.border_x + self.max_hole_size/2.0 + i * self.grid_spacing,
                    self.border_y + self.max_hole_size/2.0 + j * self.grid_spacing,
                    currentDotSize,
                    self.pixels_per_inch,
                    self.max_hole_size,
                    self.font_size,
                    self.font_color,
                    self.flag_draw_ranges,
                    self.flag_draw_sizes
                )
                hole.draw()
                # print('Drawing hole at (' + str(hole.x / pixels_per_inch) + ',' + str(hole.y / pixels_per_inch) + ') with size ' + str(hole.size / pixels_per_inch))
                del hole

                self.dot_count += 1

        # Draw inset border
        # draw.rectangle(( self.border_x * self.pixels_per_inch, self.border_y * self.pixels_per_inch, self.out_x - self.border_x * self.pixels_per_inch, self.out_y - self.border_y * self.pixels_per_inch),outline=self.inset_border_color)

        self.printInfo(draw)

        del draw
    # --- function end ---

    # Reloads image calls init again
    def reload_image(self):
        self.calculate_params()
        self.draw()
    # --- function end ---

    # Reloads image calls init again
    def load_new_image(self, newImage):
        self.input_image         = newImage
        self.calculate_params()
        self.draw()
    # --- function end ---

    # Sets new dot width for image
    # def set_new_dotWidth(self, dots_wide):
        # self.dots_wide   = dots_wide
        # self.calculate_params()
        # self.draw()

    # Prints dottizing info to console
    def printInfo(self, draw):

        tempfont = ImageFont.truetype("RobotoMono-Regular.ttf", self.font_size*2)
        # tempfont = ImageFont.truetype("cour.ttf", self.font_size*2)
        tempVertSpace = self.font_size*2
        
        out_text = 'Dimensions:  ' + str(self.dots_wide*self.max_hole_size + (self.dots_wide-1)*self.dist_between_holes + 2*self.border_x) + '"x' + str(self.dots_tall*self.max_hole_size + (self.dots_tall-1)*self.dist_between_holes + 2*self.border_y) + '"    (' + str(self.dots_wide) + ' dots x ' + str(self.dots_tall) + ' dots)'
        draw.text((0, 0*tempVertSpace), out_text, fill=self.font_color, font=tempfont)
        
        out_text = 'Grid Spacing:  ' + str(self.grid_spacing) + ' in    (max hole size:  ' + str(self.max_hole_size) + ' in, spacing size:  ' + str(self.dist_between_holes) + ' in)'
        draw.text((0, 1*tempVertSpace), out_text, fill=self.font_color, font=tempfont)
        
        #Print available drill sizes
        out_text = 'Using the following drill sizes:'
        draw.text((0, 2*tempVertSpace), out_text, fill=self.font_color, font=tempfont)
        
        j = 3
        for i in self.drill_sizes:
            # print('    ' + str(Fraction(str(i[0]))) + '"')
            out_text = '    ' + str(Fraction(str(i[0]))) + '"     (' + str(i[1]) + ' scaled)'
            draw.text((0, j*tempVertSpace), out_text, fill=self.font_color, font=tempfont)
            j += 1
        
    # --- function end ---
# --------------------------- class end ---------------------------












