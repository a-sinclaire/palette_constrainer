import cv2
import numpy as np
import math


DISPLAY = False


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv //3))


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
        hue = ((g-b)/delta)
    elif cmax == g:
        hue = ((b-r)/delta)+2
    else:
        hue = ((r-g)/delta)+4
    if cmax == 0:
        sat = 0
    else:
        sat = (delta/cmax)*100.0
    val = cmax*100.0
    hue *= 60
    return [hue, sat, val]


def hsv_to_rgb(value):
    h, s, v = value
    s /= 100.0
    v /= 100.0
    c = v*s
    x = c*(1-abs(((h/60.0) % 2)-1))
    m = v-c
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
    return [(temp[0]+m)*255.0, (temp[1]+m)*255.0, (temp[2]+m)*255.0]


def average_rgb(val1, val2):
    return [(val1[0]+val2[0])/2, (val1[1]+val2[1])/2, (val1[2]+val2[2])/2]


def angle_difference(ang1, ang2):
    diff = ((ang2 - ang1 + 180) % 360) - 180
    return diff + 360 if (diff < -180) else diff


def closest_color(hsv_palette, rgb, x, y, dither, dither_palette, dither_parents, Hue_Weight, Sat_Weight, Val_Weight):
    pix_hsv = rgb_to_hsv(rgb)
    palette_close_arr = []
    for p in hsv_palette:
        palette_close_arr.append((abs(angle_difference(pix_hsv[0], p[0]))*Hue_Weight) + (abs(pix_hsv[1]-p[1])*Sat_Weight) + (abs(pix_hsv[2]-p[2])*Val_Weight))
    lowest = 999
    id = 0
    for v in range(len(palette_close_arr)):
        if palette_close_arr[v] < lowest:
            lowest = palette_close_arr[v]
            id = v
    use_dither = False
    if dither:
        dither_close_arr = []
        for p in dither_palette:
            dither_close_arr.append((abs(angle_difference(pix_hsv[0], p[0]))*Hue_Weight) + (abs(pix_hsv[1]-p[1])*Sat_Weight) + (abs(pix_hsv[2]-p[2])*Val_Weight))
        for v in range(len(dither_close_arr)):
            if dither_close_arr[v] < lowest:
                use_dither = True
                lowest = dither_close_arr[v]
                id = v
        if use_dither:
            if x % 2 == y % 2:
                return dither_parents[id][0]
            return dither_parents[id][1]
    return hsv_palette[id]


def run(image, palette, dither=False, Hue_Weight=1, Sat_Weight=1, Val_Weight=10):
    ### PREP ###
    # convert palette to HSV
    hsv_palette = []
    for p in palette:
        hsv_palette.append(rgb_to_hsv(hex_to_rgb(p)))
    if DISPLAY:
        print("HSV")
        print(hsv_palette)
        print()
    dither_palette = []
    dither_parents = []
    if dither:
        for p in palette:
            for q in palette:
                dither_parents.append([rgb_to_hsv(hex_to_rgb(p)), rgb_to_hsv(hex_to_rgb(q))])
                dither_palette.append(rgb_to_hsv(average_rgb(hex_to_rgb(p), hex_to_rgb(q))))
        # removes vals from base palette (leave just the in_betweens)
        dither_palette = [x for x in dither_palette if x not in hsv_palette]
        # removes duplicates
        dither_palette = [i for n, i in enumerate(dither_palette) if i not in dither_palette[:n]]

        # remove duplicates
        res = []
        for i in dither_parents:
            if i[0] != i[1]:
                res.append(i)
        dither_parents = res
        # check for swaps
        # if swap exists remove the swap
        for p in dither_parents:
            if [p[1], p[0]] in dither_parents:
                dither_parents.remove([p[1], p[0]])
        # remove vals that computer to vals from base palette
        for p in dither_parents:
            if average_rgb(hsv_to_rgb(p[0]), hsv_to_rgb(p[1])) in hsv_palette:
                dither_parents.remove(p)
        if DISPLAY:
            print("DITHER PALETTE")
            print(dither_palette)
            print()
            print("DITHER PARENTS")
            print(dither_parents)

    ### GO ###
    cv2.imshow("before", image)
    cv2.waitKey(1)
    rows, cols, colors = image.shape
    for i in range(rows):
        for j in range(cols):
            hsv = closest_color(hsv_palette, [image[i, j, 2], image[i, j, 1], image[i, j, 0]], i, j, dither, dither_palette, dither_parents, Hue_Weight, Sat_Weight, Val_Weight)
            rgb = hsv_to_rgb(hsv)
            bgr = [rgb[2], rgb[1], rgb[0]]
            image[i, j] = bgr
        if i % (rows/8) == 0:
            print("{x:8.4} %".format(x=100*((i*rows)+j)/(rows*cols)))
    print("-- Completed --")
    cv2.imshow("after", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# palette = ["#000000", "#FFFFFF"]  # b&w
# palette = ["#000000", "#C0C0C0", "#FFFFFF"]
# palette = ["#EEEEEE", "#CCCCCC", "#999999", "#666666", "#333333", "#000000"]  # grayscale
# palette = ["#870000", "#ffffff", "#494237", "#d2b869"]  # reine blanche
palette = ["#073a60", "#1d848e", "#07d8c9", "#eeecbc", "#98a19c"]  # teacup teal
skittles = ["#5d2b7d", "#a72d89", "#1474bb", "#8fc33e", "#feee22", "#e41e26", "#ffffff"]
skittles = ["#378e30", "#912439", "#dc5343", "#c5ba5e", "#1d1b20", "#ffffff"]
# palette = ["#1F1833", "#2B2E42", "#414859", "#68717A", "#90A1A8", "#B6CBCF", "#FFFFFF", "#FCBF8A", "#B58057", "#8A503E",
#            "#5C3A41", "#C93038", "#DE6A38", "#FFAD3B", "#FFE596", "#FCF960", "#B4D645", "#51C43F", "#309C63", "#236D7A",
#            "#264F6E", "#233663", "#417291", "#4C93AD", "#63C2C9", "#94D2D4", "#B8FDFF", "#3C2940", "#46275C", "#826481",
#            "#F7A48B", "#C27182", "#852D66"]
# image = cv2.imread("../QCaSg.png")
# image = cv2.imread("../palette_test.png")
# image = cv2.imread("../brown.png")
# image = cv2.imread("../lion.png")
# image = cv2.imread("../the_drill.png")
# image = cv2.imread("../Lenna_(test_image).png")
image = cv2.imread("../Lenna128.png")
H = 2
S = 1
V = 1

run(image, skittles, dither=False, Hue_Weight=H, Sat_Weight=S, Val_Weight=V)
