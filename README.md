# palette_constrainer
takes an input image and constrains it to a given palette of colors

# dither.py
takes an image and constrains it to a given palette
can enable dither option which will use dithering to achieve more "colors"
this program is garbage. super slow, and not that great.

modify they values H, S, and V at the bottom to weight hue, sat, and val differently for when the program is trying to determine how similar two colors are.
also at the bottom is where the palette is defined and the image you're operating on is defined.
nothings passed in from the cmd line b/c i cant be bothered. just edit the file.

# skittle2.py
like dither.py but the palette is defined at the top of the file.
additionally there is a var called counts that determines how many of each color you have.
takes an image, and given some number of each color, recolors the image.

imagine you wanted to convert an img into skittles. just input the num of skittles you have, and make sure you img is at the resolution so 1px=1skittle.
img is defined at bottom of file with HSV weights.

there is an option to make the num of skittles unlimited (useful to help you determine the weights you want for an image).
and an option to go in random order, so each pixel gets a more fair chance of getting its desired color.
