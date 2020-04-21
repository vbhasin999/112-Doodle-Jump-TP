import pygame

BLACK = ( 0, 0, 0)
RED = ( 255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
WHITE = ( 255, 255, 255)



class character(pygame.sprite.Sprite):
    def __init__(self, pos): 
        super().__init__()

        #Icon made by Surang from www.flaticon.com
        
        mainCharImage = pygame.image.load(
            "/Users/vedantbhasin/Desktop/raphael.png").convert_alpha()
       
        mainCharImage = pygame.transform.scale(mainCharImage, (90, 90)) 
        
        self.image = mainCharImage

        self.rect = mainCharImage.get_rect()

        #methods for character movement

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        
    def jump(self, pixels):
        self.rect.y -= pixels

    def fall(self, pixels):
        self.rect.y += pixels

    #checking for collisions
    def collide(self, group1):
        if pygame.sprite.spritecollide(self, group1, False):
            return True
    
    #Functions to wrap around
    def wrapAroundLeft(self):
        self.rect.x = screenWidth

    def wrapAroundRight(self):
        self.rect.x = 0