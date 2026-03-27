import pygame
import asyncio
import random

pygame.init()

# ===== 画面 =====
WIDTH, HEIGHT = 480, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
GREEN = (0,180,0)
ORANGE = (255,165,0)
GRAY = (100,100,100)

font = pygame.font.SysFont(None,60)
font_small = pygame.font.SysFont(None,28)

# ===== CPレベル =====
cp_levels = [
    {"shoot_rate":80,"speed":2},
    {"shoot_rate":60,"speed":3},
    {"shoot_rate":50,"speed":4},
    {"shoot_rate":40,"speed":5},
    {"shoot_rate":30,"speed":6},
    {"shoot_rate":20,"speed":7},
    {"shoot_rate":15,"speed":8},
    {"shoot_rate":10,"speed":9},
    {"shoot_rate":6,"speed":10},
    {"shoot_rate":3,"speed":12},
]

class Button:
    def __init__(self, rect, color, text):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surf = font_small.render(self.text, True, WHITE)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))
    def is_clicked(self,pos):
        return self.rect.collidepoint(pos)

def check_touch_buttons(touches, buttons):
    pressed = {"left": False, "right": False, "shoot": False}
    for t in touches:
        x, y = t[0]*WIDTH, t[1]*HEIGHT
        if buttons["left"].collidepoint((x,y)): pressed["left"] = True
        if buttons["right"].collidepoint((x,y)): pressed["right"] = True
        if buttons["shoot"].collidepoint((x,y)): pressed["shoot"] = True
    return pressed

