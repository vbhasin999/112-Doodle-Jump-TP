import pygame

BLACK = ( 0, 0, 0)
RED = ( 255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
WHITE = ( 255, 255, 255)

class projectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Icon made by Freepik from www.flaticon.com
        projectileImage = pygame.image.load(
            "/Users/vedantbhasin/Desktop/shuriken.png")
        projectileImage = pygame.transform.scale(projectileImage, (25, 25))
        self.image = projectileImage
        self.rect = self.image.get_rect()