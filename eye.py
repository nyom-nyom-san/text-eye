import pygame
import numpy
import random

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

    ink_grid = ink_from_brightness(brightness)
    eye_layer = build_text_layer(ink_grid, glyphs)

    blink = BlinkController()



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
        blink.update(dt)

        # 3. DRAW

        # filling up the color
        screen.fill((26, 0, 51))
        screen.blit((eye_layer), (0,0))


        # flip the display to screen
        pygame.display.flip()


    # Clean up
    pygame.quit()

class BlinkController:
    def __init__(self):
        self.state = "waiting"
        self.timer = 0.0
        self.wait_duration = random.uniform(2.0, 5.0)
        self.close_duration = 0.1
        self.open_duration = 0.15
        self.openness = 1.0


    def update(self, dt):
        self.timer += dt

        match self.state:
            case "waiting":
                if self.timer >= self.wait_duration:
                    self.state = "closing"
                    self.timer = 0.0

            case "closing":
                progress = min(1.0, self.timer / self.close_duration)
                self.openness = 1 - progress
                if self.timer >= self.close_duration:
                    self.openness = 0
                    self.state = "opening"
                    self.timer = 0.0

            case "opening":
                progress = min(1.0, self.timer / self.open_duration)
                self.openness = progress
                if progress >= 1:
                    self.openness = 1.0
                    self.state = "waiting"
                    self.wait_duration = random.uniform(2.0, 5.0)
                    self.timer = 0
        return self.openness


def build_glyphs(font):
    glyphs = []
    for i, ch in enumerate(CHARS):
        level = i / (len(CHARS) - 1)
        shade = int(80 + 175 * level)
        color = (shade // 3, shade, shade)
        glyphs.append(font.render(ch, True, color))
    return glyphs

def build_text_layer(ink_grid, glyphs):
    cols, rows = ink_grid.shape
    layer = pygame.Surface((cols * CELL, rows * CELL), pygame.SRCALPHA)
    for x in range(cols):
        for y in range(rows):
            ink = ink_grid[x,y]
            index  = int (ink * (len(CHARS) - 1))
            if index == 0:
                continue
            layer.blit(glyphs[index], (x * CELL, y * CELL))

    return layer

def ink_from_brightness(brightness):

    #contrasting the ink
    ink = 1 - brightness
    lo = 0.3
    hi = 0.95
    ink = (ink - lo) / (hi - lo)
    ink = numpy.clip(ink, 0, 1)
    ink = ink ** 0.7

    return ink

def load_brightness(path, target_size):

    image = pygame.image.load(path)
    # print(image.get_size())

    small = pygame.transform.smoothscale(image, target_size)
    # print(small.get_size())

    pixels = pygame.surfarray.array3d(small)
    # print(pixels.shape)

    brightness = pixels.mean(axis=2)
    # print(brightness.shape)

    brightness = brightness / 255
    # print(brightness.min(), brightness.max())


    return brightness

if __name__ == "__main__":
    main()
