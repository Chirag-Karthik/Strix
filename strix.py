import random
import math
import pygame
from pygame import mixer

#initializing pygame
pygame.init()

#SCREEN
screen=pygame.display.set_mode((640,360))

#Background
background=pygame.image.load("background.png")
#background song
mixer.music.load("background.wav")
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("STRIX")
icon=pygame.image.load("space-ship.png")
pygame.display.set_icon(icon)

#player
playerimg=pygame.image.load("spaceship.png")
playerX=300
playerY=300
playerX_change=0

#enemy list
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
     # enemy 
    enemyimg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,640))
    enemyY.append(random.randint(50,100))
    enemyX_change.append(1)
    enemyY_change.append(30)

#bullet
bulletimg=pygame.image.load("bullet.png")
bulletX=0
bulletY=300
bulletX_change=0
bulletY_change=3.7
#ready=can't see the bullet
#fire=shooting
bullet_state="ready"

#score
score_value=0
font=pygame.font.Font(("freesansbold.ttf"), 32)

#text location
textX=10
textY=10

#game over text
over_font=pygame.font.Font(("freesansbold.ttf"), 128)

#score func
def show_score(x,y):
    score=font.render("Score: "+str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text(x,y):
    over_text=font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (x,y))

#player location func
def player(x,y):
    screen.blit(playerimg,(x,y))

#enemy func
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+8,y+5))

#collision func
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<13:
        return True
    else:
        return False


#game loop
running=True
while running:
    #game upadate
    pygame.display.update()
    
    #background color(R,G,B)
    screen.fill((243,0,120))
    #background img
    screen.blit(background, (0,0))
    
    #key reading
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
        #if key pressed  check weather its right or left
        if event.type==pygame.KEYDOWN:
        
            if event.key==pygame.K_LEFT:
                playerX_change=-3
            if event.key==pygame.K_RIGHT:
                playerX_change=3
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet( bulletX, bulletY)
        #key released
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0


    #player boundry
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=608:
        playerX=608

    #enemy movement
    for i in range(num_of_enemies):

        #game over
        if enemyY[i]>250:
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            game_over_text(215,160)
            break


        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=1
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=608:
            enemyX_change[i]=-1
            enemyY[i]+=enemyY_change[i]
        #collision
        collision=isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound=mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY=300
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,640)
            enemyY[i]=random.randint(50,100)
        enemy(enemyX[i],enemyY[i],i)

    #bullet movement
    if bulletY<=0:
        bulletY=300
        bullet_state="ready"

    if bullet_state is "fire":
        fire_bullet( bulletX, bulletY)
        bulletY-=bulletY_change
    
    
    show_score(textX,textY)
    player(playerX,playerY)
    

