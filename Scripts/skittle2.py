import cv2
import random

# purple, magenta, blue, green, yellow, red, white
# skittles = ["#5d2b7d", "#a72d89", "#1474bb", "#8fc33e", "#feee22", "#e41e26", "#ffffff"]  # logo col, not real col
# counts = [1700, 1800, 2100, 2100, 2200, 2000, 99999999]  # 100 bags

# green, red, orange, yellow, purple, white
skittles = ["#378e30", "#912439", "#dc5343", "#c5ba5e", "#1d1b20", "#ffffff"]
counts = [1700, 1800, 2100, 2100, 2200, 99999999]  # ~100 bags


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hsv(value):
    r, g, b = value
    r /= 255.0
    g /= 255.0
    b /= 255.0
    cmax = max(r, max(g, b))
    cmin = min(r, min(g, b))
    delta = cmax - cmin
    if delta == 0:
        hue = 0
    elif cmax == r:
        hue = ((g - b) / delta)
    elif cmax == g:
        hue = ((b - r) / delta) + 2
    else:
        hue = ((r - g) / delta) + 4
    if cmax == 0:
        sat = 0
    else:
        sat = (delta / cmax) * 100.0
    val = cmax * 100.0
    hue *= 60
    return [hue, sat, val]


def hsv_to_rgb(value):
    h, s, v = value
    s /= 100.0
    v /= 100.0
    c = v * s
    x = c * (1 - abs(((h / 60.0) % 2) - 1))
    m = v - c
    if 0 <= h < 60:
        temp = [c, x, 0]
    elif 60 <= h < 120:
        temp = [x, c, 0]
    elif 120 <= h < 180:
        temp = [0, c, x]
    elif 180 <= h < 240:
        temp = [0, x, c]
    elif 240 <= h < 300:
        temp = [x, 0, c]
    else:
        temp = [c, 0, x]
    return [(temp[0] + m) * 255.0, (temp[1] + m) * 255.0, (temp[2] + m) * 255.0]


def average_rgb(val1, val2):
    return [(val1[0] + val2[0]) / 2, (val1[1] + val2[1]) / 2, (val1[2] + val2[2]) / 2]


def angle_difference(ang1, ang2):
    diff = ((ang2 - ang1 + 180) % 360) - 180
    return diff + 360 if (diff < -180) else diff


# should return array where each element corresponds to the element from the palette
# the value is a weight. how far it is to that particular color
# ex. index 0 in the array this returns corresponds to index 0 of the palette
# the value at index 0 tells us how far from the color at index 0 in the palette it is
def closest_color(hsv_palette, pixel_rgb, Hue_Weight, Sat_Weight, Val_Weight):
    pix_hsv = rgb_to_hsv(pixel_rgb)  # pixel in hsv
    palette_close_arr = []
    for p in hsv_palette:
        palette_close_arr.append(
            (abs(angle_difference(pix_hsv[0], p[0])) * Hue_Weight) + (abs(pix_hsv[1] - p[1]) * Sat_Weight) + (
                        abs(pix_hsv[2] - p[2]) * Val_Weight))
    return palette_close_arr


# returns index value of lowest value in an array
def lowest_index(arr):
    lowest = 999999
    index = 0
    for i in range(len(arr)):
        if arr[i] < lowest:
            lowest = arr[i]
            index = i
    return index


def run(image, palette, Hue_Weight=1, Sat_Weight=1, Val_Weight=10, unlimited=False, random_order=True):
    # convert palette to HSV (palette contains hex equivalent of skittles colors) (but any colors could be used)
    hsv_palette = []
    for p in palette:
        hsv_palette.append(rgb_to_hsv(hex_to_rgb(p)))

    # show before img
    cv2.imshow("before", image)
    cv2.waitKey(1)

    # get size of image
    rows, cols, colors = image.shape
    # prepare an array of same size as image to hold color closeness info
    img_data = [[None for y in range(cols)] for x in range(rows)]

    # iterate through the image
    for i in range(rows):
        for j in range(cols):
            pixel_rgb = [image[i, j, 2], image[i, j, 1], image[i, j, 0]]    # current pixles rgb val
            # closest_color returns an array that shows how close this pixel is to each color in the palette
            # ex. [0, 200, 500, 120, 950, 300]
            # where 0 is the closest because there is 0 difference between the colors
            hsv_arr = closest_color(hsv_palette, pixel_rgb, Hue_Weight, Sat_Weight, Val_Weight)
            # we store this info in the img_data arr at the same location as the pixel
            img_data[i][j] = hsv_arr
        if i % (rows / 8) == 0:  # prints progress bar
            print("{x:8.4} %".format(x=100 * ((i * rows) + j) / (rows * cols)))

    # green, red, orange, yellow, purple, white

    # the order we will loop through the array to assign colors
    pix_index = list(range(rows*cols))
    if random_order:  # if random we shuffle
        random.shuffle(pix_index)

    # we now iterate through the image in order according to pix_index
    for i in range(rows*cols):
        y_in = pix_index[i] % cols
        x_in = int(pix_index[i] / cols)
        # keep track if we have colored this pixel yet
        colored = False
        while not colored:
            # find the closest color and get the index value of that element
            # (the index value corresponds to the same color in the palette)
            col_ind = lowest_index(img_data[x_in][y_in])
            # if the count for that color is 0, we ran out of that color
            if counts[col_ind] <= 0:
                # we set this pixels closeness to that color really high so it wont choose this again, then repeat
                img_data[x_in][y_in][col_ind] = 99999
                continue
            # if not unlimited skittles then we decrement the count as we color this pixel
            if not unlimited:
                counts[col_ind] -= 1
            # assign the closest available color to this pixel before moving onto the next pixel
            rgb = hex_to_rgb(skittles[col_ind])
            bgr = [rgb[2], rgb[1], rgb[0]]
            image[x_in, y_in] = bgr
            colored = True

    # prints out how many of each color remain
    print(counts)

    print("-- Completed --")
    # show after image
    cv2.imshow("after", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image = cv2.imread("../Lenna128.png")
image = cv2.imread("../Lenna128_2.png")
image = cv2.imread("../rainbow128.jpg")
# image = cv2.imread("../the_drill.png")
# image = cv2.imread("../brown.png")
image = cv2.imread("../me128.jpg")

# how we weight the hue, saturation, and value
H = 2
S = 1
V = 5

run(image, skittles, Hue_Weight=H, Sat_Weight=S, Val_Weight=V, unlimited=False, random_order=False)
