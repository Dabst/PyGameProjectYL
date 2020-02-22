import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 500
HEIGHT = 600
FPS = 60
turn_off = 5000
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(pygame.Color('BLACK'))
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = 250
        self.rect.bottom = 590
        self.speedx = 0
        self.speedy = 0
        self.speed_2 = 0
        self.shield = 100
        self.zd = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > turn_off:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = 250
            self.rect.bottom = 590

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.speed_2 = -8
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.speed_2 = 8
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.speed_2 = -8
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.speed_2 = 8
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speed_2
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        i = pygame.time.get_ticks()
        if i - self.last_shot > self.zd:
            self.last_shot = i
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bul.add(bullet)
            if self.power >= 2:
                b1 = Bullet(self.rect.left, self.rect.centery)
                b2 = Bullet(self.rect.right, self.rect.centery)
                b3 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(b1)
                all_sprites.add(b2)
                all_sprites.add(b3)
                bul.add(b1)
                bul.add(b2)
                bul.add(b3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(pygame.Color('BLACK'))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(pygame.Color('BLACK '))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = bax[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self):
        i = pygame.time.get_ticks()
        if i - self.last_update > self.frame_rate:
            self.last_update = i
            self.frame += 1
            if self.frame == len(bax[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = bax[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(pygame.Color('BLACK'))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


def keys(a, b, c, x, y):
    text_1 = pygame.font.Font(pygame.font.match_font('verdana'), c)
    text_2 = text_1.render(b, True, pygame.Color('green'))
    text_3 = text_2.get_rect()
    text_3.midtop = (x, y)
    a.blit(text_2, text_3)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(z, x, y, alfa):
    if alfa < 0:
        alfa = 0
    length_1 = 100
    height_1 = 10
    fill = (alfa / 100) * length_1
    outline_rect = pygame.Rect(x, y, length_1, height_1)
    fill_rect = pygame.Rect(x, y, fill, height_1)
    pygame.draw.rect(z, pygame.Color('GREEN'), fill_rect)
    pygame.draw.rect(z, pygame.Color('WHITE'), outline_rect, 2)


def draw_lives(z, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        z.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    keys(screen, "STAR WARS 1970!", 50, 250, 125)
    keys(screen, "ВЫ ПОПАЛИ В КОСМОС", 18, 250, 300)
    keys(screen, "Передвижение на стрелочки, выстрел на пробел", 18, 250, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


background = pygame.image.load(path.join(img_dir, "fon.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "korabl.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(pygame.Color('BLACK'))
bullet_img = pygame.image.load(path.join(img_dir, "pulya3.png")).convert()
meteor_images = []
meteor_list = ['1.png', '2.png','3.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

bax = {}
bax['lg'] = []
bax['sm'] = []
bax['player'] = []
for i in range(9):
    filename = 'vsriv.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(pygame.Color('BLACK'))
    img_lg = pygame.transform.scale(img, (75, 75))
    bax['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    bax['sm'].append(img_sm)
    filename = 'vsriv2.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(pygame.Color('BLACK'))
    bax['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'molnia.png')).convert()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bul = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()
score = 0

game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bul = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bul, True, True)
    for hit in hits:
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death = Explosion(player.rect.center, 'player')
            all_sprites.add(death)
            player.lives -= 1
            player.shield = 100

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    if player.lives == 0 and not death.alive():
        game_over = True

    screen.fill(pygame.Color('BLACK'))
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    keys(screen, str(score), 18, 250, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, 400, 5, player.lives,
               player_mini_img)
    pygame.display.flip()

pygame.quit()
