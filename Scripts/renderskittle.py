#
# pops up a graphic window and draws circles instead of pixels
#
import pygame,sys
from pygame.locals import *  # pygame.locals.QUIT --> QUIT
BACKGROUND = (217,217,217)

def main():
    # test
    diam=10
    cols=10
    rows=10
    testPalette = ["#378e30", "#912439", "#dc5343", "#c5ba5e", "#1d1b20", "#ffffff"]
    testPixels = [[None for y in range(cols)] for x in range(rows)]
    ix = 0
    for col in range(cols):
        for row in range(rows):
            ix = (ix + 1) % 5
            testPixels[col][row] = ix
    renderSkittles(diam, cols, rows, testPixels, testPalette);
    print("Leaving Main function")
    return

def renderOneSkittle(surface, diameter, color, row, column):
    x = column * diameter * 2 + diameter; # add offset to make it show on screen
    y = row * diameter * 2 + diameter;    # add offset in Y direction as well
    pygame.draw.circle(surface, color, (x,y), diameter)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def renderSkittles(diameter, w, h, poxels, palette):
    pygame.init()
    screen = pygame.display.set_mode((w*diameter*2,h*diameter*2))
    pygame.display.set_caption("Skittles")
    clock = pygame.time.Clock() # creating the game clock 
    showingWindow = True

    while showingWindow: # Game Loop
        for event in pygame.event.get(): # checking for user input
            if event.type==QUIT: #input to close the window
                pygame.quit()
                #sys.exit()  # maybe don't do this
                showingWindow=False

        if showingWindow:
            screen.fill(BACKGROUND)
            for r in range(h):
                for c in range(w):
                    color_index = poxels[r][c]
                    colorHex = palette[color_index]
                    renderOneSkittle(screen, diameter, hex_to_rgb(colorHex), r, c)
            pygame.display.update()

    return

if __name__ == "__main__":
    main()
    
