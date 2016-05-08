# This file contains globals used across the dottizer program

# ==============================================================================
# User Specified Params
# ==============================================================================

# drill_sizes = []             # Sets available drill bits when creating images
drill_sizes = [
0.0,
1.0/8.0,
9.0/64.0,
5.0/32.0,
3.0/16.0,
1.0/4.0,
5.0/16.0,
3.0/8.0,
1.0/2.0,
5.0/8.0,
3.0/4.0,
7.0/8.0,
1.0
]

# Function for generating drill_sizes global var
def generate_global_drill_sizes():
    print('called generate_global_drill_sizes()')

    global drill_sizes
    drill_sizes = []
    for size in optional_drill_sizes:
        if size[1]:
            drill_sizes.append(size[0])

    print(drill_sizes)

    # drill_sizes = np.asarray(temp_drill_sizes)

optional_drill_sizes = [
[0.0, True],
[1.0/8.0, True],
[9.0/64.0, True],
[5.0/32.0, True],
[3.0/16.0, True],
[1.0/4.0, True],
[5.0/16.0, True],
[3.0/8.0, True],
[1.0/2.0, True],    # Largest regular drill bit
[5.0/8.0, False],
[3.0/4.0, False],
[7.0/8.0, False],
[1.0, False]
]

generate_global_drill_sizes()



dist_between_holes = 0.4      # Sets the distance between holes (edge to edge in inches)
border_x = 2.0               # Sets the border width (in inches)
border_y = 2.0               # Sets the border height (in inches)
input_image = "input.png"    # Input image for dottizing
dots_wide = 50               # How many drill holes wide the image should be (dotsTall will be calculated from this)

pixels_per_inch = 40          # Sets scaling of rendered image(s)

pixels_per_inch_render = 80

# ==============================================================================
# Other Params (not exposed to user yet)
# ==============================================================================

font_size = 12               # Size of global font

# Image colors
font_color = (255, 255, 255, 255)        # Color of global font
grid_color = (128, 128, 128, 128)        # Color of background dot grid
inset_border_color = (0, 0, 255, 255)     # Color of edge border line

# Params for making series of images
# series_base_width = dotsWide  # dotWidth for initial image
# series_increment = 10        # How many dot increments to make images for


# ==============================================================================
# Internal Dottizer Stuff
# ==============================================================================

# workDir = 'dottizerFiles/'      # Directory for temporary dottizer files
out_dir = 'out/'                 # Directory for output images

# Size of source image view
src_view_x = 300
src_view_y = 225

# Size of output image view
out_view_x = 1200/2
out_view_y = 900/2
# out_view_x = 1200
# out_view_y = 900


