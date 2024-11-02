#
# skittle4.py
#
# Description:
#       Can take an image, a palette of colors, a count of how many of each color exists and
#       generate an output image using only those available colors and their counts
#
# Author: Amelia Sinclaire
#
# History:
#   19Nov2021   Amelia Sinclaire Created file from skittle3.py
#                                Removed elements that made it a script
#                                Added more accessible options for skittlefication
#                                Comment and Clean
#
# Example of how to use:
#
# # the path of the image to convert (try to pick something small, like 128x128 or less, larger will take time)
# img = "../Lenna128_2.png"
# # green, red, orange, yellow, purple, white (skittle colors - last element is always the "bg" color)
# skittle_palette = ["#378e30", "#912439", "#dc5343", "#c5ba5e", "#1d1b20", "#ffffff"]
# # counts of each color in array above. - last element value doesn't matter
# skittle_counts = [17, 18, 21, 21, 22, 999]
# # how we weight the hue, saturation, and value when comparing img col to palette col
# # the higher it's weighted the more important it is to preserve
# H = 1
# S = 1
# V = 3
# # this loop just increases the number of each skittle for testing purposes
# # in a real implementation your counts array should have the real num of skittles available to begin with
# n_bags = 65
# for q in range(len(skittle_counts)):
#     skittle_counts[q] *= n_bags
#
# # this is the line the actually skittlefies your img.
# # it has an option to make the counts unlimited which will allow you to see what skittlefy would do in the ideal situation
# # it has an option to use_all. this will ensure it uses every single skittle you give it provided the number of skittles is smaller than the canvas size
# # it also ha a priority option with three choices: none, random, and confidence.
# # none assigns skittles in pixel order, random in random order, confidence assigns the most confident skittles first
# out_img, out_arr, out_count = skittlefy(img, skittle_palette, skittle_counts, Hue_Weight=H, Sat_Weight=S, Val_Weight=V, unlimited=False, use_all=True, priority='confidence')
#
# # it returns three values: out_img, out_arr, and out_count
# # out_img is a cv2 img with the skittle colors in it
# # out_arr is a 2d array where each element has an int value corresponding to the color that pixel has been assigned by skittlefy
# #     the int is the index of that color in the skittle_palette you provided
# # out_count is the same skittle_count you passed in, but now with new values representing how many skittles are remaining after the operation
# #     if you have use_all=True, they should all = 0
#
# # displaying some of this information:
# # prints skittle counts before and after
# print(skittle_counts)
# print(out_count)
#
# # displays before and after images
# img = cv2.imread(img)
# cv2.imshow("before", img)
# cv2.waitKey(1)
# cv2.imshow("after", out_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
import random
import cv2
from color_conversion import hex_to_rgb, hsv_to_rgb, rgb_to_hsv


def angle_difference(ang1, ang2):
    # returns diff of two angles (shortest dist)
    diff = ((ang2 - ang1 + 180) % 360) - 180
    return diff + 360 if (diff < -180) else diff


def closest_color(hsv_palette, pixel_rgb, Hue_Weight, Sat_Weight, Val_Weight):
    """
    Compares a pixel's color to all the colors in the given palette
    Generates an array corresponding to how far from a color the pixel is for each col in the palette

    :param hsv_palette: the palette array of hsv values [[h1, s1, v1], [h2, s2, v2], ...]
    :param pixel_rgb: the rgb of the pixel you are comparing against [r, g, b]
    :param Hue_Weight: how important is preserving the hue? (hint: negative values work as a deterrent)
    :param Sat_Weight: how important is preserving the sat? (this is typically the least important weight)
    :param Val_Weight: how important is preserving the val? (this is typically the most important weight)
    :return: array of len len(hsv_palette). each element corresponds to the distance to that palette color
             index 0 in this array shows how far the given pixel is from the color at index 0 in hsv_palette array...
             a value of 0 would indicate a perfect match
    """
    pix_hsv = rgb_to_hsv(pixel_rgb)  # pixel in hsv
    palette_close_arr = []
    for p in hsv_palette:
        palette_close_arr.append(
            (abs(angle_difference(pix_hsv[0], p[0])) * Hue_Weight) + (abs(pix_hsv[1] - p[1]) * Sat_Weight) + (
                    abs(pix_hsv[2] - p[2]) * Val_Weight))
    return palette_close_arr


def lowest_index(arr):
    # returns index value of lowest value in given array
    lowest = arr[0]
    index = 0
    for i in range(len(arr)):
        if arr[i] < lowest:
            lowest = arr[i]
            index = i
    return index


def lowest_value(arr):
    # returns lowest value in given array
    lowest = arr[0]
    for i in range(len(arr)):
        if arr[i] < lowest:
            lowest = arr[i]
    return lowest


