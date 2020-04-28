import pygame
import random
import math
from Platforms import platform
from MovingPlatforms import movingPlatform
from Character import character
from enemyCharacters import enemy
from Projectiles import projectile
from os import path

pygame.init()

# set the pygame window name 
pygame.display.set_caption('TURTLEDUEL')

#File which stores High score
highScoreFile = "highscore.txt"
leaderBoardFile = "leaderboard.txt"


#initialize some colors
BLACK = ( 0, 0, 0)
RED = ( 255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
WHITE = ( 255, 255, 255)
YELLOW = ( 255, 211, 0)
GOLD = (212,175,55)
SILVER = (192, 192, 192)
BRONZE = (176, 141, 87)
PINK = (255, 0, 144)

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
platformList = [] #2D of platform x and y positions
scoreList = []
enemiesList = []

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
def getMinDistBwPlats(y, L):
    #Helper function that gets the smallest distance between a platform and a list of platforms
    if L == []:
        return 1000
    closestPlatDist = 1000
    platX = y[0]
    platY = y[1]
    for pL in L:
        checkX = pL[0]
        checkY = pL[1]

        dist = getDistance(platX, platY, checkX, checkY)
        if dist < closestPlatDist:
            closestPlatDist = dist
    return closestPlatDist
  
def makeInitialPlatforms():
    #Makes the initial platforms on the screen
    keepMaking = True

    global platformList
    plat = platform(platWidth, platHeight)
    x = 50
    y = screenHeight - 400
    plat.rect.x = x
    plat.rect.y = y
    platformList.append([x,y])
    plats.add(plat)
    all_sprites_list.add(plat)

    while keepMaking:
        
        x = random.randint(0, screenWidth - platWidth)
        y = random.randint(0, screenHeight - platHeight)
        
        if getMinDistBwPlats([x,y], platformList) < 100:
            continue

        if len(platformList) > 9: #number of platforms on screen at once
            break
        
        plat = platform(platWidth, platHeight)
        plat.rect.x = x
        plat.rect.y = y
        platformList.append([x,y])
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

#----------------------LOAD HIGH SCORE---------------------
#https://www.youtube.com/watch?v=MFv1Ew_nGG0
#https://www.youtube.com/watch?v=Uh2ebFW8OYM
#Used the above videos to understand the process but still wrote code here myself
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
                        selected = "AI mode"
                    elif selected == "AI mode":
                        selected = "leaderboard"
                    elif selected == "leaderboard":
                        selected = "quit"
                    elif selected == "quit":
                        selected = "start"

                elif event.key == pygame.K_UP:
                    if selected == "start":
                        selected = "quit"
                    elif selected == "AI mode":
                        selected = "start"
                    elif selected == "leaderboard":
                        selected = "AI mode"
                    elif selected == "quit":
                        selected = "leaderboard"

                elif event.key == pygame.K_a:
                    AIGameLoop()

                elif event.key == pygame.K_RETURN:
                    if selected == "start":
                        menu = False
                        keepPlaying = True
                        restart()
                    elif selected == "AI mode":
                        restartAI()
                    elif selected == "leaderboard":
                        leaderboard()
                    elif selected == "quit":
                        pygame.quit()
                        pygame.QUIT

            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                break

        screen.fill(WHITE)
        # logo from https://namelix.com/
        background = pygame.image.load(
            "/Users/vedantbhasin/Desktop/turtlDuel.png")
        background = pygame.transform.scale(background, (350, 200))
        screen.blit(background, (125, 100))

        if selected == "start":
            startText = font.render(f"START", 1, YELLOW)
            AIText = font.render(f"AI MODE", 1, RED)
            leaderBoardText = font.render(f"LEADERBOARD", 1, RED)
            quitText = font.render(f"QUIT", 1, RED)
        
        elif selected == "AI mode":
            startText = font.render(f"START", 1, RED)
            AIText = font.render(f"AI MODE", 1, YELLOW)
            leaderBoardText = font.render(f"LEADERBOARD", 1, RED)
            quitText = font.render(f"QUIT", 1, RED)


        elif selected == "leaderboard":
            startText = font.render(f"START", 1, RED)
            AIText = font.render(f"AI MODE", 1, RED)
            leaderBoardText = font.render(f"LEADERBOARD", 1, YELLOW)
            quitText = font.render(f"QUIT", 1, RED)

        elif selected == "quit":
            startText = font.render(f"START", 1, RED)
            AIText = font.render(f"AI MODE", 1, RED)
            leaderBoardText = font.render(f"LEADERBOARD", 1, RED)
            quitText = font.render(f"QUIT", 1, YELLOW)
 
        # Main Menu Text
      
        screen.blit(startText, (screenWidth/2 - 80, 300))
        screen.blit(AIText, (screenWidth/2 - 110, 400))
        screen.blit(leaderBoardText, (screenWidth/2 - 200, 500))
        screen.blit(quitText, (screenWidth/2 - 60, 600))
        
        pygame.display.update()
        clock.tick(fps)

#--------------------LOAD LEADERBOARD----------------------
def loadLeaderboard():
    global Dir
    Dir = path.dirname(__file__)
    with open(path.join(Dir, leaderBoardFile), 'w') as lbf:
        lbf.write("No scores :(")

loadLeaderboard()
#--------------------LEADERBOARD SCREEN---------------------
def leaderboard():
    global Dir
    Dir = path.dirname(__file__)
    clock = pygame.time.Clock()
    fps = 60
    keys = pygame.key.get_pressed()
    font = pygame.font.Font(None, 48)
    leaderboardScreen = True

    with open(path.join(Dir, leaderBoardFile), 'r') as lbf:
        lineOne = lbf.readline()
        lineTwo = lbf.readline()
        lineThree = lbf.readline()
        lineFour = lbf.readline()
        lineFive = lbf.readline()

    while leaderboardScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                leaderboardScreen = False
                main_menu()

        #Icon made by Freepik from www.flaticon.com
        screen.fill(WHITE)
        background = pygame.image.load(
                "/Users/vedantbhasin/Desktop/podium.png")
        background = pygame.transform.scale(background, (screenHeight -200,
        screenWidth))
        screen.blit(background, (0,200))
      
        leaderboardTitleText = font.render(f"LEADERBOARD", 1, PINK)
        highestScorerText = font.render(f"HIGHEST SCORE: {lineOne}", 1, 
                                                                    GOLD)
        secHighestScorerText = font.render(f"SECOND HIGHEST: {lineTwo}", 1,
                                                                        SILVER)
        thirdHighestScorerText = font.render(f"THIRD HIGHEST: {lineThree}", 1, 
                                                                        BRONZE)
        fourthHighestScorerText = font.render(f"FOURTH HIGHEST: {lineFour}", 1, 
                                                                        BLUE)
        fifthHighestScorerText = font.render(f"FIFTH HIGHEST: {lineFive}", 1, 
                                                                        GREEN)

        smallFont = pygame.font.Font(None, 24)
        menuText = smallFont.render("Click anywhere to return to home-screen", 
                                                                        1, RED)
     
        screen.blit(menuText, (25,10))
        screen.blit(leaderboardTitleText, (screenWidth/2 - 200, 50))
        screen.blit(highestScorerText, (screenWidth/2 - 200, 150))
        screen.blit(secHighestScorerText, (screenWidth/2 - 200, 250))
        screen.blit(thirdHighestScorerText, (screenWidth/2 - 200, 350))
        screen.blit(fourthHighestScorerText, (screenWidth/2 - 200, 450))
        screen.blit(fifthHighestScorerText, (screenWidth/2 - 200, 550))
        
     
        pygame.display.update()
        clock.tick(fps) 
#---------------------GAME OVER SCREEN---------------------
def game_over(s):
    global highScore
    global scoreList
    score = s
    clock = pygame.time.Clock()
    fps = 60
    gameOver = True
    keys = pygame.key.get_pressed()
    font = pygame.font.Font(None, 74)
    selected = "restart"

    scoreList.append(score)
    updateLeaderboard(scoreList)

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

       
 #----------------------UPDATE LEADERBOARD----------
def descendingList(L):
    L.sort()
    L.reverse()
    return L

def updateLeaderboard(L):
    global Dir
    Dir = path.dirname(__file__)

    newList = descendingList(L)
  
    with open(path.join(Dir, leaderBoardFile), 'w') as lbf:
      try:
        lbf.write(str(newList[0]))
        lbf.write("\n")
        lbf.write(str(newList[1]))
        lbf.write("\n")
        lbf.write(str(newList[2]))
        lbf.write("\n")
        lbf.write(str(newList[3]))
        lbf.write("\n")
        lbf.write(str(newList[4]))
      
      except: 
        lbf.write("0")
    
#-----------------------DFS Functions--------------------
def getDistance(x1, y1, x2, y2):
    a = (x2-x1)**2
    b = (y2-y1)**2
    d = math.sqrt(a+b)
    return d

def enemyPlatDist(pL, LoE):
    closestEnemyDist = 1000
    platX = pL[0]
    platY = pL[1]
    for e in LoE:
        enemyX = e[0]
        enemyY = e[1]
        if enemyY > platY:
            continue
        else:
            dist = getDistance(platX, platY, enemyX, enemyY)
            if dist < closestEnemyDist:
                closestEnemyDist = dist
    return closestEnemyDist

def getClosestPlatDist(c, LoP, LoE):
    closestPlat = (0, 0)
    secondClosestPlat = (0,0)
    smallestDistToPlat = 10000
    charX = c[0] 
    charY = c[1]
    for plat in LoP:
      
        platX = plat[0] + platWidth/2  #using midpoint of platform
        platY = plat[1]
       
        dist = getDistance(charX, charY, plat[0], plat[1])

        if platY < 175 or enemyPlatDist(plat, LoE) < 200:
            continue

        if dist < smallestDistToPlat:
            secondClosestPlat = plat

            if platY < charY:
                smallestDistToPlat = dist
                closestPlat = plat

             
    if closestPlat == (0,0): return secondClosestPlat
    
    else: return closestPlat


#-----------------------RESTART GAME----------------------
def restart():
    global platformList
    global enemiesList
    all_sprites_list.empty()
    plats.empty()
    platformList = []
    enemiesList = []
    enemies.empty()
    char.empty()
    
    gameLoop()

#----------------------RESTART AI MODE------------------------
def restartAI():
    global platformList
    global enemiesList
    all_sprites_list.empty()
    plats.empty()
    platformList = []
    enemiesList = []
    enemies.empty()
    char.empty()

    AIGameLoop()

#---------------------Create enemy character function----------
def createEnemy():
    
    notCreated = True
    while notCreated:
       
        enemyChar = enemy(20, 40)
        enemyCharHeight = 20
        enemyCharWidth = 40
        enemyChar.rect.x = random.randint(0, screenWidth - enemyCharWidth)
        enemyChar.rect.y = 0
        x = enemyChar.rect.x
        y = enemyChar.rect.y

        if enemyPlatDist([x, y], platformList) < 150:
            continue

        elif enemyPlatDist([x, y], platformList) > 150:
            
            enemiesList.append([enemyChar.rect.x, enemyChar.rect.y])
            enemies.add(enemyChar)
            all_sprites_list.add(enemyChar)
            screen.blit(enemyChar.image, enemyChar.rect)
            notCreated = False
            break
#---------------------MAIN PROGRAM LOOP--------------------

def gameLoop():
    #Global variables
    dx = 0 #x position of mainCharacter
    dy = 0 #y co-ordinate of mainCharacter
    jumpHeight = 200
    global platformList
    global enemiesList
  

    fallSpeed = 0 #used to simulate gravity
    score = 0

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

        charPosition = (mainCharacter.rect.x, mainCharacter.rect.y)

        score += 1

        for p in plats:       #Platforms move down to simulate char moving up
            
            if p.rect.y >= screenHeight: #platform generation as the game scrolls
                saidPlat = [p.rect.x, p.rect.y]
                if saidPlat in platformList:
                    platformList.remove(saidPlat)

                p.kill()
                
                if len(plats.sprites()) < 11:
                    newPlatX = random.randint(0, screenWidth - platWidth)
                    newPlatY = 0
                    newPlatPos = [newPlatX, newPlatY]

                    if getMinDistBwPlats(newPlatPos, platformList) < 100:
                        continue

                    newPlat = platform(platWidth, platHeight)
                    newPlat.rect.x = newPlatX
                    newPlat.rect.y = newPlatY

                    
                    platformList.append([newPlatX, newPlatY])

                    plats.add(newPlat)
                    all_sprites_list.add(newPlat)
                    screen.blit(newPlat.image, newPlat.rect)
        
        freqOfMovingPlats = 1.5 #seconds between generation of a moving platform
        if score > 500:
            freqOfMovingPlats = 3 #fewer moving platforms at higher scores

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
            freqOfEnemies = 2.5 #more enemies appear at higher scores 
            
        if score % (freqOfEnemies*fps) == 0 and score != 0:
            createEnemy()
        
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
            nextPlat = getClosestPlatDist(charPosition, platformList, 
                                                                    enemiesList)
            
            for p in plats:
                p.rect.y += jumpHeight/2

            for pL in platformList:
                
                pL[1] += jumpHeight/2

            for e in enemies:
                e.rect.y += jumpHeight/2
                if e.rect.y > screenHeight:
                    saidEn = [e.rect.x, e.rect.y]
                    if saidEn in enemiesList:
                        enemiesList.remove(saidEn)
                    e.kill
                   

            for en in enemiesList:
                en[1] += jumpHeight/2
            
        if pygame.sprite.groupcollide(char, enemies, True, False):
            keepPlaying = False
            game_over(score)

        if pygame.sprite.groupcollide(projectiles, enemies, True, True):
            score += 50
    #Update
        all_sprites_list.update()
        plats.update()
        enemies.update()
        char.update()

    #initialize screen   
        screen.fill(WHITE)
        screen.blit(background, (0,0))
        screen.blit(mainCharacter.image, mainCharacter.rect)
        

    #display scores
        font = pygame.font.Font(None, 54)
        text = font.render(f"score:{score}", 1, RED)
        screen.blit(text, (25,10))

    #draw sprites
        all_sprites_list.draw(screen)
        plats.draw(screen)
        enemies.update(screen)
        char.update(screen)
        
    #Refresh Screen
        pygame.display.flip()

    #set fps
        clock.tick(fps)

#-----------------------AI Game Loop------------------
def AIGameLoop():
       #Global variables
    dx = 0 #x position of mainCharacter
    dy = 0 #y co-ordinate of mainCharacter
    jumpHeight = 200
    global platformList
    global enemiesList
   

    fallSpeed = 0 #used to simulate gravity
    score = 0

    

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

        charPosition = (mainCharacter.rect.x, mainCharacter.rect.y)

        score += 1

        for p in plats:       #Platforms move down to simulate char moving up
            
            if p.rect.y >= screenHeight: #platform generation as the game scrolls
                saidPlat = [p.rect.x, p.rect.y]
                if saidPlat in platformList:
                    platformList.remove(saidPlat)

                p.kill()
                
                if len(plats.sprites()) < 11:
                    newPlatX = random.randint(0, screenWidth - platWidth)
                    newPlatY = 0
                    newPlatPos = [newPlatX, newPlatY]
                    if getMinDistBwPlats(newPlatPos, platformList) < 100:
                        continue

                    newPlat = platform(platWidth, platHeight)
                    newPlat.rect.x = newPlatX
                    newPlat.rect.y = newPlatY

                    
                    platformList.append([newPlatX, newPlatY])

                    plats.add(newPlat)
                    all_sprites_list.add(newPlat)
                    screen.blit(newPlat.image, newPlat.rect)
        
        freqOfMovingPlats = 1.25 #seconds between generation of a moving platform
        if score > 500:
            freqOfMovingPlats = 2.5 #fewer moving platforms at higher scores

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
                       

            
        freqOfEnemies = 3 #Seconds between generation of next enemy 
        if score > 500:
            freqOfEnemies = 2 #more enemies appear at higher scores 
            
        if score % (freqOfEnemies*fps) == 0 and score != 0:
            createEnemy()
        
        for e in enemies:

            if abs(e.rect.x - charPosition[0]) < 25:
                if e.rect.y < charPosition[1]:
                    shuriken = projectile()
                    shuriken.rect.x = charPosition[0]
                    shuriken.rect.y = charPosition[1]
                    projectiles.add(shuriken)
                    all_sprites_list.add(shuriken)
                    screen.blit(shuriken.image, shuriken.rect)
                
        
        #Simulating gravity and terminal velocity
        #https://blog.withcode.uk/2016/06/doodle-jump-microbit-python-game-tutorial/
        if fallSpeed < 10:
            fallSpeed += 0.1
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
      
        
        for s in projectiles:
            s.rect.y -= 20 



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

            for e in enemies:
                
                if abs(e.rect.x - charPosition[0]) < 25:
                    if e.rect.y < charPosition[1]:
                        shuriken = projectile()
                        shuriken.rect.x = charPosition[0]
                        shuriken.rect.y = charPosition[1]
                        projectiles.add(shuriken)
                        all_sprites_list.add(shuriken)
                        screen.blit(shuriken.image, shuriken.rect)

            #mainCharacter.jump(jumpHeight/10)
            dy = mainCharacter.rect.y
            
            
            for p in plats:
                p.rect.y += jumpHeight/2

            for pL in platformList:
                
                pL[1] += jumpHeight/2

            for e in enemies:
                e.rect.y += jumpHeight/2
                if e.rect.y > screenHeight:
                    saidEn = [e.rect.x, e.rect.y]
                    if saidEn in enemiesList:
                        enemiesList.remove(saidEn)
                    e.kill

            for en in enemiesList:
                en[1] += jumpHeight/2 

            nextPlat = getClosestPlatDist(charPosition, platformList, 
                                                                enemiesList)
            
            nextPlatX = nextPlat[0]
            nextPlatY = nextPlat[1]

            if nextPlat[1] < charPosition[1]:
             
                heightDifference = charPosition[1] - nextPlatY
                mainCharacter.jump(heightDifference)

                if nextPlatX < mainCharacter.rect.x:
                 
                    widthDifference = mainCharacter.rect.x - nextPlatX
                    mainCharacter.moveLeft(widthDifference)
                    
                elif nextPlatX > mainCharacter.rect.x:
                   
                    widthDifference = nextPlatX - mainCharacter.rect.x
                    mainCharacter.moveRight(widthDifference)

            
        if pygame.sprite.groupcollide(char, enemies, True, False):
            keepPlaying = False
            game_over(score)

        if pygame.sprite.groupcollide(projectiles, enemies, True, True):

            score += 50

    #Update
        all_sprites_list.update()
        plats.update()
        enemies.update()
        char.update()

    #initialize screen   
        screen.fill(WHITE)
        screen.blit(background, (0,0))
        screen.blit(mainCharacter.image, mainCharacter.rect)
        

    #display scores
        font = pygame.font.Font(None, 54)
        text = font.render(f"score:{score}", 1, RED)
        screen.blit(text, (25,10))

    #draw sprites
        all_sprites_list.draw(screen)
        plats.draw(screen)
        enemies.update(screen)
        char.update(screen)
        
    #Refresh the screen
        pygame.display.flip()

    #set the fps
        clock.tick(fps)

main_menu() 
pygame.quit()

