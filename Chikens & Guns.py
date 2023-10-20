
import pygame
import random
from levels import *
import time


pygame.init()



FPS = 60
pygame.display.set_caption("Ping-Pong")
wind = pygame.display.set_mode((1500, 800))

clock = pygame.time.Clock()



bk = pygame.image.load("Фон.png")
player_group = pygame.sprite.Group()
player_anim = "right"



left_score = 0
right_score = 0



class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.transform.scale(image, (w, h))
    def draw(self):
        wind.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def __init__(self, x, y, w, h, speed, go_left,go_right, gravition, jumping, player_anim, images, jump_count, can_jump):
        super().__init__(x, y, w, h, images[0])
        player_group.add(self)
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.go_left = go_left
        self.go_right = go_right
        self.gravition = gravition
        self.jumping = jumping
        self.player_anim = player_anim
        self.images = []
        self.jumping = False
        self.jump_count = 0
        self.can_jump = False
        for i in images:
            i = pygame.transform.scale(i, (w, h))
            self.images.append(i)
        self.image = self.images[0]
    def move(self):
        x = self.rect.x
        y = self.rect.y

        k = pygame.key.get_pressed()
        if k[self.go_left]:
            self.rect.x -= self.speed
            self.player_anim = "left"
        if k[self.go_right]:
            self.rect.x += self.speed
            self.player_anim = "right"
        for block in blocks:
            if self.collide(block):
                self.rect.x = x
                self.rect.y = y
                self.gravition = False
                return
    def collide(self, block):                                                               
        if self.rect.colliderect(block.rect):
            return True
        else:
            return False
    def jump(self):
        if not self.jumping and self.can_jump:
            self.jumping = True
            self.jump_count = 35
            if self.jump_count <= 0:
                self.jumping = False
                if self.jump_count == 0:
                    self.jumping = False
    def graviti(self):
        x = self.rect.x
        y = self.rect.y
        for block in blocks:
            if player.collide(block):
                player.gravition = False
                player.jumping = False
                break
            else:
                player.gravition = True
        print(self.gravition)
        if not self.jumping:
            if self.gravition == True:
                self.rect.y += self.speed
        else:
            self.rect.y -= 1
            self.jump_count -= 35
        for block in blocks:
            if self.collide(block):
                self.rect.x = x
                self.rect.y = y
                return
    #def jumping(self):
        #k = pygame.key.get_pressed()
        #if self.jump >= 1:
            #self.rect.y -= 5
            #self.gravition = False
            #self.jump -= 1
        #else:
            #if k[pygame.K_SPACE]:

class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed, go_right, go_left):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.go_right = go_right
        self.go_left = go_left
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    def move(self):
        if self.go_right == True:
            self.rect.x -= self.speed
        if self.go_left == True:
            self.rect.x += self.speed


player_img = pygame.image.load("player_l1.png")

player = Player(10, 50, 40, 40, 3, pygame.K_a , pygame.K_d, True, False, "right", [player_img,pygame.transform.flip(player_img, True, False)], 1, False)
enemy1_img = pygame.image.load("enemy_img.png")
enemy1 = Enemy(450, 200, 40, 40, enemy1_img, 5 , False, True)

gold = pygame.image.load("дёрн.png")
kmn = pygame.image.load("дёрн.png")
invisible_block = pygame.image.load("invis_img.png")
blocks = []
blocks_inviss = []
block_size_y = 30
block_size_x = 30

x, y = 0, 0





for bl in map1:
    for l in bl:
        if l == "2":
            block_gold = GameSprite(x ,y , block_size_x, block_size_y, gold)
            blocks.append(block_gold)
        if l == "1":
            block = GameSprite(x ,y , block_size_x, block_size_y, kmn)
            blocks.append(block)
        if l == "3":
            block_invis = GameSprite(x ,y , block_size_x, block_size_y, invisible_block)
            blocks_inviss.append(block_invis)
        x += block_size_x
    y += block_size_y
    x = 0

game = True
finish = True


tamer = 0
road2 = 2


 
font = pygame.font.SysFont("Arial", 32)
block_group_in = pygame.sprite.Group()
block_group = pygame.sprite.Group()
for block in blocks:
    block_group.add(block)
for block_invis in blocks_inviss:
    block_group_in.add(block_invis)


while game:


    wind.blit(bk, (0,0))
    if pygame.sprite.spritecollide(enemy1, blocks_inviss, False):
        if enemy1.go_right == True:
            enemy1.go_left = True
            enemy1.go_right = False
        else:
            enemy1.go_left = False
            enemy1.go_right = True
    if player.player_anim == "right":
        player.image = player.images[0]
    if player.player_anim == "left":
        player.image = player.images[1]
    for block in blocks:
            block.draw()
            if player.collide(block):
                player.gravition = False
            else:
                player.gravition = True
    if player.rect.y >= 900:
        finish = True
    if not finish:
        enemy1.move()
        player.move()
        player.graviti()

    enemy1.draw()
    player.draw()
    block.draw()
    if finish == True:
        game_over = font.render('Game Over', True, (255,255,255))
        wind.blit(game_over, (600, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                finish = False
                enemy1.go_left = True
                enemy1.go_right = False
            if event.key == pygame.K_1:
                finish = True
                enemy1.go_left = True
                enemy1.go_right = False
            if event.key == pygame.K_SPACE:
                if not player.jumping:
                    player.jumping = True

    

                
                
            

                    



    clock.tick(FPS)
    pygame.display.update()

