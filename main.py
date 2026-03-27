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

font = pygame.font.SysFont(None,60)
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

async def main():

    player=pygame.Rect(WIDTH//2-25, HEIGHT-150,50,50)
    enemy=pygame.Rect(WIDTH//2-25,50,50,50)

    player_bullets=[]
    enemy_bullets=[]

    player_hp=10
    enemy_hp=10
    max_enemy_hp=10
    max_player_hp=10

    cp_level=3

    left_btn = pygame.Rect(30, HEIGHT-120, 80, 80)
    right_btn = pygame.Rect(130, HEIGHT-120, 80, 80)
    shoot_btn = pygame.Rect(WIDTH-110, HEIGHT-120, 80, 80)

    # クールタイム（0.5秒）
    shoot_cooldown = 0
    cooldown_chance = 0.1
    cooldown_time = 30

    # ★タッチ管理（重要）
    active_touches = {}

    running=True
    while running:
        clock.tick(60)
        screen.fill(BLACK)

        moving_left = moving_right = shooting = False

        # ===== イベント =====
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                running=False

            if e.type == pygame.FINGERDOWN:
                active_touches[e.finger_id] = (e.x, e.y)
            if e.type == pygame.FINGERMOTION:
                active_touches[e.finger_id] = (e.x, e.y)
            if e.type == pygame.FINGERUP:
                if e.finger_id in active_touches:
                    del active_touches[e.finger_id]

        # ===== タッチ判定（同時押し対応） =====
        for tx, ty in active_touches.values():
            x, y = tx*WIDTH, ty*HEIGHT
            if left_btn.collidepoint((x,y)): moving_left = True
            if right_btn.collidepoint((x,y)): moving_right = True
            if shoot_btn.collidepoint((x,y)): shooting = True

        # PC用（おまけ）
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            mx, my = pygame.mouse.get_pos()
            if left_btn.collidepoint((mx,my)): moving_left = True
            if right_btn.collidepoint((mx,my)): moving_right = True
            if shoot_btn.collidepoint((mx,my)): shooting = True

        # クールタイム
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        # プレイヤー
        if moving_left: player.x -= 5
        if moving_right: player.x += 5

        if shooting and shoot_cooldown == 0:
            player_bullets.append(pygame.Rect(player.centerx-5, player.y,10,10))

            if random.random() < cooldown_chance:
                shoot_cooldown = cooldown_time

        player.x = max(0,min(WIDTH-player.width,player.x))

        # 敵
        dx = player.centerx - enemy.centerx
        direction = dx/abs(dx) if dx!=0 else 0
        enemy.x += direction * cp_levels[cp_level]["speed"]
        enemy.x = max(0,min(WIDTH-enemy.width,enemy.x))

        if random.randint(0,cp_levels[cp_level]["shoot_rate"])==0:
            enemy_bullets.append(pygame.Rect(enemy.centerx-5,enemy.bottom,10,10))

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

        # 勝敗
        if player_hp <= 0 or enemy_hp <= 0:
            screen.fill(BLACK)
            text = font.render("WIN" if enemy_hp<=0 else "LOSE", True, BLUE if enemy_hp<=0 else RED)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
            pygame.display.flip()
            await asyncio.sleep(2)
            running=False
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

        pygame.draw.rect(screen, GRAY if shoot_cooldown>0 else RED, shoot_btn)

        screen.blit(font_small.render("L",True,WHITE),(left_btn.x+30,left_btn.y+25))
        screen.blit(font_small.render("R",True,WHITE),(right_btn.x+30,right_btn.y+25))
        screen.blit(font_small.render("SHOOT",True,WHITE),(shoot_btn.x+5,shoot_btn.y+25))

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())