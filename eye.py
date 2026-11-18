import pygame
WIDTH, HEIGHT = 1800, 1200
CELL = 6
FONT_SIZE = 8
GRID_SIZE = (100,123)
CHARS = " .:+*%#@"

def main():

    #SetUP
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("THE EYE")
    running = True

    brightness = load_brightness("eye.png", GRID_SIZE)
    cols, rows = brightness.shape

    font = pygame.font.SysFont("consolas", FONT_SIZE)
    glyphs = build_glyphs(font)


    # The loop
    while running is True:

        # Time since last frame ms -> s
        dt = clock.tick(60) / 1000

        # 1. TIME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Exiting the game...")
                    running = False

        # 2. UPDATE

        # 3. DRAW

        # filling up the color
        screen.fill((26, 0, 51))

        for x in range(cols):
            for y in range(rows):
                ink = 1 - brightness[x,y]
                index  = int (ink * (len(CHARS) - 1))
                if index == 0:
                    continue
                screen.blit(glyphs[index], (x * CELL, y * CELL))


        # flip the display to screen
        pygame.display.flip()


    # Clean up
    pygame.quit()


def build_glyphs(font):
    glyphs = []
    for i, ch in enumerate(CHARS):
        level = i / (len(CHARS) - 1)
        shade = int(80 + 175 * level)
        color = (shade // 3, shade, shade)
        glyphs.append(font.render(ch, True, color))
    return glyphs

def load_brightness(path, target_size):

    image = pygame.image.load(path)
    print(image.get_size())

    small = pygame.transform.smoothscale(image, target_size)
    print(small.get_size())

    pixels = pygame.surfarray.array3d(small)
    print(pixels.shape)

    brightness = pixels.mean(axis=2)
    print(brightness.shape)

    brightness = brightness / 255
    print(brightness.min(), brightness.max())


    return brightness

if __name__ == "__main__":
    main()
