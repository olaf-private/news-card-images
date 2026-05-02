from PIL import Image, ImageDraw, ImageFont
import textwrap

FONT_BOLD        = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
FONT_REGULAR     = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
FONT_SQUARE_BOLD = "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

BG     = "#fdf8f0"
BOX_BG = "#ffffff"
SUM_BG = "#fff3cd"
BORDER = "#333333"
RED    = "#d92b2b"
BLUE   = "#1a4fc4"
GOLD   = "#c47f00"
GRAY   = "#888888"
YELLOW = "#f5c842"
PINK   = "#fff0f0"
LBLUE  = "#f0f4ff"

W, H = 900, 1200

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

def rect(xy, fill=BOX_BG, outline=BORDER, width=2, radius=14):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def text(s, x, y, fnt, color="#111111", anchor="la"):
    draw.text((x, y), s, font=fnt, fill=color, anchor=anchor)

def hline(y, x0=36, x1=None, color="#cccccc", width=1, dash=False):
    x1 = x1 or W - 36
    if dash:
        seg, gap, cx = 10, 6, x0
        while cx < x1:
            draw.line([(cx, y), (min(cx+seg, x1), y)], fill=color, width=width)
            cx += seg + gap
    else:
        draw.line([(x0, y), (x1, y)], fill=color, width=width)

def sign_color(pct_str):
    return RED if pct_str.startswith("+") else BLUE

f_title = font(FONT_SQUARE_BOLD, 34)
f_mid   = font(FONT_BOLD, 21)
f_body  = font(FONT_REGULAR, 19)
f_small = font(FONT_REGULAR, 16)
f_tag   = font(FONT_BOLD, 16)
f_num   = font(FONT_BOLD, 20)
f_hash  = font(FONT_REGULAR, 15)

# ── 입력 데이터 ────────────────────────────────────────────
DATE      = "02 / May / 26"
HEADLINE  = ["나스닥 25,000 첫 돌파", "· S&P 신고가"]

indices = [
    ("S&P 500",    "7,230.12",  "+0.29%"),
    ("나스닥",     "25,114.44", "+0.89%"),
    ("다우존스",   "49,499.27", "-0.31%"),
    ("Russell 2000","2,812.82", "+0.46%"),
    ("VIX",        "16.99",     "+0.59%"),
    ("WTI 유가",   "$102.53",   "-2.42%"),
    ("금(Gold)",   "$4,622",    "-0.16%"),
]

headlines_right = [
    "Apple 랠리 · M7",
    "서프라이즈 5멘타",
    "사상 최고치 경신",
]

stories = [
    ("Apple 어닝 서프라이즈",
     "Q2 매출 $145B, +3.24%\n아이폰 실적 견인\niPhone17 수요 빅업"),
    ("M7 실적 5개 서프라이즈",
     "Alphabet 순이익+63%\nMeta/MS Q2 Capex 증단\n5기 호조 이후 매수 강화"),
    ("FOMC 금리 동결 Pow",
     "5.5~3.75% 3년 연속 동결\n파월, 1992년 이후 최대\nPCE 3.5% 인플레 둔화"),
]

bigtech = [
    ("Apple",     "+3.24%"), ("Alphabet",  "+10.00%"),
    ("NVIDIA",    "-1.50%"), ("Meta",      "-8.60%"),
    ("Microsoft", "-3.90%"), ("Tesla",     "+0.63%"),
    ("Amazon",    "-1.09%"), ("AMD",       "+10%"),
]

semis = [
    ("NVIDIA",   "-1.50%"), ("AMD",      "+1.71%"),
    ("Qualcomm", "+16.00%"),("Micron",   "+3.20%"),
    ("Intel",    "+2.10%"), ("TSMC ADR", "+0.80%"),
]

SUMMARY = ("Apple·Alphabet 중심 M7 어닝 랠리로 나스닥·S&P500 동반 사상 최고 경신."
           " FOMC 3연속 동결·파월 최고조 발언 금리 인하 기대 자극.")

