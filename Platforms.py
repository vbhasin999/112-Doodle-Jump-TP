import pygame

BLACK = ( 0, 0, 0)
RED = ( 255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
WHITE = ( 255, 255, 255)

class platform(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super().__init__()
        platImage = pygame.image.load(
            "/Users/vedantbhasin/Desktop/TPplatform.png")
        platImage = pygame.transform.scale(platImage, (width, height))
        self.image = platImage

        self.rect = self.image.get_rect()