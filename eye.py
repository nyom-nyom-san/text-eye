import pygame
import numpy
import random

x0, y0, x1, y1 = 0.3, 0.34, 0.8, 0.62
# EYE_BOX = (x0, y0, x1, y1)
CHARS = " .:+*%#@"

def main():

    #SetUP
    pygame.init()
    desktop_w, desktop_h = pygame.display.get_desktop_sizes()[0]
    # print(pygame.display.get_desktop_sizes())
    win_w = int(desktop_w * 0.75)
    win_h  = int(desktop_h * 0.75)
    screen = pygame.display.set_mode((win_w, win_h))


    clock = pygame.time.Clock()
    pygame.display.set_caption("THE EYE")
    running = True

    eye_layer = build_for_size(win_w, win_h)
    blink = BlinkController()
    layer_w, layer_h = eye_layer.get_size()

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

                elif event.key == pygame.K_SPACE:
                    blink.trigger_blink()

                elif event.key == pygame.K_f:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    win_w, win_h = screen.get_size()
                    eye_layer = build_for_size(win_w, win_h)
                    layer_w, layer_h = eye_layer.get_size()

        # 2. UPDATE
        blink.update(dt)

        # 3. DRAW
        openness = blink.openness
        new_h = max(1, int(layer_h * openness))
        squashed = pygame.transform.smoothscale(eye_layer, (layer_w, new_h))

        # keeping the squashed layer centered
        current_w, current_h = screen.get_size()
        left = (current_w - layer_w) // 2
        center_y = current_h // 2 

        top = center_y - new_h  // 2

        # finding the rectngle
        picture_top = center_y - layer_h // 2

        box_x = left + x0 * layer_w
        box_y = picture_top + y0* layer_h
        box_w = (x1 - x0) * layer_w
        box_h = (y1 - y0) * layer_h

        # filling up the color
        screen.fill((26, 0, 51))
        screen.blit(squashed, (left, top))

        rect = (int(box_x), int(box_y), int(box_w), int(box_h))
        pygame.draw.rect(screen, (255, 80, 80), rect, 1)

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

    def trigger_blink(self):
        self.state = "closing"
        self.timer = 0.0

def build_for_size(win_w, win_h):
    cell = 7
    target_h = win_h * 0.9
    rows = max(1, int(target_h // cell))
    cols = max(1, int(rows * (837/ 1032)))
    brightness = load_brightness("eye.png", (cols, rows))
    ink_grid = ink_from_brightness(brightness)
    font = pygame.font.SysFont("consolas", int(max(1, cell * 1.3)))
    glyphs = build_glyphs(font)
    layer = build_text_layer(ink_grid, glyphs, cell)

    return layer

def build_glyphs(font):
    glyphs = []
    for i, ch in enumerate(CHARS):
        level = i / (len(CHARS) - 1)
        shade = int(80 + 175 * level)
        color = (shade // 3, shade, shade)
        glyphs.append(font.render(ch, True, color))
    return glyphs

def build_text_layer(ink_grid, glyphs, cell):
    cols, rows = ink_grid.shape
    layer = pygame.Surface((cols * cell, rows * cell), pygame.SRCALPHA)
    for x in range(cols):
        for y in range(rows):
            ink = ink_grid[x,y]
            index  = int (ink * (len(CHARS) - 1))
            if index == 0:
                continue
            layer.blit(glyphs[index], (x * cell, y * cell))

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
