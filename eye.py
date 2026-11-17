import pygame
WIDTH, HEIGHT = 900, 600

def main():

    #SetUP
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("THE EYE")
    running = True

    brightness = load_brightness("eye.png", (100, 123))

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

        # 3. Draw
        screen.fill((26, 0, 51))

        #flip the display to screen
        pygame.display.flip()


    # Clean up
    pygame.quit()

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
