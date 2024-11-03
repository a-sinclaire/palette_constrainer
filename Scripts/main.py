import cv2
from skittle4 import skittlefy
from renderskittle import renderSkittles

def main():
    # the path of the image to convert (try to pick something small, like 128x128 or less, larger will take time)
    img = "../Examples/Lenna128_2.png"
    # green, red, orange, yellow, purple, white (skittle colors - last element is always the "bg" color)
    skittle_palette = ["#378e30", "#912439", "#dc5343", "#c5ba5e", "#1d1b20", "#ffffff"]
    # counts of each color in array above. - last element value doesn't matter
    skittle_counts = [17, 18, 21, 21, 22, 999]
    # how we weight the hue, saturation, and value when comparing img col to palette col
    # the higher it's weighted the more important it is to preserve
    H = 1
    S = 1
    V = 3
    # this loop just increases the number of each skittle for testing purposes
    # in a real implementation your counts array should have the real num of skittles available to begin with
    n_bags = 65
    for q in range(len(skittle_counts)):
        skittle_counts[q] *= n_bags

    # this is the line the actually skittlefies your img.
    # it has an option to make the counts unlimited (will allow you to see what skittlefy would do in the ideal situation)
    # it has an option to use_all. this will ensure it uses every single skittle you give it
    #   (provided the number of skittles is smaller than the canvas size)
    # it also ha a priority option with three choices: none, random, and confidence.
    # none assigns skittles in pixel order, random in random order, confidence assigns the most confident skittles first
    out_img, out_arr, out_count = skittlefy(img, skittle_palette, skittle_counts, hue_weight=H, sat_weight=S, val_weight=V, unlimited=False, use_all=True, priority='confidence')
    # it returns three values: out_img, out_arr, and out_count
    # out_img is a cv2 img with the skittle colors in it
    # out_arr is a 2d array where each element has an int value corresponding to the color that pixel has been assigned
    #     the value is the index of the color in the skittle_palette you provided
    # out_count is the same skittle_count you passed in, but with new values representing how many skittles are remaining
    #     if you have use_all=True, they should all = 0

    # displaying some of this information:
    # prints skittle counts before and after
    print(skittle_counts)
    print(out_count)

    # Take the returned array and the palette to create an image where the pixels
    # represent a skittle and draw a circle instead of the pixel. Each circle
    # will be colored using the palette.
    circDiam = 4
    rimage = cv2.imread(img)
    rows, cols, colors = rimage.shape
    renderSkittles(circDiam, cols, rows, out_arr, skittle_palette)

    # displays before and after images
    img = cv2.imread(img)
    cv2.imshow("before", img)
    cv2.waitKey(1)
    cv2.imshow("after", out_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__=='__main__':
    main()