async def main():

    # ===== 難易度選択 =====
    difficulty_buttons = [
        Button((60,200,120,50),GREEN,"Easy"),
        Button((200,200,120,50),BLUE,"Normal"),
        Button((60,270,120,50),ORANGE,"Hard"),
        Button((200,270,120,50),RED,"Ultra"),
    ]

    selecting=True
    max_player_hp=10

    while selecting:
        screen.fill(BLACK)
        screen.blit(font_small.render("Select Difficulty",True,WHITE),(120,100))
        for btn in difficulty_buttons: btn.draw(screen)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                return
            if e.type==pygame.MOUSEBUTTONDOWN:
                for btn in difficulty_buttons:
                    if btn.is_clicked(pygame.mouse.get_pos()):
                        if btn.text=="Easy": max_player_hp=20
                        elif btn.text=="Normal": max_player_hp=10
                        elif btn.text=="Hard": max_player_hp=5
                        elif btn.text=="Ultra": max_player_hp=1
                        selecting=False

        await asyncio.sleep(0)

    player_hp = max_player_hp

    # ===== レベル選択 =====
    level_buttons=[]
    for i in range(10):
        level_buttons.append(Button((20+i*45,350,40,40),(0,255-20*i,255),str(i+1)))

    selecting=True
    cp_level=0

    while selecting:
        screen.fill(BLACK)
        screen.blit(font_small.render("Select CP Level",True,WHITE),(130,100))
        for btn in level_buttons: btn.draw(screen)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                return
            if e.type==pygame.MOUSEBUTTONDOWN:
                for i,btn in enumerate(level_buttons):
                    if btn.is_clicked(pygame.mouse.get_pos()):
                        cp_level=i
                        selecting=False

        await asyncio.sleep(0)

    # ===== 初期化 =====
    player=pygame.Rect(WIDTH//2-25, HEIGHT-150,50,50)
    enemy=pygame.Rect(WIDTH//2-25,50,50,50)
    player_bullets=[]
    enemy_bullets=[]
    enemy_hp=3+cp_level*2
    max_enemy_hp=enemy_hp

    left_btn = pygame.Rect(30, HEIGHT-120, 80, 80)
    right_btn = pygame.Rect(130, HEIGHT-120, 80, 80)
    shoot_btn = pygame.Rect(WIDTH-110, HEIGHT-120, 80, 80)
    buttons = {"left": left_btn, "right": right_btn, "shoot": shoot_btn}

    # ===== クールタイム =====
    shoot_cooldown = 0
    cooldown_chance = 0.1
    cooldown_time = 60

    running=True

    while running:
        clock.tick(60)
        screen.fill(BLACK)

        moving_left = moving_right = shooting = False
        touches = []

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                running=False

            if e.type==pygame.FINGERDOWN:
                touches.append((e.x,e.y))

        # 長押し対応
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            mx, my = pygame.mouse.get_pos()
            if left_btn.collidepoint((mx,my)): moving_left = True
            if right_btn.collidepoint((mx,my)): moving_right = True
            if shoot_btn.collidepoint((mx,my)): shooting = True

        touch_pressed = check_touch_buttons(touches, buttons)
        moving_left |= touch_pressed["left"]
        moving_right |= touch_pressed["right"]
        shooting |= touch_pressed["shoot"]

        # クールタイム
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        # プレイヤー
        if moving_left: player.x -= 5
        if moving_right: player.x += 5

        if shooting and len(player_bullets) < 5 and shoot_cooldown == 0:
            player_bullets.append(pygame.Rect(player.centerx-5, player.y,10,10))
            if random.random() < cooldown_chance:
                shoot_cooldown = cooldown_time

        player.x = max(0,min(WIDTH-player.width,player.x))

        # 敵
        dx = player.centerx - enemy.centerx
        direction = dx / abs(dx) if dx != 0 else 0
        enemy.x += direction * cp_levels[cp_level]["speed"]
        enemy.x = max(0, min(WIDTH-enemy.width, enemy.x))

        if random.randint(0, cp_levels[cp_level]["shoot_rate"])==0:
            enemy_bullets.append(pygame.Rect(enemy.centerx-5, enemy.bottom, 10,10))

        # 弾移動
        for b in player_bullets: b.y -= 7
        for b in enemy_bullets: b.y += 7

        # 衝突
        for pb in player_bullets[:]:
            for eb in enemy_bullets[:]:
                if pb.colliderect(eb):
                    player_bullets.remove(pb)
                    enemy_bullets.remove(eb)
                    break

        for b in enemy_bullets[:]:
            if player.colliderect(b):
                enemy_bullets.remove(b)
                player_hp -= 1

        for b in player_bullets[:]:
            if enemy.colliderect(b):
                player_bullets.remove(b)
                enemy_hp -= 1

        # ===== 勝敗（ここが追加） =====
        if player_hp <= 0 or enemy_hp <= 0:
            screen.fill(BLACK)

            if player_hp <= 0:
                text = font.render("LOSE", True, RED)
            else:
                text = font.render("WIN", True, BLUE)

            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
            pygame.display.flip()

            await asyncio.sleep(2)
            running = False
            continue

        # 描画
        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, RED, enemy)

        for b in player_bullets:
            pygame.draw.rect(screen, WHITE, b)
        for b in enemy_bullets:
            pygame.draw.rect(screen, WHITE, b)

        x = (WIDTH-200)//2
        pygame.draw.rect(screen, WHITE, (x,20,200,20),2)
        pygame.draw.rect(screen, RED, (x,20,200*(enemy_hp/max_enemy_hp),20))
        pygame.draw.rect(screen, WHITE, (x,HEIGHT-60,200,20),2)
        pygame.draw.rect(screen, BLUE, (x,HEIGHT-60,200*(player_hp/max_player_hp),20))

        pygame.draw.rect(screen, GREEN, left_btn)
        pygame.draw.rect(screen, GREEN, right_btn)

        if shoot_cooldown > 0:
            pygame.draw.rect(screen, GRAY, shoot_btn)
        else:
            pygame.draw.rect(screen, RED, shoot_btn)

        screen.blit(font_small.render("L",True,WHITE),(left_btn.x+30,left_btn.y+25))
        screen.blit(font_small.render("R",True,WHITE),(right_btn.x+30,right_btn.y+25))
        screen.blit(font_small.render("SHOOT",True,WHITE),(shoot_btn.x+5,shoot_btn.y+25))

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())