def skittlefy(image_path, palette, palette_count, Hue_Weight=1, Sat_Weight=1, Val_Weight=3, unlimited=False,
              use_all=False, priority='none'):
    """
    Takes an input image and "skittlefies" it.

    :param image_path: path to img to skittlefy
    :param palette: array of hex strings (available skittle colors) -- last is bg color of your canvas
    :param palette_count: count of how many of each color skittle you have. (count for last index doesnt matter)
    :param Hue_Weight: how important is preserving the hue? (hint: negative values work as a deterrent)
    :param Sat_Weight: how important is preserving the sat? (this is typically the least important weight)
    :param Val_Weight: how important is preserving the val? (this is typically the most important weight)
    :param unlimited: if true, it doesnt subtract from the count of skittles
                      (allows you to see what skittlefy would do in the ideal situation)
    :param use_all: if true, it will use every single skittle provided to it, assuming the num of skittles < canvas size
    :param priority: none, random, or confidence.
                     priority none: assigns skittles in order of the pixels
                     priority random: assigns skittles in random order
                     priority confidence: assigns the most confident skittles first
    :return: skittlefied_img, skittlefied_array, remaining_count
             skittlefied_img: cv2 img where the colors are replaced with the palette colors
             skittlefied_array: 2d array filled with the skittle colors represented by the index from palette
             remaining_count: how many of each color are remaining after skittlefying (relevant if use_all=False)
    """
    image = cv2.imread(image_path)
    rows, cols, colors = image.shape
    if image is None:
        raise ValueError("Failed to load specified image.")

    if len(palette) is not len(palette_count):
        raise ValueError("Expected palette and palette_count to be of equal size.")

    priority_types = ['none', 'random', 'confidence']
    if priority not in priority_types:
        raise ValueError("Invalid priority type. Expected one of: %s" % priority_types)

    # SETTING THE NUMBER OF "BG color" SKITTLES TO EXACTLY (last index)
    # THE NUMBER OF EMPTY SPACES WE HAVE
    if use_all is True:
        total_skittles = 0
        for k in range(len(palette_count)):
            total_skittles += palette_count[k]
        palette_count[-1] = (rows * cols) - (total_skittles - palette_count[-1])
    else:
        palette_count[-1] = rows * cols

    # convert palette to HSV (palette contains hex equivalent of skittles colors) (but any colors could be used)
    hsv_palette = []
    for p in palette:
        hsv_palette.append(rgb_to_hsv(hex_to_rgb(p)))

    # prepare an array of same size as image to hold color closeness info
    img_data = [[None for y in range(cols)] for x in range(rows)]

    # iterate through the image
    for i in range(rows):
        for j in range(cols):
            pixel_rgb = [image[i, j, 2], image[i, j, 1], image[i, j, 0]]  # current pixles rgb val
            # closest_color returns an array that shows how close this pixel is to each color in the palette
            # ex. [0, 200, 500, 120, 950, 300]
            # where 0 is the closest because there is 0 difference between the colors
            hsv_arr = closest_color(hsv_palette, pixel_rgb, Hue_Weight, Sat_Weight, Val_Weight)
            # we store this info in the img_data arr at the same location as the pixel
            img_data[i][j] = hsv_arr

    # setting the order we will loop through the array to assign colors
    pix_index = list(range(rows * cols))
    if priority == priority_types[2]:
        # instead of random we want it to be in order of pixels that are closet to values
        # sort this list based on lowest_value(img_data[i][j])
        expanded_img_data = [[None] for y in range(rows * cols)]
        for i in range(len(expanded_img_data)):
            expanded_img_data[i] = img_data[int(i / cols)][i % cols]
        sort_control = [[None] for y in range(rows * cols)]
        for i in range(len(sort_control)):
            sort_control[i] = lowest_value(expanded_img_data[i])

        # control the order in which we assign skittles based on how close they are to their preferred color
        pix_index = [x for _, x in sorted(zip(sort_control, pix_index))]
    elif priority == priority_types[1]:
        random.shuffle(pix_index)

    out_array = [[None for y in range(cols)] for x in range(rows)]
    # we now iterate through the image in order according to pix_index
    for i in range(rows * cols):
        y_in = pix_index[i] % cols
        x_in = int(pix_index[i] / cols)
        # keep track if we have colored this pixel yet
        colored = False
        while not colored:
            # find the closest color and get the index value of that element
            # (the index value corresponds to the same color in the palette)
            col_ind = lowest_index(img_data[x_in][y_in])
            # check if any colors are available
            col_available = False
            for k in range(len(palette_count)):
                if palette_count[k] > 0:
                    col_available = True
            # if no colors are available then color white
            if col_available is not True:
                image[x_in, y_in] = [255, 255, 255]
                break

            # if the count for that color is 0, we ran out of that color
            if palette_count[col_ind] <= 0:
                # we set this pixels closeness to that color really high so it wont choose this again, then repeat
                img_data[x_in][y_in][col_ind] = 99999
                continue
            # if not unlimited skittles then we decrement the count as we color this pixel
            if not unlimited:
                palette_count[col_ind] -= 1
            # assign the closest available color to this pixel before moving onto the next pixel
            rgb = hex_to_rgb(palette[col_ind])
            bgr = [rgb[2], rgb[1], rgb[0]]
            image[x_in, y_in] = bgr
            out_array[x_in][y_in] = col_ind
            colored = True

    palette_count[-1] = 0
    return image, out_array, palette_count
