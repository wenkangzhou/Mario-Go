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
    # SMB1 exact small Mario: 12x16 grid, px=3 -> 36x48, centered in 40x60
    grid = [
        "...RRRRR....",
        "..RRRRRRRRR.",
        "..HHHSSHS...",
        ".HSHSSSHSSS.",
        ".HSHHSSSHSSS",
        ".HHSSSSHHHH.",
        "...SSSSSSS..",
        "..HHRHHH....",
        ".HHHRHHRHHH.",
        "HHHHRRRRHHHH",
        "SSHSRRSRHSSS",
        "SSSRRRRRRSSS",
        "SSRRRRRRRRSS",
        "..RRR..RRR..",
        ".HHH....HHH.",
        "HHHH....HHHH",
    ]
    palette = {
        'R': (220, 40, 20),
        'H': (130, 90, 10),
        'S': (255, 190, 130),
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
    # SMB1 style Koopa: green shell with white diagonal ridges + long neck + round head
    # Shell (green dome with flat bottom)
    draw.ellipse([2, 6, 30, 24], fill=(50, 180, 50), outline=(30, 130, 30), width=2)
    draw.rectangle([2, 20, 30, 26], fill=(50, 180, 50))

    # White diagonal ridges on shell (diamond pattern)
    draw.line([(6, 10), (10, 14)], fill=(255, 255, 255), width=2)
    draw.line([(12, 10), (16, 14)], fill=(255, 255, 255), width=2)
    draw.line([(18, 10), (22, 14)], fill=(255, 255, 255), width=2)
    draw.line([(24, 10), (28, 14)], fill=(255, 255, 255), width=2)
    draw.line([(6, 16), (10, 20)], fill=(255, 255, 255), width=2)
    draw.line([(12, 16), (16, 20)], fill=(255, 255, 255), width=2)
    draw.line([(18, 16), (22, 20)], fill=(255, 255, 255), width=2)
    draw.line([(24, 16), (28, 20)], fill=(255, 255, 255), width=2)

    # Neck (skin tone, thin)
    draw.rectangle([28, 14, 32, 24], fill=(255, 220, 150))

    # Head (white round face)
    draw.ellipse([28, 8, 38, 18], fill=(255, 255, 255))

    # Eye (black dot + white highlight)
    draw.ellipse([32, 10, 36, 14], fill=(0, 0, 0))
    draw.point([(33, 11)], fill=(255, 255, 255))

    # Feet (small green blocks)
    draw.rectangle([8, 26, 14, 32], fill=(50, 180, 50))
    draw.rectangle([20, 26, 26, 32], fill=(50, 180, 50))

# ============== 龟壳 30x30 ==============
def draw_shell(draw, w, h):
    # SMB1 style shell: flattened green dome with vertical ridges
    # Main dome
    draw.ellipse([2, 2, 28, 20], fill=(50, 180, 50), outline=(30, 130, 30), width=2)
    # Flat bottom
    draw.rectangle([2, 16, 28, 24], fill=(50, 180, 50))
    # Vertical ridges
    draw.line([(10, 4), (10, 22)], fill=(30, 130, 30), width=2)
    draw.line([(18, 4), (18, 22)], fill=(30, 130, 30), width=2)
    # Bottom rim
    draw.line([(2, 22), (28, 22)], fill=(30, 130, 30), width=2)

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

# ============== 小夏主角 40x60 ==============
def draw_summer_player_idle(draw, w, h):
    # Shoes
    draw.rectangle([10, 54, 18, 60], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([22, 54, 30, 60], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([10, 58, 18, 60], fill=(215, 35, 35))
    draw.rectangle([22, 58, 30, 60], fill=(215, 35, 35))
    # Socks
    draw.rectangle([12, 52, 16, 54], fill=(255, 255, 255))
    draw.rectangle([24, 52, 28, 54], fill=(255, 255, 255))
    # Legs
    draw.rectangle([11, 42, 17, 52], fill=(255, 205, 155))
    draw.rectangle([23, 42, 29, 52], fill=(255, 205, 155))
    # Shorts
    draw.rectangle([10, 32, 30, 44], fill=(55, 85, 185))
    draw.rectangle([10, 32, 30, 34], fill=(85, 115, 215))
    draw.rectangle([10, 32, 12, 44], fill=(85, 115, 215))
    draw.rectangle([28, 32, 30, 44], fill=(35, 65, 155))
    # T-shirt
    draw.rectangle([8, 16, 32, 34], fill=(225, 55, 35))
    draw.rectangle([8, 16, 32, 18], fill=(255, 85, 65))
    draw.rectangle([8, 16, 10, 34], fill=(255, 85, 65))
    draw.rectangle([30, 16, 32, 34], fill=(185, 35, 15))
    # Arms
    draw.rectangle([4, 20, 8, 34], fill=(255, 205, 155))
    draw.rectangle([32, 20, 36, 34], fill=(255, 205, 155))
    draw.rectangle([4, 20, 8, 22], fill=(255, 225, 185))
    draw.rectangle([32, 20, 36, 22], fill=(255, 225, 185))
    # Hands
    draw.ellipse([3, 32, 9, 38], fill=(255, 205, 155))
    draw.ellipse([31, 32, 37, 38], fill=(255, 205, 155))
    # Backpack straps
    draw.line([(14, 16), (12, 32)], fill=(45, 45, 45), width=2)
    draw.line([(26, 16), (28, 32)], fill=(45, 45, 45), width=2)
    # Backpack
    draw.rectangle([6, 18, 34, 30], fill=(55, 55, 55))
    draw.rectangle([6, 18, 34, 20], fill=(75, 75, 75))
    draw.rectangle([6, 18, 8, 30], fill=(75, 75, 75))
    draw.rectangle([32, 18, 34, 30], fill=(35, 35, 35))
    # Neck
    draw.rectangle([17, 14, 23, 16], fill=(255, 205, 155))
    # Head
    draw.ellipse([12, 2, 28, 16], fill=(255, 205, 155))
    draw.ellipse([12, 2, 28, 4], fill=(255, 225, 185))
    draw.ellipse([26, 6, 28, 14], fill=(235, 185, 135))
    # Hair
    draw.rectangle([12, 0, 28, 4], fill=(25, 25, 25))
    draw.rectangle([10, 2, 14, 6], fill=(25, 25, 25))
    draw.rectangle([26, 2, 30, 6], fill=(25, 25, 25))
    draw.rectangle([14, 0, 18, 2], fill=(35, 35, 35))
    draw.rectangle([22, 0, 26, 2], fill=(35, 35, 35))
    draw.rectangle([12, 4, 14, 6], fill=(35, 35, 35))
    draw.rectangle([26, 4, 28, 6], fill=(35, 35, 35))
    draw.rectangle([16, 0, 24, 1], fill=(15, 15, 15))
    # Eyes
    draw.ellipse([16, 8, 20, 12], fill=(255, 255, 255))
    draw.ellipse([20, 8, 24, 12], fill=(255, 255, 255))
    draw.ellipse([17, 9, 19, 11], fill=(15, 15, 15))
    draw.ellipse([21, 9, 23, 11], fill=(15, 15, 15))
    draw.point([(18, 10)], fill=(255, 255, 255))
    draw.point([(22, 10)], fill=(255, 255, 255))
    # Mouth
    draw.arc([17, 10, 23, 14], start=0, end=180, fill=(200, 120, 100), width=1)
    # Blush
    draw.ellipse([14, 11, 16, 13], fill=(255, 160, 160))
    draw.ellipse([24, 11, 26, 13], fill=(255, 160, 160))

def draw_summer_player_run1(draw, w, h):
    # Shoes (right leg forward)
    draw.rectangle([18, 52, 26, 58], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([6, 54, 14, 60], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([18, 56, 26, 58], fill=(215, 35, 35))
    draw.rectangle([6, 58, 14, 60], fill=(215, 35, 35))
    # Socks
    draw.rectangle([20, 50, 24, 52], fill=(255, 255, 255))
    draw.rectangle([8, 52, 12, 54], fill=(255, 255, 255))
    # Legs
    draw.rectangle([19, 40, 25, 50], fill=(255, 205, 155))
    draw.rectangle([9, 42, 15, 52], fill=(255, 205, 155))
    # Shorts
    draw.rectangle([10, 32, 30, 44], fill=(55, 85, 185))
    draw.rectangle([10, 32, 30, 34], fill=(85, 115, 215))
    draw.rectangle([10, 32, 12, 44], fill=(85, 115, 215))
    draw.rectangle([28, 32, 30, 44], fill=(35, 65, 155))
    # T-shirt
    draw.rectangle([8, 16, 32, 34], fill=(225, 55, 35))
    draw.rectangle([8, 16, 32, 18], fill=(255, 85, 65))
    draw.rectangle([8, 16, 10, 34], fill=(255, 85, 65))
    draw.rectangle([30, 16, 32, 34], fill=(185, 35, 15))
    # Arms (near back, far forward)
    draw.rectangle([2, 22, 6, 32], fill=(255, 205, 155))
    draw.rectangle([34, 18, 38, 28], fill=(255, 205, 155))
    draw.ellipse([1, 30, 7, 36], fill=(255, 205, 155))
    draw.ellipse([33, 26, 39, 32], fill=(255, 205, 155))
    # Backpack straps
    draw.line([(14, 16), (12, 32)], fill=(45, 45, 45), width=2)
    draw.line([(26, 16), (28, 32)], fill=(45, 45, 45), width=2)
    # Backpack
    draw.rectangle([6, 18, 34, 30], fill=(55, 55, 55))
    draw.rectangle([6, 18, 34, 20], fill=(75, 75, 75))
    draw.rectangle([6, 18, 8, 30], fill=(75, 75, 75))
    draw.rectangle([32, 18, 34, 30], fill=(35, 35, 35))
    # Neck
    draw.rectangle([17, 14, 23, 16], fill=(255, 205, 155))
    # Head
    draw.ellipse([12, 2, 28, 16], fill=(255, 205, 155))
    draw.ellipse([12, 2, 28, 4], fill=(255, 225, 185))
    draw.ellipse([26, 6, 28, 14], fill=(235, 185, 135))
    # Hair
    draw.rectangle([12, 0, 28, 4], fill=(25, 25, 25))
    draw.rectangle([10, 2, 14, 6], fill=(25, 25, 25))
    draw.rectangle([26, 2, 30, 6], fill=(25, 25, 25))
    draw.rectangle([14, 0, 18, 2], fill=(35, 35, 35))
    draw.rectangle([22, 0, 26, 2], fill=(35, 35, 35))
    draw.rectangle([12, 4, 14, 6], fill=(35, 35, 35))
    draw.rectangle([26, 4, 28, 6], fill=(35, 35, 35))
    draw.rectangle([16, 0, 24, 1], fill=(15, 15, 15))
    # Eyes
    draw.ellipse([16, 8, 20, 12], fill=(255, 255, 255))
    draw.ellipse([20, 8, 24, 12], fill=(255, 255, 255))
    draw.ellipse([17, 9, 19, 11], fill=(15, 15, 15))
    draw.ellipse([21, 9, 23, 11], fill=(15, 15, 15))
    draw.point([(18, 10)], fill=(255, 255, 255))
    draw.point([(22, 10)], fill=(255, 255, 255))
    # Mouth
    draw.arc([17, 10, 23, 14], start=0, end=180, fill=(200, 120, 100), width=1)
    # Blush
    draw.ellipse([14, 11, 16, 13], fill=(255, 160, 160))
    draw.ellipse([24, 11, 26, 13], fill=(255, 160, 160))

def draw_summer_player_run2(draw, w, h):
    # Shoes
    draw.rectangle([11, 50, 19, 56], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([21, 50, 29, 56], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([11, 54, 19, 56], fill=(215, 35, 35))
    draw.rectangle([21, 54, 29, 56], fill=(215, 35, 35))
    # Socks
    draw.rectangle([13, 48, 17, 50], fill=(255, 255, 255))
    draw.rectangle([23, 48, 27, 50], fill=(255, 255, 255))
    # Legs
    draw.rectangle([11, 40, 17, 48], fill=(255, 205, 155))
    draw.rectangle([23, 40, 29, 48], fill=(255, 205, 155))
    # Shorts
    draw.rectangle([10, 32, 30, 44], fill=(55, 85, 185))
    draw.rectangle([10, 32, 30, 34], fill=(85, 115, 215))
    draw.rectangle([10, 32, 12, 44], fill=(85, 115, 215))
    draw.rectangle([28, 32, 30, 44], fill=(35, 65, 155))
    # T-shirt
    draw.rectangle([8, 16, 32, 34], fill=(225, 55, 35))
    draw.rectangle([8, 16, 32, 18], fill=(255, 85, 65))
    draw.rectangle([8, 16, 10, 34], fill=(255, 85, 65))
    draw.rectangle([30, 16, 32, 34], fill=(185, 35, 15))
    # Arms
    draw.rectangle([4, 20, 8, 32], fill=(255, 205, 155))
    draw.rectangle([32, 20, 36, 32], fill=(255, 205, 155))
    draw.ellipse([3, 30, 9, 36], fill=(255, 205, 155))
    draw.ellipse([31, 30, 37, 36], fill=(255, 205, 155))
    # Backpack straps
    draw.line([(14, 16), (12, 32)], fill=(45, 45, 45), width=2)
    draw.line([(26, 16), (28, 32)], fill=(45, 45, 45), width=2)
    # Backpack
    draw.rectangle([6, 18, 34, 30], fill=(55, 55, 55))
    draw.rectangle([6, 18, 34, 20], fill=(75, 75, 75))
    draw.rectangle([6, 18, 8, 30], fill=(75, 75, 75))
    draw.rectangle([32, 18, 34, 30], fill=(35, 35, 35))
    # Neck
    draw.rectangle([17, 14, 23, 16], fill=(255, 205, 155))
    # Head
    draw.ellipse([12, 2, 28, 16], fill=(255, 205, 155))
    draw.ellipse([12, 2, 28, 4], fill=(255, 225, 185))
    draw.ellipse([26, 6, 28, 14], fill=(235, 185, 135))
    # Hair
    draw.rectangle([12, 0, 28, 4], fill=(25, 25, 25))
    draw.rectangle([10, 2, 14, 6], fill=(25, 25, 25))
    draw.rectangle([26, 2, 30, 6], fill=(25, 25, 25))
    draw.rectangle([14, 0, 18, 2], fill=(35, 35, 35))
    draw.rectangle([22, 0, 26, 2], fill=(35, 35, 35))
    draw.rectangle([12, 4, 14, 6], fill=(35, 35, 35))
    draw.rectangle([26, 4, 28, 6], fill=(35, 35, 35))
    draw.rectangle([16, 0, 24, 1], fill=(15, 15, 15))
    # Eyes
    draw.ellipse([16, 8, 20, 12], fill=(255, 255, 255))
    draw.ellipse([20, 8, 24, 12], fill=(255, 255, 255))
    draw.ellipse([17, 9, 19, 11], fill=(15, 15, 15))
    draw.ellipse([21, 9, 23, 11], fill=(15, 15, 15))
    draw.point([(18, 10)], fill=(255, 255, 255))
    draw.point([(22, 10)], fill=(255, 255, 255))
    # Mouth
    draw.arc([17, 10, 23, 14], start=0, end=180, fill=(200, 120, 100), width=1)
    # Blush
    draw.ellipse([14, 11, 16, 13], fill=(255, 160, 160))
    draw.ellipse([24, 11, 26, 13], fill=(255, 160, 160))

def draw_summer_player_run3(draw, w, h):
    # Shoes (left leg forward)
    draw.rectangle([6, 54, 14, 60], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([18, 52, 26, 58], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([6, 58, 14, 60], fill=(215, 35, 35))
    draw.rectangle([18, 56, 26, 58], fill=(215, 35, 35))
    # Socks
    draw.rectangle([8, 52, 12, 54], fill=(255, 255, 255))
    draw.rectangle([20, 50, 24, 52], fill=(255, 255, 255))
    # Legs
    draw.rectangle([9, 42, 15, 52], fill=(255, 205, 155))
    draw.rectangle([19, 40, 25, 50], fill=(255, 205, 155))
    # Shorts
    draw.rectangle([10, 32, 30, 44], fill=(55, 85, 185))
    draw.rectangle([10, 32, 30, 34], fill=(85, 115, 215))
    draw.rectangle([10, 32, 12, 44], fill=(85, 115, 215))
    draw.rectangle([28, 32, 30, 44], fill=(35, 65, 155))
    # T-shirt
    draw.rectangle([8, 16, 32, 34], fill=(225, 55, 35))
    draw.rectangle([8, 16, 32, 18], fill=(255, 85, 65))
    draw.rectangle([8, 16, 10, 34], fill=(255, 85, 65))
    draw.rectangle([30, 16, 32, 34], fill=(185, 35, 15))
    # Arms (near forward, far back)
    draw.rectangle([2, 18, 6, 28], fill=(255, 205, 155))
    draw.rectangle([34, 22, 38, 32], fill=(255, 205, 155))
    draw.ellipse([1, 26, 7, 32], fill=(255, 205, 155))
    draw.ellipse([33, 30, 39, 36], fill=(255, 205, 155))
    # Backpack straps
    draw.line([(14, 16), (12, 32)], fill=(45, 45, 45), width=2)
    draw.line([(26, 16), (28, 32)], fill=(45, 45, 45), width=2)
    # Backpack
    draw.rectangle([6, 18, 34, 30], fill=(55, 55, 55))
    draw.rectangle([6, 18, 34, 20], fill=(75, 75, 75))
    draw.rectangle([6, 18, 8, 30], fill=(75, 75, 75))
    draw.rectangle([32, 18, 34, 30], fill=(35, 35, 35))
    # Neck
    draw.rectangle([17, 14, 23, 16], fill=(255, 205, 155))
    # Head
    draw.ellipse([12, 2, 28, 16], fill=(255, 205, 155))
    draw.ellipse([12, 2, 28, 4], fill=(255, 225, 185))
    draw.ellipse([26, 6, 28, 14], fill=(235, 185, 135))
    # Hair
    draw.rectangle([12, 0, 28, 4], fill=(25, 25, 25))
    draw.rectangle([10, 2, 14, 6], fill=(25, 25, 25))
    draw.rectangle([26, 2, 30, 6], fill=(25, 25, 25))
    draw.rectangle([14, 0, 18, 2], fill=(35, 35, 35))
    draw.rectangle([22, 0, 26, 2], fill=(35, 35, 35))
    draw.rectangle([12, 4, 14, 6], fill=(35, 35, 35))
    draw.rectangle([26, 4, 28, 6], fill=(35, 35, 35))
    draw.rectangle([16, 0, 24, 1], fill=(15, 15, 15))
    # Eyes
    draw.ellipse([16, 8, 20, 12], fill=(255, 255, 255))
    draw.ellipse([20, 8, 24, 12], fill=(255, 255, 255))
    draw.ellipse([17, 9, 19, 11], fill=(15, 15, 15))
    draw.ellipse([21, 9, 23, 11], fill=(15, 15, 15))
    draw.point([(18, 10)], fill=(255, 255, 255))
    draw.point([(22, 10)], fill=(255, 255, 255))
    # Mouth
    draw.arc([17, 10, 23, 14], start=0, end=180, fill=(200, 120, 100), width=1)
    # Blush
    draw.ellipse([14, 11, 16, 13], fill=(255, 160, 160))
    draw.ellipse([24, 11, 26, 13], fill=(255, 160, 160))

def draw_summer_player_jump(draw, w, h):
    # Shoes (tucked back)
    draw.rectangle([6, 46, 14, 52], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([18, 44, 26, 50], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([6, 50, 14, 52], fill=(215, 35, 35))
    draw.rectangle([18, 48, 26, 50], fill=(215, 35, 35))
    # Legs (bent back)
    draw.rectangle([9, 38, 15, 46], fill=(255, 205, 155))
    draw.rectangle([21, 36, 27, 44], fill=(255, 205, 155))
    # Shorts
    draw.rectangle([10, 26, 30, 38], fill=(55, 85, 185))
    draw.rectangle([10, 26, 30, 28], fill=(85, 115, 215))
    draw.rectangle([10, 26, 12, 38], fill=(85, 115, 215))
    draw.rectangle([28, 26, 30, 38], fill=(35, 65, 155))
    # T-shirt
    draw.rectangle([8, 12, 32, 28], fill=(225, 55, 35))
    draw.rectangle([8, 12, 32, 14], fill=(255, 85, 65))
    draw.rectangle([8, 12, 10, 28], fill=(255, 85, 65))
    draw.rectangle([30, 12, 32, 28], fill=(185, 35, 15))
    # Arms (raised)
    draw.rectangle([2, 6, 6, 16], fill=(255, 205, 155))
    draw.rectangle([34, 6, 38, 16], fill=(255, 205, 155))
    draw.ellipse([1, 2, 7, 8], fill=(255, 205, 155))
    draw.ellipse([33, 2, 39, 8], fill=(255, 205, 155))
    # Backpack straps
    draw.line([(14, 12), (12, 26)], fill=(45, 45, 45), width=2)
    draw.line([(26, 12), (28, 26)], fill=(45, 45, 45), width=2)
    # Backpack
    draw.rectangle([6, 14, 34, 26], fill=(55, 55, 55))
    draw.rectangle([6, 14, 34, 16], fill=(75, 75, 75))
    draw.rectangle([6, 14, 8, 26], fill=(75, 75, 75))
    draw.rectangle([32, 14, 34, 26], fill=(35, 35, 35))
    # Neck
    draw.rectangle([17, 10, 23, 12], fill=(255, 205, 155))
    # Head
    draw.ellipse([12, 0, 28, 12], fill=(255, 205, 155))
    draw.ellipse([12, 0, 28, 2], fill=(255, 225, 185))
    draw.ellipse([26, 4, 28, 10], fill=(235, 185, 135))
    # Hair
    draw.rectangle([12, 0, 28, 3], fill=(25, 25, 25))
    draw.rectangle([10, 1, 14, 4], fill=(25, 25, 25))
    draw.rectangle([26, 1, 30, 4], fill=(25, 25, 25))
    draw.rectangle([14, 0, 18, 1], fill=(35, 35, 35))
    draw.rectangle([22, 0, 26, 1], fill=(35, 35, 35))
    # Eyes (looking up)
    draw.ellipse([16, 4, 20, 7], fill=(255, 255, 255))
    draw.ellipse([20, 4, 24, 7], fill=(255, 255, 255))
    draw.ellipse([17, 4, 19, 6], fill=(15, 15, 15))
    draw.ellipse([21, 4, 23, 6], fill=(15, 15, 15))
    draw.point([(18, 5)], fill=(255, 255, 255))
    draw.point([(22, 5)], fill=(255, 255, 255))
    # Mouth (open)
    draw.ellipse([19, 7, 21, 9], fill=(200, 100, 100))

def draw_summer_player_crouch(draw, w, h):
    # Shoes
    draw.rectangle([10, 48, 18, 54], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([22, 48, 30, 54], fill=(240, 240, 240), outline=(200, 200, 200), width=1)
    draw.rectangle([10, 52, 18, 54], fill=(215, 35, 35))
    draw.rectangle([22, 52, 30, 54], fill=(215, 35, 35))
    # Legs (bent)
    draw.rectangle([11, 38, 17, 48], fill=(255, 205, 155))
    draw.rectangle([23, 38, 29, 48], fill=(255, 205, 155))
    # Shorts
    draw.rectangle([10, 30, 30, 40], fill=(55, 85, 185))
    draw.rectangle([10, 30, 30, 32], fill=(85, 115, 215))
    draw.rectangle([10, 30, 12, 40], fill=(85, 115, 215))
    draw.rectangle([28, 30, 30, 40], fill=(35, 65, 155))
    # T-shirt
    draw.rectangle([8, 16, 32, 32], fill=(225, 55, 35))
    draw.rectangle([8, 16, 32, 18], fill=(255, 85, 65))
    draw.rectangle([8, 16, 10, 32], fill=(255, 85, 65))
    draw.rectangle([30, 16, 32, 32], fill=(185, 35, 15))
    # Arms (forward)
    draw.rectangle([2, 24, 6, 34], fill=(255, 205, 155))
    draw.rectangle([34, 24, 38, 34], fill=(255, 205, 155))
    draw.ellipse([1, 32, 7, 38], fill=(255, 205, 155))
    draw.ellipse([33, 32, 39, 38], fill=(255, 205, 155))
    # Backpack straps
    draw.line([(14, 16), (12, 30)], fill=(45, 45, 45), width=2)
    draw.line([(26, 16), (28, 30)], fill=(45, 45, 45), width=2)
    # Backpack
    draw.rectangle([6, 18, 34, 28], fill=(55, 55, 55))
    draw.rectangle([6, 18, 34, 20], fill=(75, 75, 75))
    draw.rectangle([6, 18, 8, 28], fill=(75, 75, 75))
    draw.rectangle([32, 18, 34, 28], fill=(35, 35, 35))
    # Neck
    draw.rectangle([17, 14, 23, 16], fill=(255, 205, 155))
    # Head
    draw.ellipse([12, 2, 28, 16], fill=(255, 205, 155))
    draw.ellipse([12, 2, 28, 4], fill=(255, 225, 185))
    draw.ellipse([26, 6, 28, 14], fill=(235, 185, 135))
    # Hair
    draw.rectangle([12, 0, 28, 4], fill=(25, 25, 25))
    draw.rectangle([10, 2, 14, 6], fill=(25, 25, 25))
    draw.rectangle([26, 2, 30, 6], fill=(25, 25, 25))
    draw.rectangle([14, 0, 18, 2], fill=(35, 35, 35))
    draw.rectangle([22, 0, 26, 2], fill=(35, 35, 35))
    draw.rectangle([12, 4, 14, 6], fill=(35, 35, 35))
    draw.rectangle([26, 4, 28, 6], fill=(35, 35, 35))
    draw.rectangle([16, 0, 24, 1], fill=(15, 15, 15))
    # Eyes
    draw.ellipse([16, 8, 20, 12], fill=(255, 255, 255))
    draw.ellipse([20, 8, 24, 12], fill=(255, 255, 255))
    draw.ellipse([17, 9, 19, 11], fill=(15, 15, 15))
    draw.ellipse([21, 9, 23, 11], fill=(15, 15, 15))
    draw.point([(18, 10)], fill=(255, 255, 255))
    draw.point([(22, 10)], fill=(255, 255, 255))
    # Mouth
    draw.arc([17, 10, 23, 14], start=0, end=180, fill=(200, 120, 100), width=1)
    # Blush
    draw.ellipse([14, 11, 16, 13], fill=(255, 160, 160))
    draw.ellipse([24, 11, 26, 13], fill=(255, 160, 160))

# ============== 流浪猫 40x40 ==============
def draw_cat(draw, w, h):
    # Tail
    draw.line([(4, 32), (8, 22), (6, 12), (10, 6)], fill=(235, 140, 50), width=3)
    draw.line([(4, 32), (8, 22), (6, 12), (10, 6)], fill=(255, 170, 80), width=1)
    # Back legs
    draw.rectangle([6, 28, 12, 36], fill=(235, 140, 50))
    draw.rectangle([6, 28, 8, 36], fill=(255, 170, 80))
    draw.rectangle([10, 28, 12, 36], fill=(215, 120, 40))
    # Body
    draw.ellipse([8, 14, 32, 32], fill=(235, 140, 50))
    draw.ellipse([8, 14, 20, 24], fill=(255, 170, 80))
    draw.ellipse([26, 18, 32, 28], fill=(215, 120, 40))
    # Stripes
    draw.line([(14, 16), (18, 20)], fill=(200, 100, 30), width=2)
    draw.line([(20, 16), (24, 20)], fill=(200, 100, 30), width=2)
    draw.line([(16, 22), (20, 26)], fill=(200, 100, 30), width=2)
    # Front legs
    draw.rectangle([24, 26, 30, 36], fill=(235, 140, 50))
    draw.rectangle([24, 26, 26, 36], fill=(255, 170, 80))
    draw.rectangle([28, 26, 30, 36], fill=(215, 120, 40))
    # Paws
    draw.ellipse([5, 34, 13, 40], fill=(255, 200, 160))
    draw.ellipse([23, 34, 31, 40], fill=(255, 200, 160))
    # Head
    draw.ellipse([18, 4, 36, 20], fill=(235, 140, 50))
    draw.ellipse([18, 4, 26, 12], fill=(255, 170, 80))
    draw.ellipse([32, 8, 36, 16], fill=(215, 120, 40))
    # Ears
    draw.polygon([(20, 6), (18, 0), (24, 4)], fill=(235, 140, 50))
    draw.polygon([(20, 6), (18, 0), (22, 4)], fill=(255, 170, 80))
    draw.polygon([(32, 6), (36, 0), (34, 4)], fill=(235, 140, 50))
    draw.polygon([(32, 6), (36, 0), (34, 4)], fill=(255, 170, 80))
    draw.polygon([(19, 2), (21, 0), (23, 2)], fill=(255, 160, 160))
    draw.polygon([(33, 2), (35, 0), (37, 2)], fill=(255, 160, 160))
    # Eyes
    draw.ellipse([22, 8, 26, 12], fill=(255, 255, 255))
    draw.ellipse([28, 8, 32, 12], fill=(255, 255, 255))
    draw.ellipse([23, 9, 25, 11], fill=(10, 10, 10))
    draw.ellipse([29, 9, 31, 11], fill=(10, 10, 10))
    draw.point([(24, 10)], fill=(255, 255, 255))
    draw.point([(30, 10)], fill=(255, 255, 255))
    # Nose
    draw.ellipse([26, 12, 28, 14], fill=(255, 160, 160))
    # Whiskers
    draw.line([(18, 12), (10, 10)], fill=(255, 255, 255), width=1)
    draw.line([(18, 13), (10, 14)], fill=(255, 255, 255), width=1)
    draw.line([(36, 12), (44, 10)], fill=(255, 255, 255), width=1)
    draw.line([(36, 13), (44, 14)], fill=(255, 255, 255), width=1)
    # Mouth
    draw.arc([24, 12, 30, 16], start=0, end=180, fill=(200, 100, 100), width=1)

# ============== 天台平台 40x40 ==============
def draw_rooftop_tile(draw, w, h):
    base = (100, 105, 110)
    hi = (130, 135, 140)
    sh = (75, 80, 85)
    draw.rectangle([0, 0, 40, 40], fill=base)
    draw.rectangle([0, 0, 40, 3], fill=hi)
    draw.rectangle([0, 0, 3, 40], fill=hi)
    draw.rectangle([0, 37, 40, 40], fill=sh)
    draw.rectangle([37, 0, 40, 40], fill=sh)
    # Concrete texture
    for y in range(5, 35, 7):
        for x in range(5, 35, 7):
            if random.random() < 0.4:
                draw.rectangle([x, y, x+2, y+2], fill=(110, 115, 120))
            elif random.random() < 0.3:
                draw.rectangle([x, y, x+2, y+2], fill=(90, 95, 100))
    # Weathering cracks
    draw.line([(10, 15), (18, 18)], fill=(70, 75, 80), width=1)
    draw.line([(25, 8), (28, 16)], fill=(70, 75, 80), width=1)
    draw.line([(8, 28), (16, 30)], fill=(70, 75, 80), width=1)
    # Edge detail
    draw.line([(3, 3), (37, 3)], fill=(140, 145, 150), width=1)
    draw.line([(3, 3), (3, 37)], fill=(140, 145, 150), width=1)

# ============== 背景建筑剪影 60x100 ==============
def draw_building(draw, w, h):
    draw.rectangle([0, 0, w, h], fill=(50, 45, 60))
    draw.rectangle([0, 0, w, 4], fill=(65, 60, 75))
    draw.rectangle([0, 0, 4, h], fill=(65, 60, 75))
    draw.rectangle([0, h-4, w, h], fill=(40, 35, 50))
    draw.rectangle([w-4, 0, w, h], fill=(40, 35, 50))
    # Windows
    for wy in range(10, h-10, 12):
        for wx in range(8, w-8, 10):
            if random.random() < 0.35:
                draw.rectangle([wx, wy, wx+4, wy+6], fill=(255, 220, 120))
                draw.rectangle([wx, wy, wx+4, wy+1], fill=(255, 240, 180))
            else:
                draw.rectangle([wx, wy, wx+4, wy+6], fill=(45, 40, 55))

# ============== 西瓜 30x30 ==============
def draw_watermelon(draw, w, h):
    draw.ellipse([0, 0, 30, 30], fill=(40, 160, 60), outline=(25, 120, 40), width=2)
    draw.ellipse([4, 4, 26, 26], fill=(230, 60, 60))
    draw.ellipse([6, 6, 12, 10], fill=(255, 100, 100))
    for pos in [(10, 10), (18, 12), (12, 18), (20, 20)]:
        draw.ellipse([pos[0], pos[1], pos[0]+2, pos[1]+3], fill=(20, 20, 20))

# ============== 冰棍 20x40 ==============
def draw_ice_cream(draw, w, h):
    draw.rectangle([8, 30, 12, 40], fill=(210, 170, 120))
    draw.rectangle([2, 2, 18, 32], fill=(255, 120, 120), outline=(230, 90, 90), width=2)
    draw.rectangle([2, 8, 18, 12], fill=(255, 200, 100))
    draw.rectangle([2, 18, 18, 22], fill=(100, 200, 255))

# ============== 磁带 30x20 ==============
def draw_tape(draw, w, h):
    draw.rectangle([0, 0, 30, 20], fill=(40, 40, 40), outline=(20, 20, 20), width=2)
    draw.rectangle([2, 2, 28, 18], fill=(60, 60, 60))
    draw.ellipse([6, 6, 12, 14], fill=(20, 20, 20))
    draw.ellipse([18, 6, 24, 14], fill=(20, 20, 20))
    draw.rectangle([8, 2, 22, 8], fill=(255, 255, 255))
    draw.rectangle([8, 2, 22, 3], fill=(220, 220, 220))

# ============== 空调外机 40x30 ==============
def draw_ac_unit(draw, w, h):
    draw.rectangle([0, 0, 40, 30], fill=(200, 200, 205), outline=(170, 170, 175), width=2)
    draw.rectangle([2, 2, 38, 28], fill=(220, 220, 225))
    for y in range(6, 26, 5):
        draw.line([(4, y), (36, y)], fill=(180, 180, 185), width=2)
    for x in range(8, 36, 6):
        draw.line([(x, 6), (x, 24)], fill=(180, 180, 185), width=1)
    draw.rectangle([8, 2, 32, 6], fill=(240, 240, 240))

# ============== 铁栅栏 40x40 ==============
def draw_railing(draw, w, h):
    draw.rectangle([0, 0, 40, 6], fill=(160, 160, 165), outline=(130, 130, 135), width=1)
    for x in [4, 12, 20, 28, 36]:
        draw.rectangle([x-1, 6, x+1, 38], fill=(170, 170, 175), outline=(140, 140, 145), width=1)
    draw.rectangle([0, 36, 40, 40], fill=(160, 160, 165), outline=(130, 130, 135), width=1)

# ============== 晾衣绳 100x12 ==============
def draw_clothesline(draw, w, h):
    # Rope
    draw.line([(0, 2), (w, 2)], fill=(180, 160, 140), width=2)
    draw.line([(0, 1), (w, 1)], fill=(210, 190, 170), width=1)
    # Hanging shirts
    for x in [15, 45, 75]:
        # Body
        draw.rectangle([x, 3, x+10, 10], fill=(255, 120, 120))
        draw.rectangle([x, 3, x+10, 4], fill=(255, 160, 160))
        # Sleeves
        draw.rectangle([x-2, 4, x, 7], fill=(255, 100, 100))
        draw.rectangle([x+10, 4, x+12, 7], fill=(255, 100, 100))
        # Clothespins
        draw.line([(x+2, 2), (x+2, 3)], fill=(255, 255, 255), width=1)
        draw.line([(x+8, 2), (x+8, 3)], fill=(255, 255, 255), width=1)

# ============== 天线杆 20x80 ==============
def draw_antenna(draw, w, h):
    # Pole
    draw.rectangle([8, 0, 12, h], fill=(160, 160, 165))
    draw.rectangle([8, 0, 10, h], fill=(190, 190, 195))
    draw.rectangle([11, 0, 12, h], fill=(130, 130, 135))
    # Crossbars
    for y in [12, 32, 52]:
        draw.line([(2, y), (18, y)], fill=(160, 160, 165), width=2)
        draw.line([(2, y-1), (18, y-1)], fill=(190, 190, 195), width=1)
    # Top tip
    draw.polygon([(10, 0), (6, -6), (14, -6)], fill=(160, 160, 165))

# ============== 飞鸟 20x10 ==============
def draw_bird(draw, w, h):
    draw.polygon([(0, 6), (6, 0), (10, 4)], fill=(60, 55, 70))
    draw.polygon([(10, 4), (14, 0), (20, 6)], fill=(60, 55, 70))
    draw.polygon([(6, 0), (10, 4), (8, 2)], fill=(80, 75, 90))
    draw.polygon([(14, 0), (10, 4), (12, 2)], fill=(80, 75, 90))

# ============== 检查点 30x40 ==============
def draw_checkpoint(draw, w, h):
    # Pole
    draw.rectangle([13, 10, 17, 40], fill=(120, 120, 125))
    draw.rectangle([13, 10, 15, 40], fill=(150, 150, 155))
    # Light box
    draw.rectangle([5, 2, 25, 14], fill=(255, 60, 60))
    draw.rectangle([5, 2, 25, 4], fill=(255, 120, 120))
    draw.rectangle([5, 2, 7, 14], fill=(255, 120, 120))
    draw.rectangle([23, 2, 25, 14], fill=(200, 40, 40))
    # Arrow
    draw.polygon([(10, 5), (16, 8), (10, 11)], fill=(255, 255, 255))
    # Glow
    draw.ellipse([20, 6, 22, 8], fill=(255, 255, 200))

# ============== 水塔 60x100 ==============
def draw_watertower(draw, w, h):
    # Legs
    draw.rectangle([10, 60, 14, 100], fill=(140, 140, 145))
    draw.rectangle([46, 60, 50, 100], fill=(140, 140, 145))
    draw.rectangle([10, 60, 12, 100], fill=(170, 170, 175))
    draw.rectangle([46, 60, 48, 100], fill=(170, 170, 175))
    # Cross braces
    draw.line([(12, 70), (48, 90)], fill=(120, 120, 125), width=2)
    draw.line([(12, 90), (48, 70)], fill=(120, 120, 125), width=2)
    # Tank body
    draw.rectangle([8, 20, 52, 65], fill=(180, 185, 190))
    draw.rectangle([8, 20, 52, 24], fill=(210, 215, 220))
    draw.rectangle([8, 20, 12, 65], fill=(210, 215, 220))
    draw.rectangle([48, 20, 52, 65], fill=(150, 155, 160))
    # Tank top cone
    draw.polygon([(8, 20), (30, 0), (52, 20)], fill=(200, 205, 210))
    draw.polygon([(8, 20), (30, 0), (20, 15)], fill=(230, 235, 240))
    draw.polygon([(30, 0), (52, 20), (40, 15)], fill=(170, 175, 180))
    # Detail lines
    draw.line([(8, 35), (52, 35)], fill=(150, 155, 160), width=1)
    draw.line([(8, 50), (52, 50)], fill=(150, 155, 160), width=1)
    # Ladder
    for y in range(25, 60, 6):
        draw.line([(28, y), (32, y)], fill=(100, 100, 105), width=1)
    draw.line([(30, 25), (30, 60)], fill=(100, 100, 105), width=1)

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
save_img("summer_player_idle.png", 40, 60, draw_summer_player_idle)
save_img("summer_player_run1.png", 40, 60, draw_summer_player_run1)
save_img("summer_player_run2.png", 40, 60, draw_summer_player_run2)
save_img("summer_player_run3.png", 40, 60, draw_summer_player_run3)
save_img("summer_player_jump.png", 40, 60, draw_summer_player_jump)
save_img("summer_player_crouch.png", 40, 60, draw_summer_player_crouch)
save_img("cat.png", 40, 40, draw_cat)
save_img("rooftop_tile.png", 40, 40, draw_rooftop_tile)
save_img("watermelon.png", 30, 30, draw_watermelon)
save_img("ice_cream.png", 20, 40, draw_ice_cream)
save_img("tape.png", 30, 20, draw_tape)
save_img("ac_unit.png", 40, 30, draw_ac_unit)
save_img("railing.png", 40, 40, draw_railing)
save_img("building.png", 60, 100, draw_building)
save_img("clothesline.png", 100, 12, draw_clothesline)
save_img("antenna.png", 20, 80, draw_antenna)
save_img("bird.png", 20, 10, draw_bird)
save_img("checkpoint.png", 30, 40, draw_checkpoint)
save_img("watertower.png", 60, 100, draw_watertower)
print("素材生成完成")
