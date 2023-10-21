
import pygame
import random
from levels import *
import time


pygame.init()



FPS = 60
pygame.display.set_caption("Ping-Pong")
wind = pygame.display.set_mode((1200, 720))

clock = pygame.time.Clock()



bk = pygame.image.load("Фон.png")
player_group = pygame.sprite.Group()
player_anim = "right"

music_back = pygame.mixer.Sound("background.ogg")
music_back.set_volume(0.3)
music_back.play(-1)



class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.transform.scale(image, (w, h))
    def draw(self):
        wind.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def __init__(self, x, y, w, h, speed, go_left,go_right,jumping, player_anim, images):
        super().__init__(x, y, w, h, images[0])
        player_group.add(self)
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.go_left = go_left
        self.go_right = go_right
        self.gravition = "down"
        self.jumping = jumping
        self.player_anim = player_anim
        self.images = []
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
                return
    def collide(self, block):                                                               
        if self.rect.colliderect(block.rect):
            return True
        else:
            return False
    def start_jump(self):
        if not self.jumping and self.can_jump:
            self.jumping = True
            self.jump_count = 35
    def graviti(self):
        x = self.rect.x
        y = self.rect.y
        
        # print(self.gravity)
        if not self.jumping:
            self.rect.y += self.speed

            for block in blocks:
                if self.collide(block):
                    self.rect.x = x
                    self.rect.y = y
                    self.can_jump = True
                    return
            self.can_jump = False
        else:
            self.rect.y -= self.speed
            self.jump_count -= 1
            if self.jump_count <= 0:
                self.jumping = False
            for block in blocks:
                if self.collide(block):
                    self.rect.x = x
                    self.rect.y = y
                    return
            




            
class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed, go_right, go_left):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.go_right = go_right
        self.go_left = go_left
        image = pygame.transform.scale(image, (w, h))
        self.image = image
        enemyies.append(self)
    def move(self):
        if self.go_right == True:
            self.rect.x -= self.speed
        if self.go_left == True:
            self.rect.x += self.speed


level = 1


player_img = pygame.image.load("player_l1.png")

player = Player(10, 50, 40, 40, 3, pygame.K_a , pygame.K_d, False, "right", [player_img,pygame.transform.flip(player_img, True, False)])
enemy1_img = pygame.image.load("enemy_img.png")

gold = pygame.image.load("chest.png")
kmn = pygame.image.load("дёрн.png")
invisible_block = pygame.image.load("invis_img.png")
blocks_gold = []
blocks = []
blocks_inviss = []
enemyies = []
block_size_y = 30
block_size_x = 30

x, y = 0, 0



if level == 1:
    for bl in map1:
        for l in bl:
            if l == "2":
                block_gold = GameSprite(x ,y , block_size_x, block_size_y, gold)
                blocks.append(block_gold)
            elif l == "1":
                block = GameSprite(x ,y , block_size_x, block_size_y, kmn)
                blocks.append(block)
            elif l == "3":
                block_invis = GameSprite(x ,y , block_size_x, block_size_y, invisible_block)
                blocks_inviss.append(block_invis)
            elif l == "4":
                ran = random.randint(0,1)
                enemy = Enemy(x, y, 40, 30, enemy1_img, 5 , ran, 1-ran)
            x += block_size_x
        y += block_size_y
        x = 0
if level == 2:
    for bl in map2:
        for l in bl:
            if l == "2":
                block_gold = GameSprite(x ,y , block_size_x, block_size_y, gold)
                blocks.append(block_gold)
            elif l == "1":
                block = GameSprite(x ,y , block_size_x, block_size_y, kmn)
                blocks.append(block)
            elif l == "3":
                block_invis = GameSprite(x ,y , block_size_x, block_size_y, invisible_block)
                blocks_inviss.append(block_invis)
            elif l == "4":
                ran = random.randint(0,1)
                enemy = Enemy(x, y, 40, 30, enemy1_img, 5 , ran, 1-ran)
            x += block_size_x
        y += block_size_y
        x = 0
game = True
finish = True


tamer = 0
road2 = 2


 
font = pygame.font.SysFont("Arial", 32)
block_group_gold = pygame.sprite.Group()
block_group_in = pygame.sprite.Group()
block_group = pygame.sprite.Group()
for block in blocks:
    block_group.add(block)
for block_invis in blocks_inviss:
    block_group_in.add(block_invis)
for block_gold in blocks_gold:
    block_group_gold.add(block_gold)
while game:

    print(level)
    wind.blit(bk, (0,0))
    if pygame.sprite.spritecollide(player, blocks_gold, False):
        print("hello")
    if player.player_anim == "right":
        player.image = player.images[0]
    if player.player_anim == "left":
        player.image = player.images[1]
    for block in blocks:
            block.draw()
            if player.collide(block):
                player.gravition = "none"
            else:
                player.gravition = "down"
    if player.rect.y >= 900:
        music_over = pygame.mixer.Sound("GameOver.ogg")
        music_over.set_volume(0.5)
        music_over.play()
        player.rect.y -= 100
        finish = True
        game_over = font.render('Game Over', True, (255,255,255))
        wind.blit(game_over, (600, 0))
    if not finish:
        for enemy in enemyies:
            if pygame.sprite.spritecollide(enemy, blocks_inviss, False):
                if enemy.go_right == True:
                    enemy.go_left = True
                    enemy.go_right = False
                else:
                    enemy.go_left = False
                    enemy.go_right = True
    
            if player.collide(enemy):
                player.rect.y = 900
                finish = True
            enemy.move()
            enemy.draw()
        player.move() 
        player.graviti()



    player.draw()
    block.draw()


    if player.rect.y <= 720:
        if finish == True:
            game_paused = font.render('Game Paused', True, (255,255,255))
            wind.blit(game_paused, (600, 0))
    if finish == True:
        game_over = font.render('Game Over', True, (255,255,255))
        wind.blit(game_over, (600, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if finish == True:
                if event.key == pygame.K_RETURN:
                    finish = False
                    player.jumping = False
                    enemy.go_left = True
                    enemy.go_right = False
                    player.rect.y = 50
                    player.rect.x = 10
                    enemy.rect.y = 200
                    enemy.rect.x = 450
            else:
                if event.key == pygame.K_SPACE:
                    if not player.jumping and player.can_jump:
                        level += 1
                        player.start_jump()


    

                
                
            

                    



    clock.tick(FPS)
    pygame.display.update()

