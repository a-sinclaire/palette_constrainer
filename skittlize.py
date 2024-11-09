# Amelia Sinclaire 2024

import random
from copy import deepcopy

import cv2
from numpy.typing import NDArray

from color_conversion import hex_to_rgb, hsv_to_rgb, rgb_to_hsv


def angle_difference(ang1: float, ang2: float) -> float:
    """:return: diff of two angles (shortest dist)"""
    diff = ((ang2 - ang1 + 180) % 360) - 180
    return diff + 360 if (diff < -180) else diff


def closest_color(hsv_palette: [[int]], pixel_rgb: [int],
                  hue_weight: int, sat_weight: int, val_weight: int) -> [[int]]:
    """
    Compares a pixel's color to all the colors in the given palette and
    generates an array corresponding to how far from a color the pixel is for
    each column in the palette.

    :param hsv_palette: array of hsv values [[h1, s1, v1], [h2, s2, v2], ...]
    :param pixel_rgb: [r, g, b]
    :param hue_weight: How important is preserving the hue?
                       (Hint: Negative values work as a deterrent.)
    :param sat_weight: How important is preserving the saturation?
                       (Hint: this is typically the least important weight.)
    :param val_weight: How important is preserving the value?
                       (Hint: This is typically the most important weight.)
    :return: Array of length len(hsv_palette). Each element corresponds to the
             distance to that palette color. Index 0 in this array shows how far
             the given pixel is from the color at index 0 in hsv_palette array.
             A value of 0 would indicate a perfect match.
    """
    # TODO: look into if the missing `angle_difference`s is a bug or a feature
    pix_hsv = rgb_to_hsv(pixel_rgb)  # pixel in hsv
    palette_close_arr = []
    for pal_col in hsv_palette:
        palette_close_arr.append(
            (abs(angle_difference(pix_hsv[0], pal_col[0])) * hue_weight) +
            (abs(pix_hsv[1] - pal_col[1]) * sat_weight) +
            (abs(pix_hsv[2] - pal_col[2]) * val_weight))
    return palette_close_arr


def lowest_index(arr: list[float]) -> int:
    """:return: Index of the lowest value in given array"""
    return arr.index(min(arr))


def lowest_value(arr: list[float]) -> float:
    """:return: Lowest value in given array"""
    return min(arr)


def skittlize(image_path: str, palette: list[str], palette_count: list[int],
              hue_weight: int = 1, sat_weight: int = 1, val_weight: int = 3,
              unlimited: bool = False, use_all: bool = False,
              priority: str = 'none'
              ) -> tuple[NDArray, list[list[int]], list[int]]:
    """
    Takes an input image and "skittlefies" it.

    :param image_path:
    :param palette: Array of skittle colors (as hex strings).
                    (Hint: Last is the background color of your canvas.)
    :param palette_count: How many of each color skittle you have.
                          (Count for last index doesn't matter.)
    :param hue_weight: How important is preserving the hue?
                       (Hint: Negative values work as a deterrent.)
    :param sat_weight: How important is preserving the saturation?
                       (Hint: This is typically the least important weight.)
    :param val_weight: How important is preserving the value?
                       (Hint: This is typically the most important weight.)
    :param unlimited: If `True`, it doesn't subtract from the count of skittles.
                      (Allows you to see what skittlefy would ideally do.)
    :param use_all: If `True`, it will use every single skittle provided to it,
                    assuming the number of skittles < canvas size.
    :param priority: none, random, or confidence
                     priority none: Assigns skittles in order of the pixels.
                     priority random: Assigns skittles in random order.
                     priority confidence: Assigns most confident skittles first.
    :return: skittlefied_img, skittlefied_array, remaining_count
             skittlefied_img: cv2 img where the colors are replaced with the
                              palette colors
             skittlefied_array: 2d array filled with the skittle colors
                                represented by the index from palette
             remaining_count: how many of each color are remaining after
                              skittlefying (relevant if use_all=False)
    """
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    rows, cols, colors = image.shape
    if image is None:
        raise ValueError("Failed to load specified image.")

    if len(palette) is not len(palette_count):
        raise ValueError("Expected palette and palette_count to be equal size.")

    priority_types = ['none', 'random', 'confidence']
    if priority not in priority_types:
        raise ValueError(f'Invalid priority type.'
                         f'Expected one of: {priority_types}')
    palette_count = deepcopy(palette_count)

    # SETTING THE NUMBER OF "BG color" SKITTLES TO EXACTLY (last index)
    # THE NUMBER OF EMPTY SPACES WE HAVE
    if use_all is True and unlimited is False:
        total_skittles = 0
        for k in range(len(palette_count)):
            total_skittles += palette_count[k]
        palette_count[-1] = (rows * cols) - (total_skittles - palette_count[-1])
    else:
        palette_count[-1] = rows * cols

    hsv_palette = []
    for p in palette:
        hsv_palette.append(rgb_to_hsv(hex_to_rgb(p)))

    # prepare an array of same size as image to hold color closeness info
    img_data = [[None for y in range(cols)] for x in range(rows)]

    # iterate through the image
    for i in range(rows):
        for j in range(cols):
            # current pixel's rgb val
            pixel_rgb = [image[i, j, 2], image[i, j, 1], image[i, j, 0]]
            # closest_color returns an array that shows how close this pixel is
            # to each color in the palette
            # ex. [0, 200, 500, 120, 950, 300]
            # 0 is the closest because there is 0 difference between the colors
            hsv_arr = closest_color(hsv_palette, pixel_rgb,
                                    hue_weight, sat_weight, val_weight)
            # store this info in the img_data arr at the location of the pixel
            img_data[i][j] = hsv_arr

    # setting the order we will loop through the array to assign colors
    pix_index = list(range(rows * cols))
    if priority == priority_types[2]:
        # instead of random we want it to be in order of most confident pixels
        # sort this list based on lowest_value(img_data[i][j])
        expanded_img_data = [[None] for y in range(rows * cols)]
        for i in range(len(expanded_img_data)):
            expanded_img_data[i] = img_data[int(i / cols)][i % cols]
        sort_control = [[None] for y in range(rows * cols)]
        for i in range(len(sort_control)):
            sort_control[i] = lowest_value(expanded_img_data[i])

        # control the order in which we assign skittles based on how close they
        # are to their preferred color
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
                image[x_in, y_in] = [255, 255, 255]  # TODO: should use bg color, not white
                break

            # if the count for that color is 0, we ran out of that color
            if palette_count[col_ind] <= 0:
                # we set this pixels closeness to that color really high so it
                # won't choose this again, then repeat
                img_data[x_in][y_in][col_ind] = 99999
                continue
            # if not unlimited skittles then we decrement the count as we color
            # this pixel
            if not unlimited:
                palette_count[col_ind] -= 1
            # assign the closest available color to this pixel before moving
            # onto the next pixel
            rgb = hex_to_rgb(palette[col_ind])
            bgr = [rgb[2], rgb[1], rgb[0]]
            image[x_in, y_in] = bgr
            out_array[x_in][y_in] = col_ind
            colored = True

    palette_count[-1] = 0  # TODO: what was my thinking here?
    return image, out_array, palette_count
