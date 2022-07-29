import pygame
from PIL import Image, ImageOps
import math

pygame.init()
window_width = 810
window_height = 480

win = pygame.display.set_mode( (window_width,window_height) )
pygame.display.set_caption("Sophie the Goblin Killer")


# Sprites and Background
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png'),pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png'),pygame.image.load('R9.png')]





#walkLeft = [im.crop((101,1,200,100)),
#           im.crop((201,1,300,100)),
#           im.crop((301,1,400,100)),
#           im.crop((1,101,100,200)),
#           im.crop((101,101,200,200)),
#           im.crop((201,101,300,200)),
#           im.crop((301,101,400,200)),
#           im.crop((1,201,100,300)),
#           im.crop((101,201,200,300)),
#           im.crop((201,201,300,300))]
#
#walkRight = [ImageOps.mirror(walkLeft[i]) for i in range(len(walkLeft))]

#or else flip right image



bg = pygame.image.load('bg.jpg')
#bg_width = bg.get_width()
#scroll = 0
#tiles = (window_width//bg_width)+2

char = pygame.image.load('standing.png')
clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound('bullet.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')
ouchSound = pygame.mixer.Sound('ouch.mp3')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.width = width
        self.height = height

		# character kinematics
        self.vel = 4
        self.x = x
        self.y = y - 10 #window_height-height-16
        self.left, self.right = False , True
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 9
        self.standing = True
        self.hitbox =  (self.x+30, self.y+22, 39, 55)

    def draw(self,win):
        if self.walkCount >= 30:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit( walkLeft[self.walkCount//3], (self.x,self.y) )
                self.walkCount += 1
            elif self.right:
                win.blit( walkRight[self.walkCount//3], (self.x,self.y) )
                self.walkCount += 1
        else:
            if self.right:
                win.blit( walkRight[0], (self.x,self.y) )
            else:
                win.blit( walkLeft[0], (self.x,self.y) )
            #win.blit( char, (self.x,self.y) )

        self.hitbox =  (self.x+30, self.y+22, 39, 55)

    def hit(self):
        self.x = 64
        self.y = window_height-64-16-10
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans',100)
        text = font1.render('-1',1,(0,255,0))
        win.blit(text,(window_width-text.get_width()/2,200))
        pygame.display.update()
        i = 0
        """
        while i<300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i =301
                    pygame.quit()
                    """

    	#pygame.draw.rect(win,(255,0,0),self.hitbox,2)

class projectile(object):
    sandal = pygame.image.load('sandal.png')
    def __init__(self,x,y,width,height,facing):
        self.x = x
        self.y =  y
        self.width =  width
        self.height =  height
        self.facing =  facing
        self.vel = 6 * facing
        self.hitbox =  (self.x+5, self.y, 15, 28)

    def draw(self,win):
        win.blit( self.sandal, (self.x,self.y) )
        self.hitbox =  (self.x+5 , self.y, 20, 30)
		#pygame.draw.circle(win, self.color , (self.x,self.y), self.radius)


		#pygame.draw.rect(win,(255,0,0),self.hitbox,2)

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y+5
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox =  (self.x + 17, self.y+2, 31, 57)
        self.health = 10
        self.visible = True


    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount>=33:
                self.walkCount =0

            if self.vel > 0 :
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox =  (self.x + 17, self.y+2, 31, 57)

			#pygame.draw.rect(win,(255,0,0),self.hitbox,2)
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win,(0,128,0),(self.hitbox[0],self.hitbox[1]-20,5*(10-self.health),10))

		#pass
    def move(self):
        if self.vel > 0 :
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.walkCount = 0
        else:
            if self.x > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.walkCount = 0

		#pass

    def hit(self):

    	if self.health > 0:
    		self.health -= 1
    	else:
    		self.visible = False

    	print('hit')
    	pass



def redrawGameWindow()  :
	#global walkCount
	#print(walkCount)
    text = font.render('Score:'+str(score),1,(0,0,0))
    win.blit( bg , ( 0,0) )
    win.blit(text, (0.8*window_width,0.05*window_height))
    goblin.draw(win)
    man.draw(win)

    #pygame.draw.rect(win,(0,255,0),(x,y,width,height))
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

"""
 main Loop

"""

#for i in range(0,tiles):
##    win.blit(bg, (i + bg_width + scroll,0))
#scroll =-5
#if scroll > bg_width:
#    scroll =0



font = pygame.font.SysFont('comicsans', 30 , True)
man = player(64,window_height-64-16,64,64)
goblin = enemy(window_width/2+64,window_height-64-16,64,64,window_width-2*64)
bullets = []
shootLoop = 0
#bullets = [projectile(x,y,radius,color,facing)]
run = True
touching_time = 0
while run:
    clock.tick(30) #fps rating
    #pygame.time.delay(50)

    if goblin.visible:
        if man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1] and man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                touching_time+=1
                if touching_time<=1:
                    ouchSound.play()
                    score -=1
    if touching_time > 5:
        touching_time = 0

    if shootLoop > 0 :
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    for bullet in bullets:

    	#if bullet.hitbox[1] + bullet.hitbox[3]/2 < goblin.hitbox[1] and bullet.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]

        if bullet.hitbox[1] + bullet.hitbox[3] > goblin.hitbox[1] and bullet.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3]:
            if bullet.hitbox[0] + bullet.hitbox[2] > goblin.hitbox[0] and bullet.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:

                if goblin.visible:
                    hitSound.play()
                    goblin.hit()
                    bullets.pop(bullets.index(bullet))
                    score +=1


        if bullet.x < window_width and bullet.x >0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 20 :
            bullets.append( projectile( round(man.x + man.width//2) , round(man.y + man.height//4), 32 , 32 , facing ))

    		#bullets.append( projectile( round(man.x + man.width//2) , round(man.y + man.width//2), 6 , (0,0,0) , facing ))
        shootLoop = 1



    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.vel
        man.left , man.right = True , False
        man.standing = False
    elif keys[pygame.K_RIGHT] and  man.x < window_width-man.width:
        man.x += man.vel
        man.left , man.right = False , True
        man.standing = False
    else:
        #man.left , man.right = False , False
        man.walkCount = 0
        man.standing = True

    if not(man.isJump): # while not jumping!!!
        #if keys[pygame.K_UP] and y > vel:
        #	y -= vel

        #if keys[pygame.K_DOWN] and y < window_height-height-vel:
        #	y += vel


        if keys[pygame.K_UP]:
            man.isJump = True
            #man.left , man.right = False , False
            man.walkCount = 0

    else: # while jumping
        #print (man.jumpCount)
        if man.jumpCount>=-9:

            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= man.jumpCount**2 * 0.5 * neg
            man.jumpCount -=1
        else:
            man.isJump = False
            man.jumpCount = 9

    redrawGameWindow()



pygame.quit()
