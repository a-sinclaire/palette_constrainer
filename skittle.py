import cv2
import numpy as np
import math

DISPLAY = False
# purple, magenta, blue, green, yellow, red, white
# skittles = ["#5d2b7d", "#a72d89", "#1474bb", "#8fc33e", "#feee22", "#e41e26", "#ffffff"]  # logo col, not real col

# green, red, orange, yellow, purple, white
skittles = ["#378e30", "#912439", "#dc5343", "#c5ba5e", "#1d1b20", "#ffffff"]
counts = [1700, 1800, 2100, 2100, 2200, 99999999]  # 100 bags


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
# the value is a weight. how close it is to that particular color
def closest_color(hsv_palette, pixel, Hue_Weight, Sat_Weight, Val_Weight):
    pix_hsv = rgb_to_hsv(pixel)  # pixel in hsv
    palette_close_arr = []
    for p in hsv_palette:
        palette_close_arr.append(
            (abs(angle_difference(pix_hsv[0], p[0])) * Hue_Weight) + (abs(pix_hsv[1] - p[1]) * Sat_Weight) + (
                        abs(pix_hsv[2] - p[2]) * Val_Weight))
    # lowest = 999
    # id = 0
    # for v in range(len(palette_close_arr)):
    #     if palette_close_arr[v] < lowest:
    #         lowest = palette_close_arr[v]
    #         id = v
    # return hsv_palette[id]
    return np.array(palette_close_arr)


def lowest_index(arr):
    lowest = 999999
    index = 0
    for i in range(len(arr)):
        if arr[i] < lowest:
            lowest = arr[i]
            index = i
    return index


def fill_in_colors(col_array, image, unlimited):
    new_col_arr = [[], [], [], [], [], []]
    for i in range(len(col_array)):
        for j in range(len(col_array[i])):
            x, y = col_array[i][j][0], col_array[i][j][1]
            if counts[i] <= 0:
                image[x, y] = [255, 255, 255]
                col_array[i][j][2][i] = 99999
                col_ind = lowest_index(col_array[i][j][2])
                new_col_arr[col_ind].append(col_array[i][j])
                continue
            if not unlimited:
                counts[i] -= 1
            rgb = hex_to_rgb(skittles[i])
            bgr = [rgb[2], rgb[1], rgb[0]]
            image[x, y] = bgr
    return new_col_arr


def run(image, palette, Hue_Weight=1, Sat_Weight=1, Val_Weight=10, unlimited=False):
    # PREP
    # convert palette to HSV
    hsv_palette = []
    for p in palette:
        hsv_palette.append(rgb_to_hsv(hex_to_rgb(p)))
    if DISPLAY:
        print("HSV")
        print(hsv_palette)
        print()

    # GO
    # show before img
    cv2.imshow("before", image)
    cv2.waitKey(1)

    rows, cols, colors = image.shape
    col_array = [[], [], [], [], [], []]

    for i in range(rows):
        for j in range(cols):
            pixel = [image[i, j, 2], image[i, j, 1], image[i, j, 0]]
            hsv_arr = closest_color(hsv_palette, pixel, Hue_Weight, Sat_Weight, Val_Weight)
            col_ind = lowest_index(hsv_arr)
            col_array[col_ind].append([i, j, hsv_arr])

            # rgb = hsv_to_rgb(hsv)
            # bgr = [rgb[2], rgb[1], rgb[0]]
            # image[i, j] = bgr
        if i % (rows / 8) == 0:
            print("{x:8.4} %".format(x=100 * ((i * rows) + j) / (rows * cols)))

    # green, red, orange, yellow, purple, white
    # print(col_array[0][0])
    col_array = fill_in_colors(col_array, image, unlimited)
    col_array = fill_in_colors(col_array, image, unlimited)
    col_array = fill_in_colors(col_array, image, unlimited)
    col_array = fill_in_colors(col_array, image, unlimited)
    col_array = fill_in_colors(col_array, image, unlimited)


    print(counts)

    print("-- Completed --")
    cv2.imshow("after", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image = cv2.imread("../Lenna128.png")
image = cv2.imread("../rainbow128.jpg")
#image = cv2.imread("../the_drill.png")

H = 2
S = 1
V = 3

run(image, skittles, Hue_Weight=H, Sat_Weight=S, Val_Weight=V, unlimited=True)
