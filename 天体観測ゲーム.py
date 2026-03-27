import pygame
import math
import csv

pygame.init()

# =====================
# 画面設定
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("天体観測ゲーム")

clock = pygame.time.Clock()
running = True

# =====================
# 星データ読み込み
# =====================
def load_stars(filename):
    stars = []
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stars.append({
                "x": int(row["x"]),
                "y": int(row["y"]),
                "mag": float(row["mag"])
            })
    return stars

stars = load_stars("stars.csv")

# =====================
# 望遠鏡・世界設定
# =====================
scope_x = WIDTH // 2
scope_y = HEIGHT // 2
scope_radius = 320   # 視野サイズ（君が決めた値）

world_x = 0
world_y = 0
speed = 5

# =====================
# フォント
# =====================
font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
font = pygame.font.Font(font_path, 28)

# =====================
# メインループ
# =====================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キー入力（世界を動かす）
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        world_x += speed
    if keys[pygame.K_RIGHT]:
        world_x -= speed
    if keys[pygame.K_UP]:
        world_y += speed
    if keys[pygame.K_DOWN]:
        world_y -= speed

    # 背景
    screen.fill((0, 0, 15))

    # =====================
    # 星の描画
    # =====================
    for star in stars:
        sx = star["x"]
        sy = star["y"]
        mag = star["mag"]

        draw_x = sx + world_x + scope_x
        draw_y = sy + world_y + scope_y

        dx = draw_x - scope_x
        dy = draw_y - scope_y
        dist = math.sqrt(dx * dx + dy * dy)

        size = max(1, int(5 - mag))

        if dist <= scope_radius:
            # 視野内の星
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (draw_x, draw_y),
                size
            )
        else:
            # 視野外の星
            pygame.draw.circle(
                screen,
                (120, 120, 120),
                (draw_x, draw_y),
                max(1, size - 1)
            )

    # =====================
    # 望遠鏡の視野
    # =====================
    pygame.draw.circle(
        screen,
        (255, 255, 0),
        (scope_x, scope_y),
        scope_radius,
        2
    )

    # タイトル
    title = font.render("天体観測ゲーム", True, (255, 255, 255))
    screen.blit(title, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
