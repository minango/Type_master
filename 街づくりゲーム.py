import pygame

pygame.init()

# =====================
# 基本設定
# =====================
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("街づくりゲーム")

font = pygame.font.SysFont("AppleGothic", 20)
big_font = pygame.font.SysFont("AppleGothic", 26)
clock = pygame.time.Clock()

# =====================
# 定数
# =====================
HOUSE_SIZE_DEFAULT = 120
HOUSE_SIZE_HOUSE1 = 200
ROAD_WIDTH = 60
UI_AREA = pygame.Rect(0, 0, 300, HEIGHT)

# =====================
# ゲーム状態
# =====================
turn = 1
actions_left = 3
mode = "none"  # none / build_house / build_road / input_name
selected_house_type = "house1"
selected_house = None

# 名前入力用
name_input = ""
pending_house = None

# =====================
# マップデータ
# =====================
houses = []
roads = []
road_color = (120, 120, 120)

# =====================
# 家画像
# =====================
house_types = {
    "house1": pygame.transform.scale(pygame.image.load("house.png"), (HOUSE_SIZE_HOUSE1, HOUSE_SIZE_HOUSE1)),
    "house2": pygame.transform.scale(pygame.image.load("wood_house.png"), (HOUSE_SIZE_DEFAULT, HOUSE_SIZE_DEFAULT)),
    "house3": pygame.transform.scale(pygame.image.load("old_house.png"), (HOUSE_SIZE_DEFAULT, HOUSE_SIZE_DEFAULT)),
}

# =====================
# 補助関数
# =====================
def is_house_at(x, y, size):
    cx, cy = x + size / 2, y + size / 2
    for h in houses:
        hx, hy = h["x"] + h["size"] / 2, h["y"] + h["size"] / 2
        distance = ((cx - hx)**2 + (cy - hy)**2) ** 0.5
        if distance < 5:  # ほぼくっつけられる
            return True
    return False

def get_house_at_pos(mx, my):
    for h in houses:
        rect = pygame.Rect(h["x"], h["y"], h["size"], h["size"])
        if rect.collidepoint(mx, my):
            return h
    return None

def can_place_house(x, y, size):
    return not UI_AREA.colliderect(pygame.Rect(x, y, size, size))

# =====================
# モード関数
# =====================
def set_mode_house():
    global mode
    if actions_left > 0:
        mode = "build_house"

def set_mode_road():
    global mode
    if actions_left > 0:
        mode = "build_road"

def next_day():
    global turn, actions_left, mode
    turn += 1
    actions_left = 3
    mode = "none"

def set_house_type1(): global selected_house_type; selected_house_type = "house1"
def set_house_type2(): global selected_house_type; selected_house_type = "house2"
def set_house_type3(): global selected_house_type; selected_house_type = "house3"

def set_road_gray(): global road_color; road_color = (120,120,120)
def set_road_brown(): global road_color; road_color = (150,100,50)
def set_road_black(): global road_color; road_color = (60,60,60)

# =====================
# ボタン
# =====================
class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, (200,200,200), self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
        screen.blit(font.render(self.text, True, (0,0,0)), (self.rect.x+10, self.rect.y+8))

    def click(self):
        self.action()

buttons = [
    Button("家を建てる", 20, 80, 260, 40, set_mode_house),
    Button("道を作る", 20, 140, 260, 40, set_mode_road),
    Button("次の日へ", 20, 200, 260, 40, next_day),
    Button("道：GRAY", 20, 260, 260, 30, set_road_gray),
    Button("道：BROWN", 20, 300, 260, 30, set_road_brown),
    Button("道：BLACK", 20, 340, 260, 30, set_road_black),
    Button("普通の家", 20, 380, 120, 30, set_house_type1),
    Button("木の家", 160, 380, 120, 30, set_house_type2),
    Button("古い家", 20, 420, 120, 30, set_house_type3),
]

# =====================
# 道ドラッグ
# =====================
dragging = False
drag_start = None

# =====================
# メインループ
# =====================
running = True
while running:
    screen.fill((180,220,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- 名前入力 --------
        if mode == "input_name" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and name_input:
                pending_house["name"] = name_input
                houses.append(pending_house)
                pending_house = None
                name_input = ""
                mode = "none"
                actions_left -= 1
            elif event.key == pygame.K_BACKSPACE:
                name_input = name_input[:-1]
            else:
                name_input += event.unicode

        # -------- マウス --------
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if event.button == 1:
                for b in buttons:
                    if b.rect.collidepoint(mx,my):
                        b.click()
                        break
                else:
                    if actions_left <= 0:
                        continue

                    clicked = get_house_at_pos(mx, my)
                    if clicked and mode == "none":
                        selected_house = clicked
                        continue

                    if mode == "build_house":
                        size = HOUSE_SIZE_HOUSE1 if selected_house_type=="house1" else HOUSE_SIZE_DEFAULT
                        x, y = mx-size//2, my-size//2

                        if can_place_house(x,y,size) and not is_house_at(x,y,size):
                            pending_house = {
                                "x":x,"y":y,"size":size,
                                "type":selected_house_type,
                                "day":turn
                            }
                            mode = "input_name"

                    elif mode == "build_road":
                        dragging = True
                        drag_start = (mx,my)

        if event.type == pygame.MOUSEBUTTONUP and dragging and mode=="build_road":
            mx,my = event.pos
            sx,sy = drag_start
            dx,dy = mx-sx,my-sy

            if abs(dx)>abs(dy):
                rect = pygame.Rect(min(sx,mx), sy-ROAD_WIDTH//2, abs(dx), ROAD_WIDTH)
            else:
                rect = pygame.Rect(sx-ROAD_WIDTH//2, min(sy,my), ROAD_WIDTH, abs(dy))

            if not UI_AREA.colliderect(rect):
                roads.append({"rect":rect,"color":road_color})
                actions_left -= 1

            dragging=False
            mode="none"

    # =====================
    # 描画
    # =====================
    pygame.draw.rect(screen,(230,230,230),UI_AREA)
    screen.blit(big_font.render(f"{turn}日目",True,(0,0,0)),(20,20))
    screen.blit(font.render(f"行動: {actions_left}",True,(0,0,0)),(20,50))
    screen.blit(font.render(f"モード: {mode}",True,(0,0,0)),(20,260))

    for b in buttons:
        b.draw()

    for r in roads:
        pygame.draw.rect(screen,r["color"],r["rect"])

    for h in houses:
        screen.blit(house_types[h["type"]],(h["x"],h["y"]))

    if selected_house:
        screen.blit(font.render(f"住民名: {selected_house['name']}",True,(0,0,0)),(20,500))
        screen.blit(font.render(f"建てた日: {selected_house['day']}日目",True,(0,0,0)),(20,530))

    if mode=="input_name":
        pygame.draw.rect(screen,(255,255,255),(320,300,360,40))
        pygame.draw.rect(screen,(0,0,0),(320,300,360,40),2)
        screen.blit(font.render(name_input,True,(0,0,0)),(330,310))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
