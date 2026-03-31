import pygame
import asyncio
import random

pygame.init()
WIDTH, HEIGHT = 480, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
GREEN = (0,180,0)
GRAY = (100,100,100)
YELLOW = (255,255,0)
PURPLE = (180,0,255)

font_small = pygame.font.SysFont(None,28)

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

best_scores = [0]*10

class Button:
    def __init__(self, rect, color, text):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        t = font_small.render(self.text, True, WHITE)
        screen.blit(t, t.get_rect(center=self.rect.center))

# ---- ミニゲーム（例: Dodge Game） ----
async def dodge_game():
    player = pygame.Rect(WIDTH//2-25, HEIGHT-100,50,50)
    bullets = []
    score = 0
    timer = 0
    running = True
    left_btn = pygame.Rect(30, HEIGHT-160, 80,80)
    right_btn = pygame.Rect(130, HEIGHT-160, 80,80)
    active_touches = {}
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        timer += 1
        if timer%30==0:
            bullets.append(pygame.Rect(random.randint(0,WIDTH-10), -10,10,10))
        for e in pygame.event.get():
            if e.type==pygame.QUIT: return 0
            if e.type in (pygame.FINGERDOWN, pygame.FINGERMOTION):
                active_touches[e.finger_id]=(e.x,e.y)
            if e.type==pygame.FINGERUP:
                active_touches.pop(e.finger_id,None)
            if e.type==pygame.MOUSEBUTTONDOWN:
                x,y=e.pos
                if left_btn.collidepoint((x,y)): player.x-=5
                if right_btn.collidepoint((x,y)): player.x+=5
        for tx,ty in active_touches.values():
            x,y=tx*WIDTH,ty*HEIGHT
            if left_btn.collidepoint((x,y)): player.x-=5
            if right_btn.collidepoint((x,y)): player.x+=5
        player.x = max(0,min(WIDTH-player.width,player.x))
        for b in bullets[:]:
            b.y += 7
            if player.colliderect(b):
                running=False
            if b.y>HEIGHT:
                bullets.remove(b)
                score+=10
        pygame.draw.rect(screen, BLUE, player)
        for b in bullets: pygame.draw.rect(screen, RED, b)
        pygame.draw.rect(screen, GREEN, left_btn)
        pygame.draw.rect(screen, GREEN, right_btn)
        screen.blit(font_small.render("L",True,WHITE), font_small.render("L",True,WHITE).get_rect(center=left_btn.center))
        screen.blit(font_small.render("R",True,WHITE), font_small.render("R",True,WHITE).get_rect(center=right_btn.center))
        screen.blit(font_small.render(f"SCORE: {score}",True,YELLOW),(10,10))
        pygame.display.flip()
        await asyncio.sleep(0)
    return score

# ---- ノーマルゲーム ----
async def normal_game(cp_level, max_player_hp):
    player = pygame.Rect(WIDTH//2-25, HEIGHT-260,50,50)
    enemy = pygame.Rect(WIDTH//2-25,50,50,50)
    player_bullets=[]
    enemy_bullets=[]
    player_hp = max_player_hp
    enemy_hp = 3+cp_level*2
    max_enemy_hp = enemy_hp
    shoot_btn = pygame.Rect(WIDTH-110, HEIGHT-160, 80, 80)
    left_btn = pygame.Rect(30, HEIGHT-160, 80, 80)
    right_btn = pygame.Rect(130, HEIGHT-160, 80, 80)
    shoot_cooldown=0
    cooldown_time=30
    active_touches={}
    combo=0
    combo_timer=0
    running=True
    start_time = pygame.time.get_ticks()
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        moving_left = moving_right = shooting = False
        for e in pygame.event.get():
            if e.type==pygame.QUIT: return 0
            if e.type in (pygame.FINGERDOWN, pygame.FINGERMOTION):
                active_touches[e.finger_id]=(e.x,e.y)
            if e.type==pygame.FINGERUP:
                active_touches.pop(e.finger_id,None)
            if e.type==pygame.MOUSEBUTTONDOWN:
                x,y=e.pos
                if left_btn.collidepoint((x,y)): moving_left=True
                if right_btn.collidepoint((x,y)): moving_right=True
                if shoot_btn.collidepoint((x,y)): shooting=True
        for tx,ty in active_touches.values():
            x,y=tx*WIDTH,ty*HEIGHT
            if left_btn.collidepoint((x,y)): moving_left=True
            if right_btn.collidepoint((x,y)): moving_right=True
            if shoot_btn.collidepoint((x,y)): shooting=True
        if moving_left: player.x-=5
        if moving_right: player.x+=5
        player.x = max(0,min(WIDTH-player.width,player.x))
        if shoot_cooldown>0: shoot_cooldown-=1
        if shooting and shoot_cooldown==0:
            player_bullets.append(pygame.Rect(player.centerx-5,player.y,10,10))
            shoot_cooldown=cooldown_time
        # 敵弾
        if random.randint(0,cp_levels[cp_level]["shoot_rate"])==0:
            enemy_bullets.append(pygame.Rect(enemy.centerx-5,enemy.bottom,10,10))
        # 弾移動
        for b in player_bullets: b.y-=7
        for b in enemy_bullets: b.y+=7
        # 衝突
        for pb in player_bullets[:]:
            if enemy.colliderect(pb):
                enemy_hp-=1
                player_bullets.remove(pb)
                combo+=1
                combo_timer=300
        for eb in enemy_bullets[:]:
            if player.colliderect(eb):
                player_hp-=1
                enemy_bullets.remove(eb)
                combo=0
        combo_timer = max(0, combo_timer-1)
        if player_hp<=0 or enemy_hp<=0:
            running=False
        # 描画
        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, RED, enemy)
        for b in player_bullets: pygame.draw.rect(screen, WHITE, b)
        for b in enemy_bullets: pygame.draw.rect(screen, YELLOW, b)
        pygame.draw.rect(screen, GREEN, left_btn)
        pygame.draw.rect(screen, GREEN, right_btn)
        pygame.draw.rect(screen, RED, shoot_btn)
        screen.blit(font_small.render("L",True,WHITE), font_small.render("L",True,WHITE).get_rect(center=left_btn.center))
        screen.blit(font_small.render("R",True,WHITE), font_small.render("R",True,WHITE).get_rect(center=right_btn.center))
        screen.blit(font_small.render("SHOOT",True,WHITE), font_small.render("SHOOT",True,WHITE).get_rect(center=shoot_btn.center))
        pygame.display.flip()
        await asyncio.sleep(0)
    end_time = pygame.time.get_ticks()
    return 100  # サンプルスコア

# ---- メインループ ----
async def main():
    global best_scores
    while True:
        # スタート画面
        screen.fill(BLACK)
        t=font_small.render("Tap to Start",True,WHITE)
        screen.blit(t,t.get_rect(center=(WIDTH//2,HEIGHT//2)))
        pygame.display.flip()
        start=False
        active_touches={}
        while not start:
            for e in pygame.event.get():
                if e.type==pygame.QUIT: return
                if e.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
                    start=True
                    active_touches.clear()
            await asyncio.sleep(0)

        # 難易度選択
        buttons=[
            Button((60,200,120,50),GREEN,"Easy"),
            Button((200,200,120,50),BLUE,"Normal"),
            Button((60,270,120,50),GRAY,"Hard"),
            Button((200,270,120,50),RED,"Ultra"),
        ]
        selecting=True
        max_player_hp=10
        while selecting:
            screen.fill(BLACK)
            screen.blit(font_small.render("Select Difficulty",True,WHITE),(120,100))
            for b in buttons: b.draw(screen)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type==pygame.QUIT: return
                if e.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
                    pos = (e.x*WIDTH,e.y*HEIGHT) if e.type==pygame.FINGERDOWN else e.pos
                    for b in buttons:
                        if b.rect.collidepoint(pos):
                            if b.text=="Easy": max_player_hp=20
                            elif b.text=="Normal": max_player_hp=10
                            elif b.text=="Hard": max_player_hp=5
                            elif b.text=="Ultra": max_player_hp=1
                            selecting=False
            await asyncio.sleep(0)

        # CPレベル選択＋ミニゲームボタン
        level_buttons=[Button((20+i*45,350,40,40),(0,255-20*i,255),str(i+1)) for i in range(10)]
        mini_game_btn = Button((WIDTH//2-60, 450, 120, 50), PURPLE, "MINI GAME")
        selecting=True
        cp_level=0
        while selecting:
            screen.fill(BLACK)
            screen.blit(font_small.render("Select CP Level",True,WHITE),(130,100))
            for b in level_buttons: b.draw(screen)
            mini_game_btn.draw(screen)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type==pygame.QUIT: return
                if e.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
                    pos = (e.x*WIDTH,e.y*HEIGHT) if e.type==pygame.FINGERDOWN else e.pos
                    # レベル選択
                    for i,b in enumerate(level_buttons):
                        if b.rect.collidepoint(pos):
                            cp_level=i
                            selecting=False
                    # ミニゲーム
                    if mini_game_btn.rect.collidepoint(pos):
                        await dodge_game()
            await asyncio.sleep(0)

        # ノーマルゲーム開始
        score = await normal_game(cp_level,max_player_hp)

asyncio.run(main())