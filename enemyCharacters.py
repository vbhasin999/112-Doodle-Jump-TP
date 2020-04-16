import pygame

BLACK = ( 0, 0, 0)
RED = ( 255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
WHITE = ( 255, 255, 255)

#Icon made by Surang from www.flaticon.com

class enemy(pygame.sprite.Sprite):
    def __init__(self, width, height): 
        super().__init__()

        enemyImage = pygame.image.load(
            "/Users/vedantbhasin/Desktop/cartoon.png")

        enemyImage = pygame.transform.scale(enemyImage, (70, 70))


        
        self.image = enemyImage


        self.rect = self.image.get_rect()
        

        #methods for character movement

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels