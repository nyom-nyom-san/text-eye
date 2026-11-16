import pygame
WIDTH, HEIGHT = 900, 600

def main():

    #SetUP
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("THE EYE")
    running = True

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
                    print("Exisiting the game...")
                    running = False

        # 2. UPDATE

        # 3. Draw
        screen.fill((26, 0, 51))

        #flip the display to screen
        pygame.display.flip()


    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()