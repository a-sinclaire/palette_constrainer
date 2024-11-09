import argparse
import os.path

import cv2

# from renderskittle import renderSkittles
from skittlize import skittlize


def main(args):
    i = args.image_path
    p = args.palette
    c = args.counts
    h = args.hue_weight
    s = args.sat_weight
    v = args.val_weight
    u = args.unlimited
    a = args.use_all
    o = args.order
    out_img, out_arr, out_count = skittlize(i, p, c, h, s, v, u, a, o)

    # TODO: add render skittle back in?
    # Take the returned array and the palette to create an image where the pixels
    # represent a skittle and draw a circle instead of the pixel. Each circle
    # will be colored using the palette.
    # circDiam = 4
    # rimage = cv2.imread(img)
    # rows, cols, colors = rimage.shape
    # renderSkittles(circDiam, cols, rows, out_arr, skittle_palette)

    # displays before and after images
    img = cv2.imread(i)
    cv2.imshow("before", img)
    cv2.imshow("after", out_img)

    while cv2.getWindowProperty('before', cv2.WND_PROP_VISIBLE) >=1 and\
            cv2.getWindowProperty('after' , cv2.WND_PROP_VISIBLE) >=1:
        keyCode = cv2.waitKey(1)  # https://medium.com/@mh_yip/opencv-detect-whether-a-window-is-closed-or-close-by-press-x-button-ee51616f7088
        if (keyCode & 0xFF) == ord("q"):
            cv2.destroyAllWindows()
            break
    cv2.destroyAllWindows()


if __name__=='__main__':
    # TODO: change the default palette and counts to skittle versions?
    rainbow_palette = ['#ff595e', '#ff924c', '#ffca3a', '#c5ca30', '#8ac926',
                       '#52a675', '#1982c4', '#4267ac', '#6a4c93', '#ff0000',
                       '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff',
                       '#ffffff', '#000000']
    rainbow_counts = [500] * len(rainbow_palette)

    parser = argparse.ArgumentParser()
    parser.add_argument('image_path',
                        type=str,
                        help='<Requited> Path of image to be skittlized.')
    parser.add_argument('-p', '--palette',
                        nargs='+',
                        type=str,
                        default=rainbow_palette,
                        help='List of hex codes to use. The last color is the background color.')
    parser.add_argument('-c', '--counts',
                        nargs='+',
                        type=int,
                        default=rainbow_counts,
                        help='List of counts for each color. If left untouched it will default to 500 per color. The last color is the background color, as the count is infinite no matter what you put.')
    parser.add_argument('-x', '--hue_weight',
                        type=float,
                        default=1.0,
                        help='Hue weight. Used to preserve hue.')
    parser.add_argument('-s', '--sat_weight',
                        type=float,
                        default=1.0,
                        help='Saturation weight, Used to preserve saturation.')
    parser.add_argument('-v', '--val_weight',
                        type=float,
                        default=1.0,
                        help='Value weight. Used to preserve value.')
    parser.add_argument('-u', '--unlimited',
                        type=bool,
                        default=False,
                        help='If true the counts will be irrelevant. Will treat as though you have infinite of each')
    parser.add_argument('-a', '--use_all',
                        type=bool,
                        default=False,
                        help='If true the program will attempt to use every count of every color given.')
    parser.add_argument('-o', '--order',
                        type=str,
                        default='confidence',
                        help='Priority order to place the colors. [random, pixel, confidece]. Random places randomly. Pixel places in pixel order. Confidence places the most confident pixels first.')
    args = parser.parse_args()
    if not os.path.exists(args.image_path):
        raise ValueError(f'{args.image_path} does not exist.')
    if args.counts == rainbow_counts and args.palette != rainbow_palette:
        args.counts = [500] * len(args.palette)

    main(args)