KEYWORD_TAGS = ["#나스닥신고가", "#SP500신고가", "#애플실적", "#M7실적", "#FOMC동결"]

# ── 제목 ──────────────────────────────────────────────────
for i, line in enumerate(HEADLINE):
    text(line, W//2, 28 + i * 46, f_title, anchor="mt")
text(DATE + "  ·  07:00", W//2, 122, f_body, color=GRAY, anchor="mt")

bx = W//2 + 154
draw.rounded_rectangle([bx, 119, bx+42, 141], radius=8, fill="#fff0e8", outline="#c05000", width=1)
text("US", bx+21, 130, f_small, color="#c05000", anchor="mm")

hline(150, color="#bbbbbb", dash=True)

# ── 지수 테이블 (좌) + 헤드라인 (우) ──────────────────────
rect([36, 162, 480, 400])
text("주요 지수 마감", 56, 178, f_tag, color=GRAY)
for i, (name, val, pct) in enumerate(indices):
    y = 208 + i * 28
    c = sign_color(pct)
    text(name, 56,  y, f_body, color="#222")
    text(val,  260, y, f_body, color="#222")
    text(pct,  430, y+4, font(FONT_BOLD, 17), color=c, anchor="rm")

rect([492, 162, W-36, 400])
for i, line in enumerate(headlines_right):
    text(line, 512, 194 + i * 52, font(FONT_SQUARE_BOLD, 24), color="#111")
text("↓", 512, 350, font(FONT_BOLD, 26), color=GRAY)

# ── 뉴스 스토리 (좌) + 빅테크 등락 (우) ──────────────────
for i, (title, body) in enumerate(stories):
    y0 = 412 + i * 118
    rect([36, y0, 452, y0 + 110])
    text(title, 56, y0 + 14, f_mid)
    for j, line in enumerate(body.split("\n")):
        text(line, 56, y0 + 44 + j * 22, f_small, color="#444")

rect([464, 412, W-36, 652])
text("빅테크 주요 등락", 484, 426, f_tag, color=GRAY)
col_w = (W - 36 - 464) // 2
for i, (name, pct) in enumerate(bigtech):
    row, col = divmod(i, 2)
    x = 484 + col * col_w
    y = 454 + row * 46
    c = sign_color(pct)
    text(name, x, y, f_body, color="#222")
    text(pct, x + col_w - 12, y + 4, font(FONT_BOLD, 17), color=c, anchor="rm")

# ── 반도체 ──────────────────────────────────────────────────
rect([464, 664, W-36, 786])
text("반도체 주요 종목", 484, 678, f_tag, color=GRAY)
col_w2 = (W - 36 - 464) // 2
for i, (name, pct) in enumerate(semis):
    row, col = divmod(i, 2)
    x = 484 + col * col_w2
    y = 706 + row * 36
    c = sign_color(pct)
    text(name, x, y, f_body, color="#222")
    text(pct, x + col_w2 - 12, y + 2, font(FONT_BOLD, 17), color=c, anchor="rm")

# ── 요약 ────────────────────────────────────────────────────
rect([36, 798, W-36, 910], fill=SUM_BG, outline=YELLOW)
text("오늘의 요약", 58, 812, f_tag, color=GRAY)
for i, line in enumerate(textwrap.wrap(SUMMARY, width=52)):
    text(line, 58, 840 + i * 28, f_mid, color="#333")

# ── 해시태그 ────────────────────────────────────────────────
rect([36, 922, W-36, 1052], fill="#f5f5f5", outline="#dddddd", width=1)
hashtags = [
    ["#allround_news", "#미국주식", "#미장", "#나스닥", "#S&P500"],
    ["#미장마감", "#뉴욕증시", "#월스트리트", "#빅테크"],
    KEYWORD_TAGS,
]
for i, tags in enumerate(hashtags):
    text("  ".join(tags), 52, 936 + i * 36, f_hash, color="#777777")

text("@allround_news", W-44, H-14, f_small, color=GRAY, anchor="rb")

img.save("/home/user/news-card-images/us_card_mockup.png")
print("저장 완료: us_card_mockup.png")
