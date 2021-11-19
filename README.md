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

# example
with ~100 bags of skittles (not random order) on 128x128 canvas

![Alt text](Examples/1.jpg?raw=true "Title")

<br />
<br />

with ~100 bags of skittles (random order) on 128x128 canvas

![Alt text](Examples/2.jpg?raw=true "Title")

# skittle3.py
this is skittle2.py BUT it MUST use all the skittles it is given. (skittle2.py could "throw out" unneeded skittles)
it now also fills in not based on a random order, but rather based on the order where what pixels think they are most confident in their color.
you can see now that it MUST use all of them, it can have some quite ugly results. and now the number of bags of skittles we use is penalized for being too high.
if you will allow skittles to be "thrown out" i think skittle2.py will give nicer results

with ~65 bags of skittles on 128x128 canvas

![Alt text](Examples/3.jpg?raw=true "Title")

<br />
<br />

with ~100 bags of skittles on 128x128 canvas

![Alt text](Examples/4.jpg?raw=true "Title")

<br />
<br />

with ~50 bags of skittles on 128x128 canvas

![Alt text](Examples/5.jpg?raw=true "Title")

