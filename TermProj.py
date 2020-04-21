import pygame
import random
from Platforms import platform
from MovingPlatforms import movingPlatform
from Character import character
from enemyCharacters import enemy
from Projectiles import projectile
from os import path

pygame.init()

# set the pygame window name 
pygame.display.set_caption('NINJA TURTLE DOODLE-JUMP')

#File which stores High score
highScoreFile = "highscore.txt"


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

#https://www.zedge.net/wallpaper/88d7bd93-ad86-42d1-88ae-5e973b10edc2?utm_source=web&utm_medium=item&utm_campaign=sharing
background = pygame.image.load("/Users/vedantbhasin/Desktop/TPbackground.png")
background = pygame.transform.scale(background, screenSize)

#Global variables
dx = 0 #x position of mainCharacter
dy = 0 #y co-ordinate of mainCharacter
jumpHeight = 200
fallSpeed = 0 #used to simulate gravity
score = 0
platformHeightList = []
platformXList = []

#List of all sprites
all_sprites_list = pygame.sprite.Group()

#Initializing groups of sprites
char = pygame.sprite.Group()
plats = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

#starting platform

platWidth = 100
platHeight = 75
startingPlat = platform(platWidth, platHeight)
startingPlat.rect.x = 150
startingPlat.rect.y = 750
all_sprites_list.add(startingPlat)
plats.add(startingPlat)


#Make platforms
def getClosestPlat(y, L):
    closestPlatDy = 10000
    smallestHeightDiff = 10000
    for h in L:
        heightDiff = abs(y-h)
        if heightDiff < smallestHeightDiff:
            smallestHeightDiff = heightDiff
            closestPlatDy = h
    return closestPlatDy

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


def makeInitialPlatforms():
    keepMaking = True

    global platformHeightList
    global platformXList

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

        if len(platPosListVer) > 7: #number of platforms on screen at once
            break
        
        plat = platform(platWidth, platHeight)
        plat.rect.x = x
        plat.rect.y = y
        platformHeightList.append(y)
        platformXList.append(x)
        plats.add(plat)
        all_sprites_list.add(plat)



def initializeMainChar():
    #main character
    global mainCharacter 
    mainCharacter = character([160, 750])


    char.add(mainCharacter)
    all_sprites_list.add(mainCharacter)
   
def initializeMovingPlatforms():
    movingPlat = movingPlatform()
    movingPlat.rect.x = 0
    movingPlat.rect.y = 0
    plats.add(movingPlat)
    all_sprites_list.add(movingPlat)
    screen.blit(movingPlat.image, movingPlat.rect)
#----------------------LOAD HIGH SCORE---------------
#https://www.youtube.com/watch?v=MFv1Ew_nGG0
#Used the above video to understand the process but still wrote code here myself
def loadData():
    global highScore
    global Dir
    Dir = path.dirname(__file__)
    with open(path.join(Dir, highScoreFile), 'w') as f:
        try:
            highScore = int(f.read())

        except:
            highScore = 0

loadData()
#---------------------MAIN MENU SCREEN----------------------
def main_menu():
    #https://www.sourcecodester.com/tutorials/python/11784/python-pygame-simple-main-menu-selection.html
    #Used above website to understand how to make a main menu screen while highlighting selected options
    global highScore
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
                        keepPlaying = True
                        restart()
                    elif selected == "leaderboard":
                        pass
                    elif selected == "quit":
                        pygame.quit()
                        pygame.QUIT

            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                break

        
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

        HS = font.render(f"HIGH SCORE:{highScore}", 1, RED)
 
        # Main Menu Text
      
        screen.blit(startText, (screenWidth/2 - 80, 300))
        screen.blit(leaderBoardText, (screenWidth/2 - 200, 400))
        screen.blit(quitText, (screenWidth/2 - 60, 500))
        screen.blit(HS, (screenWidth/2 - 180, 100))
        pygame.display.update()
        clock.tick(fps)

#---------------------GAME OVER SCREEN---------------------
def game_over(s):
    global highScore
    score = s
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
                        restart()
                    if selected == "quit":
                        gameOver = False
                        main_menu()
                

            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                break
        
        #https://www.pinterest.com/pin/312085449162860319/?nic_v1=1aPiKnxPv3ti0iWggdOCVMkRKnhzFYqmXrH11BgZjK99spgHF9G3EQaYXNU3msgqj%2B
        background = pygame.image.load(
            "/Users/vedantbhasin/Desktop/sadPepe.png")
        background = pygame.transform.scale(background, screenSize)
        screen.blit(background, (0,0))
    
        
        if selected == "restart":
            restartText = font.render(f"RESTART", 1, YELLOW)
            quitText = font.render(f"QUIT", 1, RED)

        elif selected == "quit":
            restartText = font.render(f"RESTART", 1, RED)
            quitText = font.render(f"QUIT", 1, YELLOW)

        if score > highScore:
            with open(path.join(Dir, highScoreFile), 'w') as f:
                f.write(str(score))
            highScore = score
            scoreText = font.render(f"score: {score}", 1, RED)
            HS = font.render(f"NEW HIGH SCORE", 1, RED)
        
        elif score <= highScore:
            scoreText = font.render(f"score: {score}", 1, RED)
            HS = font.render(f"HIGH SCORE: {highScore}", 1, RED)
     
        gameOverText = font.render(f"GAME OVER", 1, RED)

        screen.blit(gameOverText, (screenWidth/2 - 150, 50))
        screen.blit(restartText, (screenWidth/2 - 120, 500))
        screen.blit(quitText, (screenWidth/2 - 80, 600))
        screen.blit(HS, (screenWidth/2 - 200, 150))
        screen.blit(scoreText, (screenWidth/2 - 125, 250))

        pygame.display.update()
        clock.tick(fps)    


