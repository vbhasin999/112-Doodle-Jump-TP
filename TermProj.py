
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
YELLOW = ( 255, 211, 0)

#Window in which game will run
screenWidth = 600
screenHeight = 800
screenSize = (screenWidth, screenHeight)
screen = pygame.display.set_mode(screenSize)

background = pygame.image.load("/Users/vedantbhasin/Desktop/TPbackground.png")
background = pygame.transform.scale(background, screenSize)

#Global variables
dx = 0 #x position of mainCharacter
dy = 0 #y co-ordinate of mainCharacter
jumpHeight = 150
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
startingPlat = platform(platWidth, platHeight)
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
    
    if (50 > minHeightDist) or (maxHeightDist > 500):
        platPosListHorz.remove(x)
        platPosListVer.remove(y)
        continue

    if len(platPosListVer) > 8: #number of platforms on screen at once
        break
    
    plat = platform(platWidth, platHeight)
    plat.rect.x = x
    plat.rect.y = y
    plats.add(plat)
    all_sprites_list.add(plat)




#main character
mainCharacter = character([160, 750])

#screen.blit(mainCharacter.image, mainCharacter.rect)
char.add(mainCharacter)
all_sprites_list.add(mainCharacter)

#---------------------MAIN MENU SCREEN----------------------
def main_menu():
    clock = pygame.time.Clock()
    fps = 60
    menu = True
    keys = pygame.key.get_pressed()
    font = pygame.font.Font(None, 74)
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
    
                    if selected == "start":
                        selected = "leaderboard"
                    elif selected == "leaderboard":
                        selected = "quit"
                    elif selected == "quit":
                        selected = "start"

                elif event.key == pygame.K_UP:
                    if selected == "start":
                        selected = "quit"
                    elif selected == "leaderboard":
                        selected = "start"
                    elif selected == "quit":
                        selected = "leaderboard"

                elif event.key == pygame.K_RETURN:
                    if selected == "start":
                        menu = False
                        break
                    elif selected == "leaderboard":
                        pass
                    elif selected == "quit":
                        pygame.quit()
                        pygame.QUIT

            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                break

            
        # Main Menu UI
        background = pygame.image.load(
            "/Users/vedantbhasin/Desktop/TPbackground.png")
        background = pygame.transform.scale(background, screenSize)
        screen.blit(background, (0,0))

        if selected == "start":
            startText = font.render(f"START", 1, YELLOW)
            leaderBoardText = font.render(f"LEADERBOARD", 1, RED)
            quitText = font.render(f"QUIT", 1, RED)

        elif selected == "leaderboard":
            startText = font.render(f"START", 1, RED)
            leaderBoardText = font.render(f"LEADERBOARD", 1, YELLOW)
            quitText = font.render(f"QUIT", 1, RED)

        elif selected == "quit":
            startText = font.render(f"START", 1, RED)
            leaderBoardText = font.render(f"LEADERBOARD", 1, RED)
            quitText = font.render(f"QUIT", 1, YELLOW)

 
        # Main Menu Text
      
        screen.blit(startText, (screenWidth/2 - 80, 300))
        screen.blit(leaderBoardText, (screenWidth/2 - 200, 400))
        screen.blit(quitText, (screenWidth/2 - 60, 500))
        pygame.display.update()
        clock.tick(fps)

#---------------------GAME OVER SCREEN---------------------
def game_over():
    clock = pygame.time.Clock()
    fps = 60
    gameOver = True
    keys = pygame.key.get_pressed()
    font = pygame.font.Font(None, 74)
    selected = "restart"

    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if selected == "restart":
                        selected = "quit"
                    elif selected == "quit":
                        selected = "restart" 
                elif event.key == pygame.K_UP:
                    if selected == "restart":
                        selected = "quit"
                    elif selected == "quit":
                        selected = "restart"
                elif event.key == pygame.K_RETURN:
                    if selected == "restart":
                        gameOver = False
                        main_menu()
                    if selected == "quit":
                        pygame.QUIT
                        pygame.quit
                

            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                break

            
        # Main Menu UI
        background = pygame.image.load(
            "/Users/vedantbhasin/Desktop/game over.png")
        background = pygame.transform.scale(background, screenSize)
        screen.blit(background, (0,0))

        if selected == "restart":
            restartText = font.render(f"RESTART", 1, YELLOW)
            quitText = font.render(f"QUIT", 1, RED)

        elif selected == "quit":
            restartText = font.render(f"RESTART", 1, RED)
            quitText = font.render(f"QUIT", 1, YELLOW)

 
        # Main Menu Text
      
        screen.blit(restartText, (screenWidth/2 - 120, 500))
        screen.blit(quitText, (screenWidth/2 - 80, 600))

        pygame.display.update()
        clock.tick(fps)


main_menu() 
#---------------------MAIN PROGRAM LOOP--------------------

keepPlaying = True
clock = pygame.time.Clock()
fps = 60

while keepPlaying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepPlaying = False

    score += 1

    for p in plats:       #Platforms move down to simulate char moving up
        
        if p.rect.y >= screenHeight: #platform generation as the game scrolls
            p.kill()
            newPlatX = random.randint(0, screenWidth - platWidth)
            newPlatY = 0
            newPlat = platform(platWidth, platHeight)
            newPlat.rect.x = newPlatX
            newPlat.rect.y = newPlatY
            # check for min height dist here
            if (5 > minHeightDist) or (maxHeightDist > 500):
                continue
            plats.add(newPlat)
            all_sprites_list.add(newPlat)
            screen.blit(newPlat.image, newPlat.rect)

    freqOfEnemies = 5
    if score % (freqOfEnemies*fps) == 0 and score != 0:
        enemyChar = enemy(BLUE, 20, 40)
        enemyCharHeight = 20
        enemyCharWidth = 40
        enemyChar.rect.x = random.randint(0, screenWidth - enemyCharWidth)
        enemyChar.rect.y = 0
        enemies.add(enemyChar)
        all_sprites_list.add(enemyChar)
        screen.blit(enemyChar.image, enemyChar.rect)
            


    #Simulating gravity and terminal velocity
    #https://blog.withcode.uk/2016/06/doodle-jump-microbit-python-game-tutorial/
    if fallSpeed < 10:
        fallSpeed += 0.5
    mainCharacter.fall(fallSpeed)
    dy = mainCharacter.rect.y
    
    if dy > screenHeight:
        keepPlaying = False
        game_over()

    
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
        mainCharacter.jump(jumpHeight/2)
        dy = mainCharacter.rect.y
     

        for p in plats:
            p.rect.y += jumpHeight/2

        for e in enemies:
            e.rect.y += jumpHeight/2
            if e.rect.y > screenHeight:
                e.kill
        
    if pygame.sprite.groupcollide(char, enemies, True, False):
        keepPlaying = False
        game_over()

    

        

#Game Logic
    all_sprites_list.update()
    plats.update()
    enemies.update()
    char.update()

#initializes screen   
    screen.fill(WHITE)
    screen.blit(background, (0,0))
    screen.blit(mainCharacter.image, mainCharacter.rect)

#display scores
    font = pygame.font.Font(None, 74)
    text = font.render(f"score:{score}", 1, RED)
    screen.blit(text, (50,10))

#draws all sprites
    all_sprites_list.draw(screen)
    plats.draw(screen)
    enemies.update(screen)
    char.update(screen)
    
#Refresh Screen
    pygame.display.flip()

#sets the fps
    clock.tick(fps)
pygame.quit()
