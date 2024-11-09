import cv2

from skittlize import skittlize


def main():
    example_img_path = 'meeley3_128.jpg'
    skittle_palette = ["#378e30", "#912439", "#dc5343", "#c5ba5e", "#1d1b20",
                       "#ffffff"]
    skittle_counts = [17, 18, 21, 21, 22, 999]
    n_bags = 65
    skittle_counts = [x * n_bags for x in skittle_counts]

    # UNLIMITED SKITTLES
    # example_img, unlimited
    example_img = cv2.imread(example_img_path)
    cv2.imwrite('example_img.jpg', example_img)
    unlimited, out_arr, out_count = skittlize(example_img_path, skittle_palette,
                                              skittle_counts, unlimited=True)
    cv2.imwrite('unlimited.jpg', unlimited)

    # USE ALL SKITTLES
    # pixel_order_all, random_order_all, confidence_order_all
    pixel_order_all, out_arr, out_count = skittlize(example_img_path, skittle_palette,
                                              skittle_counts, use_all=True,
                                              priority='none')
    cv2.imwrite('pixel_order_all.jpg', pixel_order_all)
    random_order_all, out_arr, out_count = skittlize(example_img_path, skittle_palette,
                                              skittle_counts, use_all=True,
                                              priority='random')
    cv2.imwrite('random_order_all.jpg', random_order_all)
    confidence_order_all, out_arr, out_count = skittlize(example_img_path, skittle_palette,
                                              skittle_counts, use_all=True,
                                              priority='confidence')
    cv2.imwrite('confidence_order_all.jpg', confidence_order_all)

    # USE SOME SKITTLES
    # pixel_order_some, random_order_some, confidence_order_some
    pixel_order_some, out_arr, out_count = skittlize(example_img_path, skittle_palette,
                                              skittle_counts, priority='none')
    cv2.imwrite('pixel_order_some.jpg', pixel_order_some)
    random_order_some, out_arr, out_count = skittlize(example_img_path, skittle_palette,
                                              skittle_counts, priority='random')
    cv2.imwrite('random_order_some.jpg', random_order_some)
    confidence_order_some, out_arr, out_count = skittlize(example_img_path, skittle_palette,
                                              skittle_counts,
                                              priority='confidence')
    cv2.imwrite('confidence_order_some.jpg', confidence_order_some)

if __name__=='__main__':
    main()
