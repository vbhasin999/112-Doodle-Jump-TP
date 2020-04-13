
import pygame
import random
from Platforms import platform
from Character import character
from enemyCharacters import enemy

pygame.init()

# set the pygame window name 
pygame.display.set_caption('Doodle jump like game')

#initialize some colors
BLACK = ( 0, 0, 0)
RED = ( 255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
WHITE = ( 255, 255, 255)

#Window in which game will run
screenWidth = 400
screenHeight = 800
size = (screenWidth, screenHeight)
screen = pygame.display.set_mode(size)

#Global variables
dx = 0 #x position of mainCharacter
dy = 0 #y co-ordinate of mainCharacter
fallSpeed = 0 #used to simulate gravity
score = 0

#List of all sprites
all_sprites_list = pygame.sprite.Group()

#Initializing groups of sprites
char = pygame.sprite.Group()
plats = pygame.sprite.Group()
enemies = pygame.sprite.Group()


#starting platform
platWidth = 100
platHeight = 15
startingPlat = platform(GREEN, platWidth, platHeight)
startingPlat.rect.x = 150
startingPlat.rect.y = 750
all_sprites_list.add(startingPlat)
plats.add(startingPlat)


#Make platforms
def getMinDistBwPlats(y, L): #checks dist between plats vertically
    if L == []:
        return y
    elif len(L) == 1:
        return y 
    else:
        return min (abs(L[0] - y), getMinDistBwPlats(y, L[1:]))

def getMaxDistBwPlats(y, L): #checks dist between plats vertically
    if L == []:
        return y
    elif len(L) == 1:
        return y 
    else:
        return max (abs(L[0] - y), getMinDistBwPlats(y, L[1:]))

keepMaking = True

platPosListVer = []
platPosListHorz = []
while keepMaking:
    
    x = random.randint(0, screenWidth - platWidth)
    y = random.randint(0, screenHeight - platHeight)
    
    platPosListHorz.append(x)
    platPosListVer.append(y)

    minHeightDist = getMinDistBwPlats(y, platPosListVer)
    maxHeightDist = getMaxDistBwPlats(y, platPosListVer)
  
    minWidthDist = getMinDistBwPlats(x, platPosListHorz)
    
    if (5 > minHeightDist) or (maxHeightDist > 500):
        platPosListHorz.remove(x)
        platPosListVer.remove(y)
        continue

    if len(platPosListVer) > 10:
        break
    
    plat = platform(GREEN, platWidth, platHeight)
    plat.rect.x = x
    plat.rect.y = y
    plats.add(plat)
    all_sprites_list.add(plat)




#main character
mainCharacter = character(RED, 20, 20)
dx = 160
dy = 750
mainCharacter.rect.x = dx
mainCharacter.rect.y = dy
char.add(mainCharacter)
all_sprites_list.add(mainCharacter)



#---------------------MAIN PROGRAM LOOP--------------------
keepPlaying = True
clock = pygame.time.Clock()
fps = 60

while keepPlaying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepPlaying = False

    for p in plats:       #Platforms move down to simulate char moving up
        '''
        if score < 30: p.rect.y += 4  #faster scrolling as score increases
        elif 30 < score < 60: p.rect.y += 6
        else: p.rect.y += 8
        '''
        if p.rect.y >= screenHeight: #platform generation as the game scrolls
            p.kill()
            newPlatX = random.randint(0, screenWidth - platWidth)
            newPlatY = 0
            newPlat = platform(GREEN, platWidth, platHeight)
            newPlat.rect.x = newPlatX
            newPlat.rect.y = newPlatY
            # check for min height dist here
            if (5 > minHeightDist) or (maxHeightDist > 500):
                continue
            plats.add(newPlat)
            all_sprites_list.add(newPlat)

  
    if score % 15 == 0 and score != 0:
        
        if not enemies.has():
            enemyChar = enemy(BLUE, 20, 40)
            enemyCharHeight = 20
            enemyCharWidth = 40
            enemyChar.rect.x = random.randint(0, screenWidth - enemyCharWidth)
            enemyChar.rect.y = 0
            enemies.add(enemyChar)
            print(1, enemies.has())
            print(2, char.has())
            print(3, plats.has)
            all_sprites_list.add(enemyChar)
            

    for p in plats:
        if score < 30: p.rect.y += 4  #faster scrolling as score increases
        elif 30 < score < 60: p.rect.y += 6
        else: p.rect.y += 8
    
    for e in enemies:
        if score < 30: e.rect.y += 4  #faster scrolling as score increases
        elif 30 < score < 60: e.rect.y += 6
        else: e.rect.y += 8
        if e.rect.y >= screenHeight: 
            e.kill()


    #Simulating gravity and terminal velocity
    #https://blog.withcode.uk/2016/06/doodle-jump-microbit-python-game-tutorial/
    if fallSpeed < 10:
        fallSpeed += 0.30
    mainCharacter.fall(fallSpeed)
    dy = mainCharacter.rect.y
    
    if dy > screenHeight:
        keepPlaying = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mainCharacter.moveLeft(5)
        dx -= 5
        if dx < 0:
            mainCharacter.moveRight(screenWidth + dx)
            dx += screenWidth

    if keys[pygame.K_RIGHT]:
        mainCharacter.moveRight(5)
        dx += 5
        if dx > screenWidth:
            mainCharacter.moveLeft(screenWidth)
            dx -= screenWidth

    
    if keys[pygame.K_UP]:
        fallSpeed = 0
        mainCharacter.jump(15)
        dy -= 15
    
    if pygame.sprite.groupcollide(char, plats, False, False):
        fallSpeed = 0
        mainCharacter.jump(200)
        dy = mainCharacter.rect.y
        score += 1

#display scores
    font = pygame.font.Font(None, 74)
    text = font.render(f"score:{score}", 1, RED)
    screen.blit(text, (50,10))
        

#Game Logic
    all_sprites_list.update()

#initializes screen    
    screen.fill(WHITE)

#draws all sprites

    all_sprites_list.draw(screen)
    
#Refresh Screen
    pygame.display.flip()

#sets the fps
    clock.tick(fps)
pygame.quit()
