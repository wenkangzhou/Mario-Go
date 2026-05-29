from PIL import Image, ImageDraw
import random
random.seed(42)

def save_img(name, w, h, draw_fn):
    img = Image.new('RGBA', (w, h), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw_fn(draw, w, h)
    img.save(name)

def draw_grid(draw, grid, palette, px=2, ox=0, oy=0):
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in palette and ch != ' ' and ch != '.':
                draw.rectangle([ox + x*px, oy + y*px, ox + (x+1)*px, oy + (y+1)*px], fill=palette[ch])

def add_noise(img, bbox, density=0.15, color_var=20):
    px = img.load()
    x1, y1, x2, y2 = bbox
    for y in range(max(0, y1), min(img.height, y2)):
        for x in range(max(0, x1), min(img.width, x2)):
            if random.random() < density:
                r, g, b, a = px[x, y]
                if a > 0:
                    d = random.randint(-color_var, color_var)
                    px[x, y] = (max(0, min(255, r+d)), max(0, min(255, g+d)), max(0, min(255, b+d)), a)

# ============== 玩家 40x60 ==============
def draw_player(draw, w, h):
    # SMB1 style small Mario: 12x16 grid, px=3 -> 36x48, centered in 40x60
    grid = [
        "....RRRR....",
        "...RRRRRR...",
        "...HHSSS....",
        "..HHSSSS....",
        "..HHKSSS....",
        "..SSHHHH....",
        "..SRRRRRR...",
        "..RRBBRR....",
        "...BBBB.....",
        "...BBBB.....",
        "..BBBBBB....",
        "..BBBBBB....",
        "..BB..BB....",
        "..BB..BB....",
        "..HH..HH....",
        "..HH..HH....",
    ]
    palette = {
        'R': (255, 50, 50),
        'H': (140, 70, 30),
        'S': (255, 200, 140),
        'K': (0, 0, 0),
        'B': (60, 100, 240),
    }
    draw_grid(draw, grid, palette, px=3, ox=2, oy=6)

# ============== 大马里奥 40x80 ==============
def draw_big_player(draw, w, h):
    # SMB1 style big Mario: 16x32 grid, px=2 -> 32x64, centered in 40x80
    grid = [
        "......RRRR......",
        ".....RRRRRR.....",
        ".....RRRRRR.....",
        ".....HHSSSS.....",
        "....HHSSSSSS....",
        "....HHHSSSS.....",
        "....HHKSSSSS....",
        "....SSSHHHHH....",
        "....SSRRRRRR....",
        "....SRRRRRRRR...",
        "....RRRRRRRRR...",
        "....RRRRRRRRR...",
        "....BYBRRBYB....",
        "....BBBBBBBB....",
        ".....BBBBBBB....",
        ".....BBBBBBB....",
        "....BBBBBBBBB...",
        "....BBBBBBBBB...",
        "....BBBBBBBBB...",
        "....BB.....BB...",
        "....BB.....BB...",
        "....BB.....BB...",
        "....WW.....WW...",
        "....WW.....WW...",
        "....WW.....WW...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
    ]
    palette = {
        'R': (255, 50, 50),
        'H': (140, 70, 30),
        'S': (255, 200, 140),
        'K': (0, 0, 0),
        'B': (60, 100, 240),
        'W': (255, 255, 255),
        'Y': (255, 220, 0),
    }
    draw_grid(draw, grid, palette, px=2, ox=4, oy=8)

# ============== 火焰马里奥 40x80 ==============
def draw_fire_player(draw, w, h):
    # SMB1 style fire Mario: 16x32 grid, px=2 -> 32x64, centered in 40x80
    grid = [
        "......WWWW......",
        ".....WWWWWW.....",
        ".....WWWWWW.....",
        ".....HHSSSS.....",
        "....HHSSSSSS....",
        "....HHHSSSS.....",
        "....HHKSSSSS....",
        "....SSSHHHHH....",
        "....SSRRRRRR....",
        "....SRRRRRRRR...",
        "....RRRRRRRRR...",
        "....RRRRRRRRR...",
        "....GYGRRGYG....",
        "....GGGGGGGG....",
        ".....GGGGGGG....",
        ".....GGGGGGG....",
        "....GGGGGGGGG...",
        "....GGGGGGGGG...",
        "....GGGGGGGGG...",
        "....GG.....GG...",
        "....GG.....GG...",
        "....GG.....GG...",
        "....WW.....WW...",
        "....WW.....WW...",
        "....WW.....WW...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
        "....HH.....HH...",
    ]
    palette = {
        'W': (255, 255, 255),
        'H': (140, 70, 30),
        'S': (255, 200, 140),
        'K': (0, 0, 0),
        'R': (255, 50, 50),
        'G': (50, 180, 50),
        'Y': (255, 220, 0),
    }
    draw_grid(draw, grid, palette, px=2, ox=4, oy=8)

# ============== 敌人 40x40 ==============
def draw_enemy(draw, w, h):
    # 脚
    draw.rectangle([8, 34, 18, 40], fill=(110, 60, 35))
    draw.rectangle([8, 34, 18, 36], fill=(140, 85, 55))
    draw.rectangle([22, 34, 32, 40], fill=(110, 60, 35))
    draw.rectangle([22, 34, 32, 36], fill=(140, 85, 55))

    # 身体
    draw.rectangle([10, 18, 30, 36], fill=(245, 225, 190))
    draw.rectangle([10, 18, 30, 20], fill=(255, 245, 220))
    draw.rectangle([10, 34, 30, 36], fill=(215, 195, 160))
    draw.rectangle([10, 18, 12, 36], fill=(255, 245, 220))
    draw.rectangle([28, 18, 30, 36], fill=(215, 195, 160))

    # 蘑菇头
    draw.ellipse([2, 0, 38, 22], fill=(170, 100, 60))
    draw.ellipse([2, 0, 38, 22], outline=(125, 70, 40), width=2)
    draw.ellipse([6, 2, 22, 10], fill=(200, 130, 90))

    # 眼睛
    draw.rectangle([10, 10, 18, 16], fill=(255,255,255))
    draw.rectangle([22, 10, 30, 16], fill=(255,255,255))
    draw.ellipse([12, 12, 16, 14], fill=(0,0,0))
    draw.ellipse([24, 12, 28, 14], fill=(0,0,0))
    draw.point([(13, 11)], fill=(255,255,255))
    draw.point([(25, 11)], fill=(255,255,255))

    # 眉毛
    draw.line([(8, 8), (20, 12)], fill=(0,0,0), width=4)
    draw.line([(20, 12), (32, 8)], fill=(0,0,0), width=4)
    draw.line([(9, 7), (20, 11)], fill=(90, 45, 25), width=2)
    draw.line([(20, 11), (31, 7)], fill=(90, 45, 25), width=2)

# ============== 金币 40x40 ==============
def draw_coin(draw, w, h):
    draw.ellipse([4, 4, 36, 36], fill=(255, 180, 0), outline=(185, 125, 0), width=2)
    draw.ellipse([8, 8, 32, 32], fill=(255, 215, 40))
    draw.arc([8, 8, 32, 32], start=30, end=150, fill=(255, 255, 150), width=3)
    draw.ellipse([14, 12, 22, 18], fill=(255, 255, 220))
    draw.arc([8, 8, 32, 32], start=210, end=330, fill=(205, 145, 0), width=2)

# ============== 地面 40x40 ==============
def draw_ground(draw, w, h):
    # 土壤
    draw.rectangle([0, 12, 40, 40], fill=(145, 95, 60))
    draw.rectangle([0, 12, 40, 14], fill=(115, 70, 45))
    for y in range(16, 40, 6):
        for x in range(0, 40, 6):
            if (x + y) % 12 == 0:
                draw.rectangle([x, y, x+2, y+2], fill=(165, 115, 75))
            elif (x + y) % 12 == 6:
                draw.rectangle([x, y, x+2, y+2], fill=(105, 65, 40))
    # 草皮
    draw.rectangle([0, 0, 40, 14], fill=(65, 175, 65))
    draw.rectangle([0, 0, 40, 4], fill=(95, 215, 95))
    for x in range(0, 40, 5):
        h_grass = 6 + (x % 3) * 3
        draw.line([(x, 14), (x+2, 14-h_grass)], fill=(85, 205, 85), width=2)
        draw.line([(x+2, 14-h_grass), (x+4, 14)], fill=(105, 225, 105), width=2)
    draw.rectangle([0, 10, 40, 12], fill=(50, 150, 50))

# ============== 地下土壤 40x40 ==============
def draw_ground_inner(draw, w, h):
    draw.rectangle([0, 0, 40, 40], fill=(145, 95, 60))
    draw.rectangle([0, 0, 40, 2], fill=(115, 70, 45))
    for y in range(4, 40, 6):
        for x in range(0, 40, 6):
            if (x + y) % 12 == 0:
                draw.rectangle([x, y, x+2, y+2], fill=(165, 115, 75))
            elif (x + y) % 12 == 6:
                draw.rectangle([x, y, x+2, y+2], fill=(105, 65, 40))

# ============== 砖块 40x40 ==============
def draw_brick(draw, w, h):
    base = (185, 95, 55)
    hi = (215, 125, 80)
    sh = (145, 70, 40)
    seam = (115, 60, 30)
    draw.rectangle([0, 0, 40, 40], fill=base)
    draw.rectangle([0, 0, 40, 3], fill=hi)
    draw.rectangle([0, 0, 3, 40], fill=hi)
    draw.rectangle([0, 37, 40, 40], fill=sh)
    draw.rectangle([37, 0, 40, 40], fill=sh)
    draw.line([(0, 12), (40, 12)], fill=seam, width=2)
    draw.line([(0, 26), (40, 26)], fill=seam, width=2)
    draw.line([(20, 0), (20, 12)], fill=seam, width=2)
    draw.line([(10, 12), (10, 26)], fill=seam, width=2)
    draw.line([(30, 12), (30, 26)], fill=seam, width=2)
    draw.line([(20, 26), (20, 40)], fill=seam, width=2)
    for y in range(2, 40, 8):
        for x in range(2, 40, 8):
            if random.random() < 0.3:
                draw.point([(x, y)], fill=sh)
            elif random.random() < 0.3:
                draw.point([(x, y)], fill=hi)

# ============== 问号砖 40x40 ==============
def draw_question(draw, w, h):
    base = (225, 185, 45)
    hi = (255, 225, 85)
    sh = (185, 150, 25)
    dark = (135, 105, 10)
    draw.rectangle([0, 0, 40, 40], fill=base)
    draw.rectangle([0, 0, 40, 4], fill=hi)
    draw.rectangle([0, 0, 4, 40], fill=hi)
    draw.rectangle([0, 36, 40, 40], fill=sh)
    draw.rectangle([36, 0, 40, 40], fill=sh)
    draw.rectangle([4, 4, 36, 36], outline=dark, width=1)
    draw.ellipse([12, 4, 28, 18], outline=dark, width=3)
    draw.line([(20, 18), (20, 26)], fill=dark, width=3)
    draw.ellipse([16, 28, 24, 36], fill=dark)
    draw.ellipse([11, 3, 27, 17], outline=(255, 245, 150), width=1)
    draw.line([(19, 17), (19, 25)], fill=(255, 245, 150), width=1)
    draw.ellipse([15, 27, 23, 35], fill=(255, 245, 150))
    draw.ellipse([4, 4, 9, 9], fill=hi, outline=dark, width=1)
    draw.ellipse([31, 4, 36, 9], fill=hi, outline=dark, width=1)
    draw.ellipse([4, 31, 9, 36], fill=sh, outline=dark, width=1)
    draw.ellipse([31, 31, 36, 36], fill=sh, outline=dark, width=1)

# ============== 管道 40x40 ==============
def draw_pipe(draw, w, h):
    draw.rectangle([8, 12, 32, 40], fill=(40, 160, 40))
    draw.rectangle([8, 12, 12, 40], fill=(70, 200, 70))
    draw.rectangle([28, 12, 32, 40], fill=(25, 110, 25))
    draw.line([(12, 12), (12, 40)], fill=(35, 140, 35), width=1)
    draw.line([(28, 12), (28, 40)], fill=(35, 140, 35), width=1)
    draw.rectangle([4, 0, 36, 12], fill=(55, 190, 55))
    draw.rectangle([4, 0, 8, 12], fill=(85, 230, 85))
    draw.rectangle([32, 0, 36, 12], fill=(30, 130, 30))
    draw.rectangle([4, 10, 36, 12], fill=(30, 130, 30))
    draw.rectangle([10, 2, 30, 8], fill=(15, 60, 15))
    draw.rectangle([10, 2, 30, 3], fill=(40, 100, 40))

# ============== 食人花 40x60 ==============
def draw_piranha(draw, w, h):
    draw.rectangle([16, 28, 24, 60], fill=(40, 160, 40))
    draw.rectangle([16, 28, 18, 60], fill=(65, 200, 65))
    draw.rectangle([22, 28, 24, 60], fill=(25, 110, 25))
    for y in range(30, 60, 8):
        draw.ellipse([17, y, 19, y+3], fill=(25, 110, 25))
        draw.ellipse([21, y+4, 23, y+7], fill=(65, 200, 65))

    draw.ellipse([4, 2, 36, 32], fill=(230, 40, 40))
    draw.ellipse([4, 2, 36, 32], outline=(180, 20, 20), width=2)
    draw.ellipse([8, 4, 22, 14], fill=(255, 100, 100))
    draw.ellipse([8, 16, 12, 20], fill=(180, 20, 20))
    draw.ellipse([28, 20, 32, 24], fill=(180, 20, 20))
    draw.ellipse([18, 8, 22, 12], fill=(180, 20, 20))

    draw.ellipse([10, 6, 17, 13], fill=(255, 255, 255), outline=(200,200,200), width=1)
    draw.ellipse([24, 8, 31, 15], fill=(255, 255, 255), outline=(200,200,200), width=1)
    draw.ellipse([12, 8, 15, 11], fill=(0, 0, 0))
    draw.ellipse([26, 10, 29, 13], fill=(0, 0, 0))
    draw.point([(13, 9)], fill=(255,255,255))
    draw.point([(27, 11)], fill=(255,255,255))

    draw.polygon([(20, 16), (10, 26), (20, 30), (30, 26)], fill=(255, 255, 255), outline=(0,0,0), width=2)
    for x in range(12, 20, 3):
        draw.line([(x, 18), (x, 22)], fill=(0,0,0), width=2)
    for x in range(21, 29, 3):
        draw.line([(x, 18), (x, 22)], fill=(0,0,0), width=2)
    for x in range(14, 19, 3):
        draw.line([(x, 26), (x, 29)], fill=(0,0,0), width=2)
    for x in range(22, 27, 3):
        draw.line([(x, 26), (x, 29)], fill=(0,0,0), width=2)

# ============== 蘑菇 40x40 ==============
def draw_mushroom(draw, w, h):
    draw.rectangle([14, 20, 26, 38], fill=(240, 240, 240))
    draw.rectangle([14, 20, 16, 38], fill=(255, 255, 255))
    draw.rectangle([24, 20, 26, 38], fill=(200, 200, 200))
    draw.rectangle([14, 36, 26, 38], fill=(180, 180, 180))
    draw.ellipse([14, 35, 26, 40], fill=(200, 200, 200))

    draw.ellipse([4, 2, 36, 24], fill=(225, 35, 35))
    draw.ellipse([4, 2, 36, 24], outline=(175, 15, 15), width=2)
    draw.ellipse([8, 4, 22, 12], fill=(255, 90, 90))
    draw.arc([4, 2, 36, 24], start=180, end=360, fill=(175, 15, 15), width=2)

    draw.ellipse([10, 6, 18, 14], fill=(255, 255, 255))
    draw.ellipse([24, 8, 32, 14], fill=(255, 255, 255))
    draw.ellipse([16, 14, 24, 20], fill=(255, 255, 255))

# ============== 火花 40x40 ==============
def draw_flower(draw, w, h):
    draw.rectangle([18, 24, 22, 38], fill=(40, 160, 40))
    draw.rectangle([18, 24, 19, 38], fill=(70, 200, 70))
    draw.rectangle([21, 24, 22, 38], fill=(25, 110, 25))

    draw.polygon([(18, 30), (10, 26), (18, 34)], fill=(50, 190, 50))
    draw.polygon([(18, 30), (10, 26), (16, 30)], fill=(70, 220, 70))
    draw.polygon([(22, 32), (30, 28), (22, 36)], fill=(50, 190, 50))
    draw.polygon([(22, 32), (30, 28), (24, 32)], fill=(70, 220, 70))

    petals = [
        ([8, 4, 16, 12], (255, 140, 0)),
        ([24, 4, 32, 12], (255, 140, 0)),
        ([4, 10, 12, 18], (255, 140, 0)),
        ([28, 10, 36, 18], (255, 140, 0)),
        ([8, 16, 16, 24], (255, 140, 0)),
        ([24, 16, 32, 24], (255, 140, 0)),
    ]
    for bbox, color in petals:
        draw.ellipse(bbox, fill=color)
        hx, hy = bbox[0]+1, bbox[1]+1
        draw.ellipse([hx, hy, hx+3, hy+3], fill=(255, 200, 100))

    draw.ellipse([14, 8, 26, 20], fill=(255, 220, 0))
    draw.ellipse([14, 8, 26, 20], outline=(200, 170, 0), width=1)
    draw.ellipse([16, 10, 22, 14], fill=(255, 255, 150))

# ============== 火球 20x20 ==============
def draw_fireball(draw, w, h):
    draw.ellipse([2, 2, 18, 18], fill=(255, 80, 0), outline=(200, 40, 0), width=2)
    draw.ellipse([4, 4, 16, 16], fill=(255, 150, 0))
    draw.ellipse([6, 6, 14, 14], fill=(255, 220, 50))
    draw.ellipse([8, 8, 12, 12], fill=(255, 255, 200))
    draw.ellipse([0, 10, 4, 14], fill=(255, 100, 0))
    draw.ellipse([1, 6, 4, 9], fill=(255, 150, 0))
    draw.ellipse([16, 10, 20, 14], fill=(255, 100, 0))

# ============== 终点旗杆 60x360 ==============
def draw_goal(draw, w, h):
    draw.rectangle([28, 0, 32, h], fill=(190, 190, 190))
    draw.rectangle([28, 0, 30, h], fill=(225, 225, 225))
    draw.rectangle([31, 0, 32, h], fill=(150, 150, 150))
    for y in range(20, h, 40):
        draw.rectangle([27, y, 33, y+2], fill=(165, 165, 165))

    draw.ellipse([24, -4, 36, 12], fill=(255, 220, 0))
    draw.ellipse([24, -4, 36, 12], outline=(200, 170, 0), width=1)
    draw.ellipse([26, -2, 32, 6], fill=(255, 255, 150))

# ============== 旗帜 30x40 ==============
def draw_flag(draw, w, h):
    draw.polygon([(2, 4), (28, 16), (2, 28)], fill=(255, 50, 50), outline=(200, 30, 30), width=1)
    draw.polygon([(2, 4), (28, 16), (8, 12)], fill=(255, 100, 100))
    draw.line([(2, 0), (2, 36)], fill=(220, 220, 220), width=2)

# ============== 乌龟 40x40 ==============
def draw_koopa(draw, w, h):
    # SMB1 style Koopa: 20x20 grid, px=2 -> 40x40
    grid = [
        "....................",
        "....................",
        "....................",
        ".........GGGG.......",
        ".......GGGGGGGG.....",
        "......GGGGGGGGGG....",
        ".....GGGGGGGGGGGG...",
        ".....GGGGGGGGGGGG...",
        ".....GGGGGGGGGGGG...",
        ".....GGGGGGGGGGGG...",
        ".....GGGGGGGGGGGG...",
        ".....GGGGGGGGGWWGG..",
        "......GGGGGGGGWKGGG.",
        ".......GGGGGGGGGG...",
        "........GGGGGGG.....",
        ".........GGGG.......",
        ".........GG..GG.....",
        ".........GG..GG.....",
        ".........GG..GG.....",
        "....................",
    ]
    palette = {
        'G': (50, 180, 50),
        'W': (255, 255, 255),
        'K': (0, 0, 0),
    }
    draw_grid(draw, grid, palette, px=2, ox=0, oy=0)

# ============== 龟壳 30x30 ==============
def draw_shell(draw, w, h):
    # SMB1 style shell: 15x15 grid, px=2 -> 30x30
    grid = [
        "...............",
        "...............",
        ".....GGGGG.....",
        "...GGGGGGGGG...",
        "..GGGGGGGGGGG..",
        ".GGGGGGGGGGGGG.",
        ".GGGDGGDGGDGGG.",
        ".GGGDGGDGGDGGG.",
        ".GGGDGGDGGDGGG.",
        ".GGGDGGDGGDGGG.",
        ".GGGDGGDGGDGGG.",
        "..GGDGGDGGDGG..",
        "..GGDGGDGGDGG..",
        "...GGGGGGGGG...",
        ".....GGGGG.....",
    ]
    palette = {
        'G': (50, 180, 50),
        'D': (30, 130, 30),
    }
    draw_grid(draw, grid, palette, px=2, ox=0, oy=0)

# ============== 无敌星 40x40 ==============
def draw_star(draw, w, h):
    pts = [(20, 2), (24, 14), (38, 14), (28, 22), (32, 36), (20, 28), (8, 36), (12, 22), (2, 14), (16, 14)]
    draw.polygon(pts, fill=(255, 220, 0), outline=(200, 170, 0), width=2)
    draw.polygon([(20, 2), (24, 14), (20, 14)], fill=(255, 255, 150))
    draw.polygon([(20, 2), (16, 14), (20, 14)], fill=(255, 255, 150))
    draw.polygon([(2, 14), (16, 14), (12, 22), (8, 18)], fill=(255, 255, 150))
    draw.polygon([(24, 14), (38, 14), (32, 18), (28, 22)], fill=(255, 255, 150))
    draw.ellipse([16, 16, 24, 24], fill=(255, 255, 200))
    draw.polygon([(20, 28), (32, 36), (28, 30)], fill=(200, 170, 0))
    draw.polygon([(20, 28), (8, 36), (12, 30)], fill=(200, 170, 0))

# ============== 城堡 120x120 ==============
def draw_castle(draw, w, h):
    draw.rectangle([15, 30, 105, 120], fill=(165, 165, 165))
    draw.rectangle([15, 30, 105, 33], fill=(195, 195, 195))
    draw.rectangle([15, 30, 18, 120], fill=(195, 195, 195))
    draw.rectangle([102, 30, 105, 120], fill=(130, 130, 130))
    for y in range(36, 120, 10):
        draw.line([(15, y), (105, y)], fill=(130, 130, 130), width=1)
    for x in range(20, 105, 15):
        for y in range(36, 120, 20):
            draw.line([(x, y), (x, y+10)], fill=(130, 130, 130), width=1)

    draw.rectangle([6, 12, 33, 60], fill=(155, 155, 155))
    draw.rectangle([6, 12, 9, 60], fill=(185, 185, 185))
    draw.rectangle([30, 12, 33, 60], fill=(120, 120, 120))
    draw.polygon([(6, 12), (19, 0), (33, 12)], fill=(185, 55, 55))
    draw.polygon([(6, 12), (19, 0), (15, 8)], fill=(225, 85, 85))
    draw.polygon([(19, 0), (33, 12), (25, 8)], fill=(145, 35, 35))

    draw.rectangle([87, 12, 114, 60], fill=(155, 155, 155))
    draw.rectangle([87, 12, 90, 60], fill=(185, 185, 185))
    draw.rectangle([111, 12, 114, 60], fill=(120, 120, 120))
    draw.polygon([(87, 12), (100, 0), (114, 12)], fill=(185, 55, 55))
    draw.polygon([(87, 12), (100, 0), (96, 8)], fill=(225, 85, 85))
    draw.polygon([(100, 0), (114, 12), (106, 8)], fill=(145, 35, 35))

    draw.rectangle([45, 0, 75, 45], fill=(155, 155, 155))
    draw.rectangle([45, 0, 48, 45], fill=(185, 185, 185))
    draw.rectangle([72, 0, 75, 45], fill=(120, 120, 120))
    draw.polygon([(45, 0), (60, -10), (75, 0)], fill=(185, 55, 55))
    draw.polygon([(45, 0), (60, -10), (55, -5)], fill=(225, 85, 85))
    draw.polygon([(60, -10), (75, 0), (66, -5)], fill=(145, 35, 35))

    draw.rectangle([48, 75, 72, 120], fill=(85, 45, 25))
    draw.rectangle([48, 75, 52, 120], fill=(115, 65, 35))
    draw.rectangle([68, 75, 72, 120], fill=(55, 25, 10))
    draw.arc([48, 65, 72, 95], start=0, end=180, fill=(65, 35, 20), width=3)

    draw.rectangle([21, 24, 30, 36], fill=(65, 45, 25))
    draw.rectangle([21, 24, 24, 36], fill=(95, 65, 35))
    draw.rectangle([90, 24, 99, 36], fill=(65, 45, 25))
    draw.rectangle([90, 24, 93, 36], fill=(95, 65, 35))

# ============== 1UP 蘑菇 40x40 ==============
def draw_1up(draw, w, h):
    draw.rectangle([14, 20, 26, 38], fill=(240, 240, 240))
    draw.rectangle([14, 20, 16, 38], fill=(255, 255, 255))
    draw.rectangle([24, 20, 26, 38], fill=(200, 200, 200))
    draw.rectangle([14, 36, 26, 38], fill=(180, 180, 180))
    draw.ellipse([14, 35, 26, 40], fill=(200, 200, 200))

    draw.ellipse([4, 2, 36, 24], fill=(45, 165, 45))
    draw.ellipse([4, 2, 36, 24], outline=(28, 115, 28), width=2)
    draw.ellipse([8, 4, 22, 12], fill=(78, 215, 78))
    draw.arc([4, 2, 36, 24], start=180, end=360, fill=(28, 115, 28), width=2)

    draw.ellipse([10, 6, 18, 14], fill=(255, 255, 255))
    draw.ellipse([24, 8, 32, 14], fill=(255, 255, 255))
    draw.ellipse([16, 14, 24, 20], fill=(255, 255, 255))

# ============== 已用砖块 40x40 ==============
def draw_used_block(draw, w, h):
    base = (185, 145, 100)
    hi = (215, 175, 130)
    sh = (145, 110, 70)
    draw.rectangle([0, 0, 40, 40], fill=base)
    draw.rectangle([0, 0, 40, 3], fill=hi)
    draw.rectangle([0, 0, 3, 40], fill=hi)
    draw.rectangle([0, 37, 40, 40], fill=sh)
    draw.rectangle([37, 0, 40, 40], fill=sh)
    for y in range(4, 36, 6):
        for x in range(4, 36, 6):
            if random.random() < 0.15:
                draw.point([(x, y)], fill=sh)
            elif random.random() < 0.15:
                draw.point([(x, y)], fill=hi)

# ============== 云朵 80x40 ==============
def draw_cloud(draw, w, h):
    c = (255, 255, 255)
    sh = (240, 248, 255)
    draw.ellipse([10, 20, 70, 38], fill=c)
    draw.ellipse([20, 10, 60, 30], fill=c)
    draw.ellipse([5, 15, 30, 32], fill=c)
    draw.ellipse([50, 15, 78, 32], fill=c)
    draw.ellipse([30, 5, 50, 22], fill=c)
    draw.ellipse([15, 28, 35, 36], fill=sh)
    draw.ellipse([45, 28, 65, 36], fill=sh)

# ============== 生成所有素材 ==============
save_img("player.png", 40, 60, draw_player)
save_img("big_player.png", 40, 80, draw_big_player)
save_img("fire_player.png", 40, 80, draw_fire_player)
save_img("enemy.png", 40, 40, draw_enemy)
save_img("coin.png", 40, 40, draw_coin)
save_img("mushroom.png", 40, 40, draw_mushroom)
save_img("flower.png", 40, 40, draw_flower)
save_img("fireball.png", 20, 20, draw_fireball)
save_img("ground.png", 40, 40, draw_ground)
save_img("ground_inner.png", 40, 40, draw_ground_inner)
save_img("brick.png", 40, 40, draw_brick)
save_img("question.png", 40, 40, draw_question)
save_img("pipe.png", 40, 40, draw_pipe)
save_img("piranha.png", 40, 60, draw_piranha)
save_img("goal.png", 60, 360, draw_goal)
save_img("flag.png", 30, 40, draw_flag)
save_img("koopa.png", 40, 40, draw_koopa)
save_img("shell.png", 30, 30, draw_shell)
save_img("star.png", 40, 40, draw_star)
save_img("castle.png", 120, 120, draw_castle)
save_img("used_block.png", 40, 40, draw_used_block)
save_img("1up.png", 40, 40, draw_1up)
save_img("cloud.png", 80, 40, draw_cloud)
print("素材生成完成")
