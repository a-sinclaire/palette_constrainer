# Amelia Sinclaire 2024

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
