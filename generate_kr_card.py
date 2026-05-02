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
DATE     = "02 / May / 26"
HEADLINE = "코스피 2,620 돌파 · 외국인 순매수 5거래일 연속"

indices = [
    ("코스피",    "2,624.32", "+0.87%"),
    ("코스닥",    "748.15",   "+1.24%"),
    ("원/달러",   "1,362.50", "-0.31%"),
    ("국채 3년",  "2.98%",    "-0.03%"),
    ("국채 10년", "3.24%",    "+0.02%"),
    ("금리(기준)","3.50%",    "-"),
]

headlines_right = [
    "외국인 5일 연속",
    "순매수 · 반도체",
    "주도 랠리 재개",
]

stories = [
    ("외국인 순매수 지속",
     "5거래일 연속 순매수 +1.2조\n반도체·IT 집중 매수\nSK하이닉스 52주 신고가"),
    ("금통위 금리 동결",
     "기준금리 3.50% 유지\n가계부채 우려 반영\n하반기 인하 가능성 시사"),
    ("2차전지 반등 시도",
     "에코프로 +4.2% 급반등\nLG에너지솔루션 +2.8%\n실적 바닥론 부각"),
]

top_stocks = [
    ("삼성전자",     "+1.82%"), ("SK하이닉스",  "+3.47%"),
    ("LG에너지솔루션","+2.80%"),("삼성바이오로직스","+1.20%"),
    ("현대차",       "-0.43%"), ("카카오",       "-1.12%"),
    ("NAVER",        "+0.95%"), ("셀트리온",     "+2.10%"),
]

supply = [
    ("외국인", "+1.24조"),
    ("기관",   "-0.38조"),
    ("개인",   "-0.86조"),
]

SUMMARY = ("외국인 5일 연속 순매수 속 코스피 2,620 돌파. "
           "반도체 주도 상승, 금통위 금리 동결은 예상 부합.")

KEYWORD_TAGS = ["#SK하이닉스신고가", "#코스피2620", "#외국인순매수", "#금통위동결", "#반도체랠리"]

# ── 제목 ──────────────────────────────────────────────────
text(HEADLINE, W//2, 36, f_title, anchor="mt")
text(DATE + "  ·  16:00", W//2, 86, f_body, color=GRAY, anchor="mt")

bx = W//2 + 160
draw.rounded_rectangle([bx, 83, bx+42, 105], radius=8, fill="#e8f4ff", outline=BLUE, width=1)
text("KR", bx+21, 94, f_small, color=BLUE, anchor="mm")

hline(116, color="#bbbbbb", dash=True)

# ── 지수 테이블 (좌) + 헤드라인 (우) ──────────────────────
rect([36, 128, 480, 348])
text("주요 지수 마감", 56, 144, f_tag, color=GRAY)
for i, (name, val, pct) in enumerate(indices):
    y = 174 + i * 28
    c = sign_color(pct) if pct != "-" else GRAY
    text(name, 56,  y, f_body, color="#222")
    text(val,  230, y, f_body, color="#222")
    text(pct,  430, y + 4, font(FONT_BOLD, 17), color=c, anchor="rm")

rect([492, 128, W-36, 348])
for i, line in enumerate(headlines_right):
    text(line, 512, 160 + i * 52, font(FONT_SQUARE_BOLD, 24), color="#111")
text("↓", 512, 308, font(FONT_BOLD, 26), color=GRAY)

# ── 뉴스 스토리 (좌) + 주요 종목 (우) ──────────────────────
for i, (title, body) in enumerate(stories):
    y0 = 360 + i * 118
    rect([36, y0, 452, y0 + 110])
    text(title, 56, y0 + 14, f_mid)
    for j, line in enumerate(body.split("\n")):
        text(line, 56, y0 + 44 + j * 22, f_small, color="#444")

rect([464, 360, W-36, 600])
text("주요 종목 등락", 484, 374, f_tag, color=GRAY)
col_w = (W - 36 - 464) // 2
for i, (name, pct) in enumerate(top_stocks):
    row, col = divmod(i, 2)
    x = 484 + col * col_w
    y = 402 + row * 46
    c = sign_color(pct)
    text(name, x, y, f_small, color="#222")
    text(pct, x + col_w - 12, y + 2, font(FONT_BOLD, 17), color=c, anchor="rm")

# ── 수급 동향 ────────────────────────────────────────────────
rect([464, 612, W-36, 716])
text("수급 동향", 484, 626, f_tag, color=GRAY)
sw = (W - 36 - 464) // 3
for i, (group, val) in enumerate(supply):
    x = 484 + i * sw
    c = sign_color(val)
    text(group, x, 660, f_body, color=GRAY)
    text(val, x, 690, font(FONT_BOLD, 22), color=c)

# ── 요약 ────────────────────────────────────────────────────
rect([36, 728, W-36, 840], fill=SUM_BG, outline=YELLOW)
text("오늘의 요약", 58, 742, f_tag, color=GRAY)
for i, line in enumerate(textwrap.wrap(SUMMARY, width=52)):
    text(line, 58, 770 + i * 28, f_mid, color="#333")

# ── 해시태그 ────────────────────────────────────────────────
rect([36, 852, W-36, 982], fill="#f5f5f5", outline="#dddddd", width=1)
hashtags = [
    ["#allround_news", "#한국주식", "#코스피", "#코스닥", "#국내주식"],
    ["#한국장마감", "#코스피마감", "#코스닥마감", "#국내증시"],
    KEYWORD_TAGS,
]
for i, tags in enumerate(hashtags):
    text("  ".join(tags), 52, 866 + i * 36, f_hash, color="#777777")

text("@allround_news", W-44, H-14, f_small, color=GRAY, anchor="rb")

img.save("/home/user/news-card-images/kr_card_mockup.png")
print("저장 완료: kr_card_mockup.png")
