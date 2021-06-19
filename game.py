import pygame
import random
import math
from pygame import mixer

# initlizing game
pygame.init()

# window
screen = pygame.display.set_mode((800,600))

# background
# background = pygame.image.load('img/background.png')
mixer.music.load('audio/background.mp3')
mixer.music.play()

# title and icon
pygame.display.set_caption("img/Space War")
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('img/fighter.png')
playerX = 370
playerY = 495
playerX_change = 0

# bullet
bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 495
bulletX_change = 0
bulletY_change = 5
bullet_state = 'ready'

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

eI1 = pygame.image.load('img/alien.png')
eI2 = pygame.image.load('img/monster.png')
eI3 = pygame.image.load('img/alien2.png')
eI4 = pygame.image.load('img/alien3.png')
eI5 = pygame.image.load('img/alien4.png')
eI6 = pygame.image.load('img/alien5.png')


no_of_enemy = 5
for i in range(no_of_enemy):
    enemyImg.append(random.choice([eI1,eI2,eI3,eI4,eI5,eI6]))
    enemyX.append(random.randint(0,733))
    enemyY.append(random.randint(20,180))
    enemyX_change.append(1)
    enemyY_change.append(40)


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 5
textY = 5

over_font = pygame.font.Font('freesansbold.ttf',62)

def showScore(x,y):
    score = font.render('Score :'+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    game_over = over_font.render('GAME OVER',True,(255,255,255))
    with open('Score/highScore.txt','r') as hs:
        hscore = hs.read()
    high_score = font.render('Best Score :'+ hscore,False,(255,255,255))
    screen.blit(game_over,(200,225))
    screen.blit(high_score,(268,310))
 
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+20.5,y+5))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    X = enemyX-bulletX
    Y = enemyY-bulletY
    dist = math.sqrt(math.pow(X,2)+math.pow(Y,2))
    if dist <= 27:
        return True
    else:
        return False

# game loop
running = True
while running:
    # background color
    screen.fill((0,0,0))
    # screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('audio/bullet.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 734:
        playerX = 734  

    for i in range(no_of_enemy):

        if enemyY[i] > 485:
            for j in range(no_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 734:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('audio/explosion.wav')
            explosion_sound.play()
            bulletY = 495
            bullet_state = 'ready'
            score_value += 1
            
            with open('Score/highScore.txt','r') as highScore:
                Score = highScore.read()
            if score_value > int(Score):
                with open('Score/highScore.txt','w') as highScore:
                    highScore.write(f'{score_value}')

            enemyX[i] = random.randint(0,733)
            enemyY[i] = random.randint(20,180)

        enemy(enemyX[i],enemyY[i],i)

    if bulletY <= 0:
        bulletY = 495
        bullet_state = 'ready'

    if bullet_state == 'fire':
        bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    showScore(textX,textY)
    pygame.display.update()