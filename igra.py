import pygame

pygame.init()

window = pygame.display.set_mode((800, 480))

pygame.display.set_caption('Fenix Game')

walkRight = [pygame.image.load('right_1.png'), pygame.image.load('right_2.png'), pygame.image.load('right_3.png'),
             pygame.image.load('right_4.png'), pygame.image.load('right_5.png'), pygame.image.load('right_6.png')]
walkLeft = [pygame.image.load('left_1.png'), pygame.image.load('left_2.png'), pygame.image.load('left_3.png'),
            pygame.image.load('left_4.png'), pygame.image.load('left_5.png'), pygame.image.load('left_6.png')]
bg = pygame.image.load('bgg.jpg')
score = 0
playerStand = pygame.image.load('idle.png')
clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound('bullet.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')
manSound = pygame.mixer.Sound('na-nas-napali.mp3')
scoreMusic = pygame.mixer.Sound('muzyika-s-proydennoy-missiey-iz-gta-san-andreas.mp3')
f = open('HiScore.txt', 'r+')
music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

class player(object):
    facing = -1
    def __init__(self, x, y, width, height):
        self.x = x
        self. y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.animCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y - 10, 40, 80)
        self.HiScore = int(f.read())

    def draw(self, window):
        if self.animCount + 1 >= 30:
            self.animCount = 0
        if not (self.standing):
            if self.left:
                window.blit(walkLeft[self.animCount // 5], (self.x, self.y))
                self.animCount += 1
            elif self.right:
                window.blit(walkRight[self.animCount // 5], (self.x, self.y))
                self.animCount += 1
        else:
            if self.right:
                window.blit(walkRight[0], (self.x, self.y))
            else:
                window.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x, self.y - 10, 40, 80)
        #pygame.draw.rect(window, (255,0,0), self.hitbox, 2)
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 500
        self.y = 350
        self.animCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        window.blit(text, (400 - (text.get_width()/2), 180))
        pygame.display.update()
        i=0
        while i < 200:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()




def drawWindow():
    window.blit(bg, (0, 0))
    text = font.render('Score :' + str(score), 1, (0,0,0))
    textg = font.render('HiScore :' + str(man.HiScore), 1, (0, 0, 0))
    window.blit(text, (700,10))
    window.blit(textg, (0, 10))
    man.draw(window)
    enemy.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    pygame.display.update()



class shoot(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)




class enemy(object):
    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
                 pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
                 pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
                pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y + 10, 28, 50)
        self.health = 10
        self.visible = True

    def draw(self,window):
        self.move()

        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.visible:
            if self.vel > 0:
                window.blit(self.walkRight[(self.walkCount // 3)], (self.x, self.y))
            else:
                window.blit(self.walkLeft[(self.walkCount // 3)], (self.x, self.y))
            self.walkCount += 1
            self.hitbox = (self.x + 20, self.y+10, 28, 50)
            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - 5 * (10 - self.health), 10))
            #pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        elif self.vel < 0:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel *-1
                self.walkCount = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
    def kill(self):
        self.x = 50
        self.y = 350
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('+5', 1, (0, 128, 0))
        window.blit(text, (400 - (text.get_width() / 2), 180))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()




font = pygame.font.SysFont('comicsans', 30)
man = player(500, 350, 60, 71)
xxx = man.HiScore
enemy = enemy(0,350, 64, 64, 750)


shootLoop = 0
done = True
bullets=[]
while done:
    clock.tick(30)
    if score > xxx:
        f.close
        f = open('HiScore.txt', 'w+')
        f.write(str(score))
    if  score == xxx or score == xxx+1 or score == xxx+2 or score == xxx+3 or score == xxx+4:
        music = pygame.mixer.music.load('muzyika-s-proydennoy-missiey-iz-gta-san-andreas.mp3')
        pygame.mixer.music.play(-1)



    if enemy.visible == True:
        if man.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and man.hitbox[1] + man.hitbox[3] > enemy.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > enemy.hitbox[0] and man.hitbox[0]< enemy.hitbox[0] + enemy.hitbox[2]:
                manSound.play()
                man.hit()
                enemy.x = 0
                score -= 5
                enemy.vel -= 1
    else:
        enemy.kill()
        enemy.health = 10
        enemy.visible = True
        enemy.vel += 1
        score += 5



    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False

    for bullet in bullets:
        if bullet.y - bullet.radius < enemy.hitbox[1]+enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                hitSound.play()
                enemy.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

    for bullet in bullets:
        if bullet.x < 800 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f] and shootLoop == 0:
        bulletSound.play()
        if  man.right == True:
            man.facing = 1
        elif man.left == True:
            man.facing = -1
        if len(bullets) < 5:
            bullets.append(shoot(round(man.x + man.width//2), round(man.y + man.height//2), 5, (139,0,255), man.facing ))
        shootLoop = 1


    if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
        if man.x < 800 - man.width - 5:
            man.x += man.speed
            man.left = False
            man.right = True
            man.standing = False
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if man.x > 5:
            man.x -= man.speed
            man.left = True
            man.right = False
            man.standing = False
    else:
        man.standing = True
        man.animCount = 0
    if not(man.isJump):
        if keys[pygame.K_SPACE]:
            man.isJump = True
    else:
        if man.jumpCount >=-10:
            if man.jumpCount < 0:
                man.y += (man.jumpCount ** 2) / 2
            else:
                man.y -= (man.jumpCount ** 2) / 2
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    drawWindow()









pygame.quit()
