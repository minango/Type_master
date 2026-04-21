import pygame
import sys
import random
import time
import numpy as np
import pykakasi
import json
import os

def save_best_score(score):
    if os.path.exists("best_score.json"):
        with open("best_score.json","r") as f:
            best = json.load(f)
    else:
        best = 0

    if score > best:
        with open("best_score.json","w") as f:
            json.dump(score, f)
# ===== 記録読み込み・保存 =====
def load_records():
    if os.path.exists("records.json"):
        with open("records.json", "r") as f:
            return json.load(f)
    else:
        return {
            "best_score": 0,
            "best_rank": "Starter",
            "best_wpm": 0,
            "best_max_wpm": 0,
            "best_rkpm": 0
        }

def save_records(records):
    with open("records.json", "w") as f:
        json.dump(records, f)


kks = pykakasi.kakasi()

pygame.init()

WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TypeMaster")

clock = pygame.time.Clock()

# ===== フォント =====
font_big = pygame.font.Font("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 70)
font = pygame.font.Font("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 40)
font_small = pygame.font.Font("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 30)

# ===== データ =====
words = [
"林檎","蜜柑","葡萄","西瓜","桃","梨","苺","柿","檸檬","香蕉",
"机","椅子","教室","黒板","消しゴム","鉛筆","筆箱","教科書","辞書","時計",
"電車","駅","改札","切符","運転","道路","信号","横断歩道","駐車場","高速道路",
"海","山","川","空","雲","風","雨","雪","雷","太陽",
"春","夏","秋","冬","朝","昼","夕方","夜","深夜","休日",
"学校","大学","先生","友達","授業","試験","合格","勉強","宿題","発表",
"音楽","映画","写真","絵画","小説","漫画","雑誌","新聞","記事","物語",
"携帯","画面","電源","充電","通信","電波","操作","設定","記録","保存",
"料理","食事","朝食","昼食","夕食","味噌汁","焼肉","寿司","天麩羅","弁当",
"運動","走行","跳躍","筋肉","練習","試合","勝利","敗北","挑戦","記録更新"
]

shorts = [
"今日は天気がいい","静かな朝が好き","ゆっくり歩いて帰る","少しだけ休憩する","音楽を聴きながら進む",
"雨の日は家で過ごす","新しい本を読み始める","友達と笑い合う","早起きは気持ちいい","夜空を見上げる",
"風が心地よく吹く","予定を確認する","机の上を整理する","コーヒーを飲む","窓を開けて空気を入れる",
"軽く運動してみる","集中して作業する","少し遠回りして帰る","空をぼんやり眺める","好きな曲を流す",
"ゆっくり深呼吸する","静かな時間を楽しむ","気分転換に外へ出る","新しいことを試す","メモを取りながら進める",
"予定を立て直す","丁寧に作業する","無理せず続ける","少しずつ進める","目標を決める",
"落ち着いて考える","周りをよく見る","慎重に行動する","一歩ずつ進む","少し休んでから再開する",
"集中力を保つ","リズムよく進める","深く考えすぎない","軽く笑ってみる","気楽に取り組む",
"新しい発見を楽しむ","工夫してみる","気分を変えてみる","やり方を見直す","小さな成功を喜ぶ",
"気を抜かずに進む","焦らず取り組む","しっかり確認する","次の準備をする","流れを大切にする",
"無駄を減らす","効率よく動く","自然に進める","余裕を持つ","時間を大切にする",
"少し挑戦してみる","考え方を変える","視点を広げる","楽しみながらやる","結果を振り返る",
"次に活かす","改善していく","続けることが大事","気持ちを整える","安定して進む",
"流れを止めない","途中であきらめない","最後までやりきる","自然体で進む","力を抜いてやる",
"少し工夫する","状況を見極める","柔軟に対応する","冷静に判断する","自分のペースで進む",
"少しずつ慣れていく","繰り返して覚える","落ち着いて打つ","正確に進める","丁寧に仕上げる"
]

longs = [
"今日は少し早起きをして静かな時間をゆっくり過ごしてみた",
"何気ない日常の中にも小さな楽しさはたくさん隠れている",
"新しいことに挑戦するのは少し不安だがその分成長できる",
"集中していると時間があっという間に過ぎていく気がする",
"ゆっくりでもいいので確実に前に進んでいくことが大切だ",

"昨日の失敗を引きずらずに次に活かすことが重要になる",
"無理をせず自分のペースで続けることが一番長続きする",
"目標を少し低く設定すると達成しやすくなることもある",
"周りと比べるよりも自分の成長を見る方が大切だと思う",
"少しの工夫で作業効率は大きく変わることがある",

"静かな環境では集中力が高まり作業がはかどりやすい",
"適度な休憩を取ることでパフォーマンスは向上する",
"一度立ち止まって考えることも大切な時間になる",
"新しい視点を持つことで見える景色が変わってくる",
"焦らず落ち着いて行動することで結果は安定する",

"日々の積み重ねが後から大きな差となって現れる",
"少しずつでも続けることが成功への近道になる",
"完璧を求めすぎると逆に動けなくなることがある",
"まずは行動してみることが大きな一歩になる",
"結果よりも過程を大切にすることが重要だ",

"何度も繰り返すことで自然と体が覚えていく",
"最初はうまくいかなくても徐々に慣れていく",
"失敗を恐れず挑戦することが成長につながる",
"少しの違いが大きな結果を生むこともある",
"自分のやり方を見つけることが大切になる",

"時間の使い方次第で一日の価値は大きく変わる",
"計画を立てて行動することで効率が上がる",
"柔軟な考え方を持つことで対応力が上がる",
"小さな成功体験が自信を育ててくれる",
"毎日の積み重ねが未来を形作っていく",

"無理に急ぐよりも確実に進む方が結果は良い",
"適切な目標設定がモチベーションを保つ鍵になる",
"習慣化することで努力が苦にならなくなる",
"環境を整えることも重要な要素の一つだ",
"継続する力が最も大きな武器になる",

"冷静に状況を判断することが重要になる場面もある",
"思い切った決断が良い結果を生むこともある",
"自分を信じて行動することが成功への第一歩だ",
"経験を重ねることで判断力は磨かれていく",
"視野を広げることで新しい可能性が見えてくる"
] * 2

current_list = words
themes = {
    # 1. Shadow（黒×青）
    "shadow": {
        "bg": (5, 5, 15),          # 深い黒青
        "text": (200, 220, 255),
        "subtext": (120, 140, 170),
        "typed": (80, 180, 255),
        "miss": (255, 90, 120),
        "button_bg": (20, 30, 60),
        "button_text": (200, 220, 255),
    },

    # 2. Crimson（黒×赤）
    "crimson": {
        "bg": (30, 0, 0),          # 深い赤黒
        "text": (255, 200, 200),
        "subtext": (150, 120, 120),
        "typed": (255, 120, 120),
        "miss": (255, 80, 80),
        "button_bg": (80, 20, 20),
        "button_text": (255, 200, 200),
    },

    # 3. Emerald（深緑）
    "emerald": {
        "bg": (0, 25, 10),         # 深い緑
        "text": (210, 255, 230),
        "subtext": (130, 170, 150),
        "typed": (120, 255, 180),
        "miss": (255, 120, 150),
        "button_bg": (20, 60, 40),
        "button_text": (210, 255, 230),
    },

    # 4. Steel（ダークグレー）
    "steel": {
        "bg": (25, 25, 35),        # 青みのあるダークグレー
        "text": (200, 230, 240),
        "subtext": (130, 150, 160),
        "typed": (0, 200, 255),
        "miss": (255, 120, 120),
        "button_bg": (50, 50, 70),
        "button_text": (200, 230, 240),
    },

    # 5. Violet（紫）
    "violet": {
        "bg": (25, 0, 40),         # 濃い紫
        "text": (230, 210, 255),
        "subtext": (150, 130, 180),
        "typed": (180, 120, 255),
        "miss": (255, 120, 160),
        "button_bg": (60, 20, 90),
        "button_text": (230, 210, 255),
    },

    # 6. Neon（黒×ネオン）
    "neon": {
        "bg": (0, 0, 10),          # 真っ黒に近いネオン背景
        "text": (0, 255, 200),
        "subtext": (0, 180, 150),
        "typed": (0, 255, 120),
        "miss": (255, 0, 120),
        "button_bg": (0, 80, 80),
        "button_text": (0, 255, 200),
    },

    # 7. Midnight（濃紺）
    "midnight": {
        "bg": (0, 0, 30),          # 深い紺
        "text": (220, 230, 255),
        "subtext": (140, 150, 180),
        "typed": (120, 160, 255),
        "miss": (255, 100, 140),
        "button_bg": (20, 30, 80),
        "button_text": (220, 230, 255),
    },

    # 8. Carbon（黒×グレー）
    "carbon": {
        "bg": (10, 10, 10),        # 完全な黒
        "text": (220, 220, 220),
        "subtext": (150, 150, 150),
        "typed": (180, 255, 180),
        "miss": (255, 120, 120),
        "button_bg": (40, 40, 40),
        "button_text": (220, 220, 220),
    },

    # 9. Abyss（深海ブルー）
    "abyss": {
        "bg": (0, 10, 30),         # 深海の青
        "text": (180, 220, 255),
        "subtext": (100, 140, 180),
        "typed": (80, 200, 255),
        "miss": (255, 100, 140),
        "button_bg": (10, 40, 80),
        "button_text": (180, 220, 255),
    },

    # 10. Obsidian（黒曜石）
    "obsidian": {
        "bg": (15, 0, 25),         # 黒曜石の紫黒
        "text": (220, 200, 255),
        "subtext": (150, 130, 180),
        "typed": (160, 120, 255),
        "miss": (255, 120, 160),
        "button_bg": (40, 10, 60),
        "button_text": (220, 200, 255),
    }
}





current_theme = "shadow"
records = load_records()


# ===== 状態 =====
state = "title"
current_text = ""
current_roma = ""
current_candidates = []
typed = ""

miss_count = 0
total_inputs = 0

start_time = 0
problem_start_time = 0
first_key_time = None
game_time = 60

show_wpm = 0
show_latency = 0
show_time = 0
showing = False

pause_total = 0
pause_start = 0
result_enter_time = 0
last_text = None
max_wpm = 0
rkpm = 0
latency_list = []
problem_start_inputs = 0





buttons = {
    "単語": pygame.Rect(300,200,300,60),
    "短文": pygame.Rect(300,280,300,60),
    "長文": pygame.Rect(300,360,300,60),
}
settings_button = pygame.Rect(820, 440, 60, 40)
highscore_button = pygame.Rect(740, 440, 60, 40)


# ===== 表示（元コードそのまま）=====
def draw_text_multiline(text, font, color, x, y, max_width):
    words = list(text)
    lines = []
    current_line = ""

    for ch in words:
        test_line = current_line + ch
        test_surface = font.render(test_line, True, color)

        if test_surface.get_width() > max_width:
            lines.append(current_line)
            current_line = ch
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        screen.blit(line_surface, (x, y + i * 45))

def draw_roma_with_color(full_text, typed_len, font, x, y, max_width):
    cx = x
    cy = y
    line_height = 45

    for i, ch in enumerate(full_text):
        color = themes[current_theme]["typed"] if i < typed_len else themes[current_theme]["subtext"]
        ch_surface = font.render(ch, True, color)
        ch_width = ch_surface.get_width()

        if cx + ch_width > x + max_width:
            cx = x
            cy += line_height

        screen.blit(ch_surface, (cx, cy))
        cx += ch_width

# ===== ローマ字パターン =====
def get_patterns(ch, next_ch=None):
    base = {
        "あ":["a"],"い":["i","yi"],"う":["u","wu","whu"],"え":["e"],"お":["o"],
        "か":["ka","ca"],"き":["ki"],"く":["ku","cu"],"け":["ke"],"こ":["ko","co"],
        "さ":["sa"],"し":["shi","si","ci"],"す":["su"],"せ":["se","ce"],"そ":["so"],
        "た":["ta"],"ち":["chi","ti"],"つ":["tsu","tu"],"て":["te"],"と":["to"],
        "な":["na"],"に":["ni"],"ぬ":["nu"],"ね":["ne"],"の":["no"],
        "は":["ha"],"ひ":["hi"],"ふ":["fu","hu"],"へ":["he"],"ほ":["ho"],
        "ま":["ma"],"み":["mi"],"む":["mu"],"め":["me"],"も":["mo"],
        "や":["ya"],"ゆ":["yu"],"よ":["yo"],
        "ら":["ra"],"り":["ri"],"る":["ru"],"れ":["re"],"ろ":["ro"],
        "わ":["wa"],"を":["wo"],
        "が":["ga"],"ぎ":["gi"],"ぐ":["gu"],"げ":["ge"],"ご":["go"],
        "ざ":["za"],"じ":["ji","zi"],"ず":["zu"],"ぜ":["ze"],"ぞ":["zo"],
        "だ":["da"],"ぢ":["di"],"づ":["du"],"で":["de"],"ど":["do"],
        "ば":["ba"],"び":["bi"],"ぶ":["bu"],"べ":["be"],"ぼ":["bo"],
        "ぱ":["pa"],"ぴ":["pi"],"ぷ":["pu"],"ぺ":["pe"],"ぽ":["po"],
    }

    if ch == "ん":
        patterns = ["nn","xn"]
        if next_ch not in ["あ","い","う","え","お","や","ゆ","よ","な","に","ぬ","ね","の"]:
            patterns.append("n")
        return patterns

    if ch == "っ":
        return ["ltu","xtu","ltsu","xtsu"]

    return base.get(ch, [ch])

def apply_small(candidates, small):
    # 小文字そのもの
    table = {
        "ゃ": ["xya","lya","ya"],
        "ゅ": ["xyu","lyu","yu"],
        "ょ": ["xyo","lyo","yo"],
    }

    # 通常拗音（mya / sha / cha など）
    normal = {
        "ゃ": "ya",
        "ゅ": "yu",
        "ょ": "yo",
    }

    new_list = []
    for c in candidates:
        # ★ 子音部分（最後の母音だけ削る）
        base = c
        while base and base[-1] in "aiueo":
            base = base[:-1]

        # ★ “i” を削った分、元の c の最後の母音を保持する
        #    例：shi → base=sh, last_vowel=i → sh + i + xya = shixya
        last_vowel = c[len(base):]  # 例：shi → "i", chi → "i"

        # x系・l系・小文字
        for p in table[small]:
            new_list.append(base + last_vowel + p)

        # 通常拗音（mya / cha / sha）
        new_list.append(base + last_vowel + normal[small])

    return new_list




def build_candidates(hira):
    candidates = [""]
    i = 0
    while i < len(hira):
        ch = hira[i]

        if ch in ["ゃ","ゅ","ょ"]:
            candidates = apply_small(candidates, ch)
            i += 1
            continue

        # ★ 長音（ー）を '-' で入力できるようにする
        if ch == "ー":
            new_list = []
            for base in candidates:
                new_list.append(base + "-")
            candidates = new_list
            i += 1
            continue

        next_ch = hira[i+1] if i+1 < len(hira) else None
        patterns = get_patterns(ch, next_ch)

        new_list = []
        for base in candidates:
            for p in patterns:
                new_list.append(base + p)

        candidates = new_list
        i += 1

    return candidates
# ===== new_problem（最小変更で候補方式を追加）=====
def new_problem():
    global current_text, current_roma, current_candidates, typed
    global first_key_time, problem_start_time

    global last_text

    # 同じ文章を避ける
    while True:
        new_text = random.choice(current_list)
        if new_text != last_text:
            break

    current_text = new_text
    last_text = new_text

    # ひらがな変換
    result = kks.convert(current_text)
    hira = "".join([item["hira"] for item in result])

    typed = ""
    current_roma = ""          # 表示用（元コード維持）
    current_candidates = build_candidates(hira)   # 判定用（追加）

    # ===== 元コードのローマ字生成（表示用）=====
    i = 0
    while i < len(hira):
        ch = hira[i]

        # 拗音（ゃゅょ）
        if i + 1 < len(hira):
            pair = hira[i:i+2]
            if pair == "しゃ": current_roma += "sha"; i += 2; continue
            if pair == "しゅ": current_roma += "shu"; i += 2; continue
            if pair == "しょ": current_roma += "sho"; i += 2; continue
            if pair == "ちゃ": current_roma += "cha"; i += 2; continue
            if pair == "ちゅ": current_roma += "chu"; i += 2; continue
            if pair == "ちょ": current_roma += "cho"; i += 2; continue

        # 促音（っ）
        if ch == "っ":
            if i + 1 < len(hira):
                next_ch = hira[i+1]
                # get_patterns の最初の候補の最初の文字を使う
                current_roma += get_patterns(next_ch)[0][0]
            i += 1
            continue

        # ん
        if ch == "ん":
            current_roma += "nn"
        else:
            # get_patterns の最初の候補を表示用に使う
            current_roma += get_patterns(ch)[0]

        i += 1

    first_key_time = None
    problem_start_time = time.time()
    global problem_start_inputs
    problem_start_inputs = total_inputs


# ===== メインループ（KEYDOWN 判定部分）=====
while True:
    screen.fill(themes[current_theme]["bg"])
    now = time.time()

    # ===== イベント処理 =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ===== タイトル =====
        if state == "title":
            if event.type == pygame.MOUSEBUTTONDOWN:

                # テーマ切り替え
                if settings_button.collidepoint(event.pos):
                    keys = list(themes.keys())
                    idx = keys.index(current_theme)
                    current_theme = keys[(idx + 1) % len(keys)]
                    continue

                # ハイスコア画面へ
                if highscore_button.collidepoint(event.pos):
                    state = "highscore"
                    continue

                # モード選択
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if name == "単語":
                            current_list = words
                        elif name == "短文":
                            current_list = shorts
                        elif name == "長文":
                            current_list = longs

                        miss_count = 0
                        total_inputs = 0
                        start_time = time.time()
                        pause_total = 0

                        new_problem()
                        state = "game"

        # ===== ゲーム =====
        elif state == "game":
            if event.type == pygame.KEYDOWN:

                if showing:
                    continue

                char = event.unicode.lower()
                if not (('a' <= char <= 'z') or char == '-'):
                    continue

                total_inputs += 1

                if not hasattr(new_problem, "prefix_map"):
                    new_problem.prefix_map = {}

                if current_text not in new_problem.prefix_map:
                    prefix_map = {}
                    for c in current_candidates:
                        if len(c) == 0:
                            continue
                        head = c[0]
                        prefix_map.setdefault(head, []).append(c)
                    new_problem.prefix_map[current_text] = prefix_map

                prefix_map = new_problem.prefix_map[current_text]

                typed += char

                if len(typed) == 1:
                    new_list = prefix_map.get(typed[0], [])
                else:
                    new_list = [c for c in current_candidates if c.startswith(typed)]

                if new_list:
                    if first_key_time is None:
                        first_key_time = time.time()
                    current_candidates = new_list
                    current_roma = new_list[0]
                else:
                    miss_count += 1
                    typed = typed[:-1]
                    continue

                if typed in current_candidates:
                    problem_inputs = total_inputs - problem_start_inputs
                    problem_elapsed = time.time() - problem_start_time
                    wpm = int((problem_inputs / problem_elapsed) * 60) if problem_elapsed > 0 else 0
                    max_wpm = max(max_wpm, wpm)

                    if first_key_time:
                        latency = first_key_time - problem_start_time
                        if 0 <= latency <= 3:
                            latency_list.append(latency)
                        show_latency = round(latency, 2)
                    else:
                        show_latency = 0

                    show_wpm = wpm
                    show_time = time.time()
                    pause_start = time.time()
                    showing = True

        # ===== ハイスコア画面 =====
        elif state == "highscore":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = "title"

        # ===== リザルト =====
        elif state == "result":
            if event.type == pygame.KEYDOWN:
                if time.time() - result_enter_time > 0.3:
                    if event.key == pygame.K_RETURN:
                        state = "title"

    # ===== showing の終了処理 =====
    if showing and time.time() - show_time > 1.2:
        showing = False
        pause_total += time.time() - pause_start
        new_problem()

    # ===== 経過時間 =====
    if showing:
        elapsed = show_time - start_time - pause_total
    else:
        elapsed = now - start_time - pause_total

    if state == "game" and elapsed >= game_time:
        state = "result"
        result_enter_time = time.time()

    # ===== 描画 =====
    if state == "title":
        title = font_big.render("TypeMaster", True, themes[current_theme]["text"])
        screen.blit(title, (240, 100))

        pygame.draw.rect(screen, themes[current_theme]["button_bg"], settings_button)
        txt = font_small.render("C", True, themes[current_theme]["button_text"])
        screen.blit(txt, (settings_button.x + 5, settings_button.y + 5))

        pygame.draw.rect(screen, themes[current_theme]["button_bg"], highscore_button)
        txt_h = font_small.render("H", True, themes[current_theme]["button_text"])
        screen.blit(txt_h, (highscore_button.x + 15, highscore_button.y + 5))

        for name, rect in buttons.items():
            pygame.draw.rect(screen,(70,70,70),rect,border_radius=10)
            txt = font.render(name, True, themes[current_theme]["text"])
            screen.blit(txt,(rect.x+100,rect.y+10))

    elif state == "game":
        remain = int(game_time - elapsed)
        screen.blit(font_small.render(f"残り: {remain}s", True, themes[current_theme]["text"]), (10, 10))
        screen.blit(font_small.render(f"ミス: {miss_count}", True, themes[current_theme]["miss"]), (10, 40))

        if not showing:
            draw_text_multiline(current_text, font, themes[current_theme]["text"], 100, 120, 700)
            draw_roma_with_color(current_roma, len(typed), font, 100, 260, 700)
        else:
            screen.blit(font.render(f"{show_wpm} WPM", True, themes[current_theme]["text"]), (330, 180))
            screen.blit(font.render(f"{show_latency}s", True, themes[current_theme]["text"]), (330, 230))

    elif state == "result":
        # ===== リザルト画面 =====
        wpm = int((total_inputs / game_time) * 60)
        acc = int(((total_inputs - miss_count) / total_inputs) * 100) if total_inputs else 0
        avg_latency = sum(latency_list) / len(latency_list) if latency_list else 0

        effective_inputs = max(total_inputs - 15, 1)
        effective_time = game_time - 15 * avg_latency
        if effective_time < 1:
            effective_time = 1

        rkpm = int((effective_inputs / effective_time) * 60)
        score = int((wpm ** 1.2) * (acc / 100))
        # ===== 記録更新フラグ =====
        updated_score = False
        updated_wpm = False
        updated_max_wpm = False
        updated_rkpm = False


        def get_rank(score):
            if score >= 3600: return "Mythic"
            elif score >= 3000: return "Transcendent"
            elif score >= 2500: return "Celestial"
            elif score >= 2000: return "Ethereal"
            elif score >= 1600: return "Masterful"
            elif score >= 1300: return "Supreme"
            elif score >= 1100: return "Radiant"
            elif score >= 900: return "Prime"
            elif score >= 750: return "Skilled"
            elif score >= 600: return "Steady"
            elif score >= 500: return "Refined"
            elif score >= 400: return "Focused"
            elif score >= 300: return "Growing"
            elif score >= 200: return "Rising"
            elif score >= 120: return "Learner"
            elif score >= 60: return "Novice"
            elif score >= 30: return "Beginner"
            else: return "Starter"

        rank = get_rank(score)
        rank_colors = {
            "Mythic": (255,120,255),
            "Transcendent": (180,140,255),
            "Celestial": (140,180,255),
            "Ethereal": (120,220,255),
            "Masterful": (120,255,200),
            "Supreme": (120,255,150),
            "Radiant": (180,255,120),
            "Prime": (230,255,120),
            "Skilled": (255,230,120),
            "Steady": (255,200,120),
            "Refined": (255,170,120),
            "Focused": (255,140,120),
            "Growing": (255,120,120),
            "Rising": (255,120,160),
            "Learner": (255,120,200),
            "Novice": (255,120,230),
            "Beginner": (220,120,255),
            "Starter": (180,120,255),
        }
        color = rank_colors.get(rank, themes[current_theme]["text"])

        screen.blit(font.render(f"ランク: {rank}", True, color), (300, 120))
        screen.blit(font.render(f"スコア: {score}", True, themes[current_theme]["text"]), (300, 160))
        screen.blit(font.render(f"WPM: {wpm}", True, themes[current_theme]["text"]), (300, 210))
        screen.blit(font.render(f"正確性: {acc}%", True, themes[current_theme]["text"]), (300, 260))
        screen.blit(font.render(f"ミス数: {miss_count}", True, themes[current_theme]["miss"]), (300, 310))
        screen.blit(font.render(f"最高WPM: {max_wpm}", True, themes[current_theme]["text"]), (300, 360))
        screen.blit(font.render(f"RKPM: {rkpm}", True, themes[current_theme]["text"]), (300, 410))

    elif state == "highscore":
        screen.blit(font_big.render("High Scores", True, themes[current_theme]["text"]), (250, 80))

        screen.blit(font_small.render(f"最高スコア: {records['best_score']} ({records['best_rank']})",
                                      True, themes[current_theme]["text"]), (250, 180))
        screen.blit(font_small.render(f"最高WPM: {records['best_wpm']}",
                                      True, themes[current_theme]["text"]), (250, 220))
        screen.blit(font_small.render(f"最高最高WPM: {records['best_max_wpm']}",
                                      True, themes[current_theme]["text"]), (250, 260))
        screen.blit(font_small.render(f"最高RKPM: {records['best_rkpm']}",
                                      True, themes[current_theme]["text"]), (250, 300))

        screen.blit(font_small.render("Enterで戻る", True, themes[current_theme]["text"]), (250, 360))

    pygame.display.flip()
    clock.tick(60)


