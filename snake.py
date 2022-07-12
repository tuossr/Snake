import pygame
import random
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player1_head_img = pygame.image.load(os.path.join(img_folder, 'p1_head.png'))
player1_tail_img = pygame.image.load(os.path.join(img_folder, 'p1_tail.png'))
player2_head_img = pygame.image.load(os.path.join(img_folder, 'p2_head.png'))
player2_tail_img = pygame.image.load(os.path.join(img_folder, 'p2_tail.png'))
food_image = pygame.image.load(os.path.join(img_folder, 'cherry.png'))

width, height = 550, 350
frame_rate = 3
cell_size = 50
countdown = 20
white = (255,255,255)
blue = (54,217,240)
red = (255,60,90)
food_counter = 0
food_list = []
win1, win2 = 1, 1
x1, x2, y1, y2 = 0, 0, 0, 0
x1 = random.randint(0,10) * cell_size
y1 = random.randint(0,6) * cell_size
if x1 > 5 * cell_size: x2 = x1 - 5 * cell_size 
else: x2 = x1 + 5 * cell_size
if y1 > 3 * cell_size: y2 = y1 - 3 * cell_size 
else: y2 = y1 + 3 * cell_size


class Player(pygame.sprite.Sprite):
    def __init__(self, head_img, tail_img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = head_img
        self.image.set_colorkey(white)
        self.tail_img = tail_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.body = [self.rect]
        self.direction = "Right"
        self.counter = countdown
        self.win = 1
        
    def update(self):
        self.counter -= 1
        if self.counter == 0:
            self.counter = countdown
            del(self.body[-1])
        if len(self.body) > 1:
            tail = self.body.pop(-1)
            tail.x = self.rect.x
            tail.y = self.rect.y
            self.body[1:1] = [tail]
        if self.direction == "Right": self.rect.x += cell_size
        elif self.direction == "Left": self.rect.x -= cell_size
        elif self.direction == "Up": self.rect.y -= cell_size
        elif self.direction == "Down": self.rect.y += cell_size
        if self.rect.x == width: self.rect.x = 0
        elif self.rect.x < 0: self.rect.x = width - cell_size
        elif self.rect.y == height: self.rect.y = 0
        elif self.rect.y < 0: self.rect.y = height - cell_size

    def grow(self):
        x_old, y_old = self.body[0].x, self.body[0].y
        self.body[:0] = [self.body[0]]
        tail = Tail(self.tail_img, x_old, y_old)
        all_sprites.add(tail)
        self.body[1] = tail.rect


class Tail(pygame.sprite.Sprite):
    def __init__(self, tail_img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = tail_img
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


class Food(pygame.sprite.Sprite):
    def __init__(self, coord):
        pygame.sprite.Sprite.__init__(self)
        self.image = food_image
        self.image.set_colorkey(white)
        self.rect = pygame.Rect(coord[0], coord[1], cell_size, cell_size)

    def update(self):
        pass

def make_food(player1, player2, food_list):
    def gen_coord():
        x, y = 0, 0
        collision = True
        while collision:
            x = random.randint(0,10) * cell_size
            y = random.randint(0,6) * cell_size
            if (all([not r.collidepoint(x, y) for r in player1])
                and all([not r.collidepoint(x, y) for r in player2])
                and all([not i.rect.collidepoint(x, y) for i in food_list])):
                collision = False
        return [x, y]
    if  len(food_list) == 0:
        food_list.append(Food(gen_coord()))
        all_sprites.add(food_list[0])
    elif len(food_list) == 1:
        if random.randint(1,5) == 1:
            food_list.append(Food(gen_coord()))
            all_sprites.add(food_list[1])

def head_colission(player1, player2):
    global run_game
    if (player1.body[0].collidelist(player2.body) >= 0 or
        len(player1.body) > 1 and player1.body[0].collidelist(player1.body[1:]) >= 0):
        player1.win = 0
        run_game = False

def food_collision(player, food_list):
    for i, food in enumerate(food_list):
        if player.rect.colliderect(food.rect):
            food_list[i].remove(all_sprites)
            del(food_list[i])
            player.grow()


pygame.init()
font = pygame.font.SysFont(pygame.font.get_fonts()[0], 70)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Hungry snakes")
screen.fill(blue)
all_sprites = pygame.sprite.Group()
player1 = Player(player1_head_img, player1_tail_img, x1, y1)
player2 = Player(player2_head_img, player2_tail_img, x2, y2)
make_food(player1.body, player2.body, food_list)
all_sprites.add(player1)
all_sprites.add(player2)
run_game = True

while run_game:
    clock.tick(frame_rate)
    food_collision(player1, food_list)
    food_collision(player2, food_list)   
    make_food(player1.body, player2.body, food_list)
    all_sprites.remove(player1)
    all_sprites.add(player1)
    all_sprites.remove(player2)
    all_sprites.add(player2)
    all_sprites.update()
    if len(player1.body) == 0:
        player1.win = 0
        run_game = False
    if len(player2.body) == 0:
        player2.win = 0
        run_game = False
    if not run_game: continue  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                if player1.direction == "Right": None
                else: player1.direction = "Left"
            elif event.key == pygame.K_RIGHT: 
                if player1.direction == "Left": None
                else: player1.direction = "Right"
            elif event.key == pygame.K_UP: 
                if player1.direction == "Down": None
                else: player1.direction = "Up"
            elif event.key == pygame.K_DOWN: 
                if player1.direction == "Up": None
                else: player1.direction = "Down"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: 
                if player2.direction == "Right": None
                else: player2.direction = "Left"
            elif event.key == pygame.K_d: 
                if player2.direction == "Left": None
                else: player2.direction = "Right"
            elif event.key == pygame.K_w: 
                if player2.direction == "Down": None
                else: player2.direction = "Up"
            elif event.key == pygame.K_s: 
                if player2.direction == "Up": None
                else: player2.direction = "Down"        
    screen.fill(blue)
    all_sprites.draw(screen)
    pygame.display.flip()
    head_colission(player1, player2)
    head_colission(player2, player1)

if player1.win: text = "Player one win!"
elif player2.win: text = "Player two win!"
else: text = "Draw..." 
text_x = font.render(text, True, red)
_, _, w, h = text_x.get_clip()
run_score = True
while run_score:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_score = False       
    screen.fill(blue)
    screen.blit(text_x, (width/2 - w/2, height/2 - h/2))
    pygame.display.flip()

pygame.quit()