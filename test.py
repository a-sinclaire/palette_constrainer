import copy

from blend_modes import multiply
import cv2
import numpy as np
from PIL import Image, ImageOps

from color_conversion import hex_to_rgb
from skittlize import skittlize

colors = ["#e64808", "#f1be02", "#048207", "#441349", "#c0043f", "#ffffff"]


def get_skittle_images(palette):
    img = cv2.imread('blank_skittle.png', -1)
    img = cv2.resize(img, (50, 50))

    bg = np.zeros(img.shape, np.uint8)
    r, g, b = hex_to_rgb(palette[-1])
    bg[:] = (b, g, r, 255)

    results = []
    for c in palette[:-1]:
        r, g, b = hex_to_rgb(c)
        img2 = np.zeros(img.shape, np.uint8)
        img2[:] = (b, g, r, 255)
        img = img.astype(np.float32)
        img2 = img2.astype(np.float32)

        # multiply blank skittle with its color
        result = multiply(img2, img, 1.0).astype(np.uint8)

        # mask out the skittle
        _, mask = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
        mask = cv2.cvtColor(mask, cv2.COLOR_RGB2RGBA).astype(np.uint8)
        result = cv2.bitwise_and(result, mask)

        # past skittle onto background
        bg1 = Image.fromarray(bg.astype(np.uint8))
        s = Image.fromarray(result.astype(np.uint8))
        bg1.paste(s, (0, 0), Image.fromarray(mask))
        result = np.array(copy.deepcopy(bg1))

        text = str(np.random.choice(['s', 'm', ''], 1, p=[0.8, 0.19, 0.01])[0])
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255)
        thickness = 1
        textsize = cv2.getTextSize(text, font, font_scale, thickness)[0]
        position = ((result.shape[1] - textsize[0]) // 2, (result.shape[0] + textsize[1]) // 2)
        cv2.putText(result, text, position, font, font_scale, color, thickness)
        results.append(result)
    results.append(bg)
    return results


def main():
    skittles = get_skittle_images(colors)
    skittle_w = skittles[0].shape[0]
    skittle_h = skittles[0].shape[1]
    # for idx, img in enumerate(skittles):
    #     cv2.imshow(str(idx), img)
    #     cv2.waitKey(0)
    # cv2.destroyAllWindows()

    out_img, out_arr, out_count = skittlize('Examples/meeley3_128.jpg', colors, [17, 18, 21, 21, 22, 999], 1, 1, 3, True, False, 'confidence')
    result = np.zeros((out_img.shape[0] * skittle_w, out_img.shape[1] * skittle_h, 4), np.uint8)
    print(out_img.shape)
    print(skittles[0].shape)
    print(result.shape)
    # cv2.imshow('t', skittles[0])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # result[100:100+skittle_h, 100:100+skittle_w] = skittles[0]
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    result = Image.fromarray(result)
    result = ImageOps.exif_transpose(result)
    # result.paste(Image.fromarray(skittles[0]), (50, 50))
    s = cv2.cvtColor(skittles[0], cv2.COLOR_BGR2RGB)
    s = Image.fromarray(s)
    s = ImageOps.exif_transpose(s)
    s.show()
    for idx, pi in enumerate(out_arr):
        for jdx, col_idx in enumerate(pi):
            skit = Image.fromarray(skittles[col_idx])
            # result[idx*skittle_w:idx*skittle_w+skittle_w, jdx*skittle_h:jdx*skittle_h+skittle_h] = copy.deepcopy(skit)
            result.paste(skit, (jdx*skittle_w, idx*skittle_h))
    result = np.array(result)
    cv2.imwrite('test.png', result)


if __name__=='__main__':
    main()