#-----------------------RESTART GAME----------------------
def restart():
    all_sprites_list.empty()
    plats.empty()
    enemies.empty()
    char.empty()
    
    gameLoop()

#---------------------MAIN PROGRAM LOOP--------------------

def gameLoop():
    #Global variables
    dx = 0 #x position of mainCharacter
    dy = 0 #y co-ordinate of mainCharacter
    jumpHeight = 200

    fallSpeed = 0 #used to simulate gravity
    score = 0
    global platformHeightList
    global platformXList

    keepPlaying = True
    clock = pygame.time.Clock()
    fps = 50
    makeInitialPlatforms()
    initializeMainChar()
    
    movingPlat = movingPlatform()
    movingPlat.rect.x = 0
    movingPlat.rect.y = 0
    plats.add(movingPlat)
    all_sprites_list.add(movingPlat)
    screen.blit(movingPlat.image, movingPlat.rect)

    while keepPlaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepPlaying = False

        score += 1

        for p in plats:       #Platforms move down to simulate char moving up
            
            if p.rect.y >= screenHeight: #platform generation as the game scrolls
        
                if p.rect.y in platformHeightList:
                    platformHeightList.remove(p.rect.y)
                    platformXList.remove(p.rect.x)
                p.kill()
                
                if len(plats.sprites()) < 8:
                    newPlatX = random.randint(0, screenWidth - platWidth)
                    newPlatY = 0
                   
                    newPlat = platform(platWidth, platHeight)
                    newPlat.rect.x = newPlatX
                    newPlat.rect.y = newPlatY

                    platformHeightList.append(newPlatY)
                    platformXList.append(newPlatX)

                    plats.add(newPlat)
                    all_sprites_list.add(newPlat)
                    screen.blit(newPlat.image, newPlat.rect)
        
        freqOfMovingPlats = 1.5 #seconds between generation of a moving platform

        if score >= 0:
            if score % (freqOfMovingPlats * fps) == 0:
                movingPlat = movingPlatform()
                movingPlat.rect.x = random.randint(0, screenWidth - platWidth)
                movingPlat.rect.y = 0
                plats.add(movingPlat)
                all_sprites_list.add(movingPlat)
                screen.blit(movingPlat.image, movingPlat.rect)


            for mp in plats:
                if type(mp) == movingPlatform:
                    if mp.rect.x >= screenWidth:
                        mp.rect.x = 0
                    else:
                        mp.moveRight(1)

        freqOfEnemies = 5 #Seconds between generation of next enemy 
        if score > 500:
            freqOfEnemies = 2.5 
        if score % (freqOfEnemies*fps) == 0 and score != 0:
            enemyChar = enemy(20, 40)
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
        
        if dy < 0:
            mainCharacter.rect.y = 0
            dy = mainCharacter.rect.y
        if dy > screenHeight:
            keepPlaying = False
            game_over(score)

        
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

        if keys[pygame.K_SPACE]:
            shuriken = projectile()
            shuriken.rect.x = dx
            shuriken.rect.y = dy
            projectiles.add(shuriken)
            all_sprites_list.add(shuriken)
            screen.blit(shuriken.image, shuriken.rect)
        
        for s in projectiles:
            s.rect.y -= 15 



        #---------------------Pause function------------
        pause = False
        if keys[pygame.K_p]:
            
            if pause == False:
                pause = True
            elif pause == True:
                pause = False

            while pause == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                          
                            pause = False
                            break
                            
                            
        
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
            game_over(score)

        if pygame.sprite.groupcollide(projectiles, enemies, True, True):
            score += 50
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
        font = pygame.font.Font(None, 54)
        text = font.render(f"score:{score}", 1, RED)
        screen.blit(text, (25,10))

    #draws all sprites
        all_sprites_list.draw(screen)
        plats.draw(screen)
        enemies.update(screen)
        char.update(screen)
        
    #Refresh Screen
        pygame.display.flip()

    #sets the fps
        clock.tick(fps)

main_menu() 
pygame.quit()

