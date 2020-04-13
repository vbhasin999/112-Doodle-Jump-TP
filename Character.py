import pygame

BLACK = ( 0, 0, 0)
RED = ( 255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
WHITE = ( 255, 255, 255)

class character(pygame.sprite.Sprite):
    def __init__(self, color, width, height): 
        super().__init__()
        
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        
        pygame.draw.rect(self.image, color, [ 0, 0, width, height]) 
        self.rect = self.image.get_rect()
        

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