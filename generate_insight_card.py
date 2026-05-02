from PIL import Image, ImageDraw, ImageFont
import textwrap

# ── 폰트 경로 ──────────────────────────────────────────
FONT_BOLD   = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
FONT_SQUARE_BOLD = "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ── 색상 ───────────────────────────────────────────────
BG       = "#fdf8f0"
BOX_BG   = "#ffffff"
KW_BG    = "#fff9e6"
SUM_BG   = "#fff3cd"
BORDER   = "#333333"
RED      = "#d92b2b"
BLUE     = "#1a4fc4"
GOLD     = "#c47f00"
GRAY     = "#888888"
YELLOW   = "#f5c842"

W, H = 900, 1080

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

def rect(xy, fill=BOX_BG, outline=BORDER, width=2, radius=14):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def text(s, x, y, fnt, color="#111111", anchor="la"):
    draw.text((x, y), s, font=fnt, fill=color, anchor=anchor)

def hline(y, x0=36, x1=None, color="#cccccc", width=1, dash=False):
    x1 = x1 or W - 36
    if dash:
        seg, gap = 10, 6
        cx = x0
        while cx < x1:
            draw.line([(cx, y), (min(cx+seg, x1), y)], fill=color, width=width)
            cx += seg + gap
    else:
        draw.line([(x0, y), (x1, y)], fill=color, width=width)

# ── 타이틀 ─────────────────────────────────────────────
f_title  = font(FONT_SQUARE_BOLD, 38)
f_large  = font(FONT_BOLD, 28)
f_mid    = font(FONT_BOLD, 22)
f_body   = font(FONT_REGULAR, 20)
f_small  = font(FONT_REGULAR, 17)
f_tag    = font(FONT_BOLD, 17)
f_num    = font(FONT_BOLD, 22)

# 제목
text("이번 주 한국장 리뷰", W//2, 38, f_title, anchor="mt")
text("03 / May / 26  ·  16:00", W//2, 88, f_body, color=GRAY, anchor="mt")

# KR 뱃지
bx = W//2 + 118
draw.rounded_rectangle([bx, 85, bx+42, 107], radius=8, fill="#e8f4ff", outline=BLUE, width=1)
text("KR", bx+21, 96, f_small, color=BLUE, anchor="mm")

hline(120, color="#bbbbbb", dash=True)

# ── 섹터 박스 (좌/우) ────────────────────────────────────
# 좌: 핫 섹터
rect([36, 132, W//2-8, 380])
text("▶ 주간 핫 섹터", 56, 148, f_mid, color="#d92b2b")

hot = [
    ("방산",    "+8.4%", RED),
    ("조선",    "+5.1%", RED),
    ("바이오",  "+3.7%", RED),
    ("금융",    "+2.9%", RED),
]
for i, (name, pct, color) in enumerate(hot):
    y = 188 + i * 46
    draw.rounded_rectangle([52, y+2, 64, y+20], radius=3, fill=GOLD)
    text(str(i+1), 58, y+11, f_small, color="#fff", anchor="mm")
    text(name, 74, y, f_body, color="#222")
    text(pct + " ↑", W//2 - 20, y+10, f_num, color=color, anchor="rm")

# 우: 콜드 섹터
rect([W//2+8, 132, W-36, 380])
text("▼ 주간 콜드 섹터", W//2+28, 148, f_mid, color="#1a4fc4")

cold = [
    ("반도체",   "-4.2%", BLUE),
    ("2차전지",  "-3.8%", BLUE),
    ("자동차",   "-2.1%", BLUE),
    ("화학",     "-1.6%", BLUE),
]
for i, (name, pct, color) in enumerate(cold):
    y = 188 + i * 46
    x0 = W//2 + 28
    draw.rounded_rectangle([x0-4, y+2, x0+8, y+20], radius=3, fill="#1a4fc4")
    text(str(i+1), x0+2, y+11, f_small, color="#fff", anchor="mm")
    text(name, x0+16, y, f_body, color="#222")
    text(pct + " ↓", W-52, y+10, f_num, color=color, anchor="rm")

# ── 인사이트 키워드 ──────────────────────────────────────
rect([36, 392, W-36, 588], fill=KW_BG, outline=YELLOW)
text("★ 이번 주 키워드", 58, 408, f_mid, color=GOLD)

text("방산 랠리의 이유", 58, 448, font(FONT_SQUARE_BOLD, 30), color=GOLD)

desc_lines = [
    "NATO 국방비 증액 합의 + 국내 방산 수출 계약 연이어 체결.",
    "한화에어로·LIG넥스원 주간 +10% 돌파.",
    "단기 과열 구간 — 추격 매수보다 조정 시 분할 접근 권장.",
]
for i, line in enumerate(desc_lines):
    text(line, 58, 494 + i * 30, f_body, color="#444")

# ── 다음 주 주요 일정 ────────────────────────────────────
rect([36, 600, W-36, 790])
text("■ 다음 주 주요 일정", 58, 616, f_mid)

schedule = [
    ("05 / 06 (화)", "한국 CPI 발표"),
    ("05 / 07 (수)", "삼성전자 주주총회"),
    ("05 / 08 (목)", "외국인 수급 동향 집계"),
    ("05 / 09 (금)", "한국은행 금통위 기준금리 결정 ★"),
]
for i, (date, content) in enumerate(schedule):
    y = 660 + i * 32
    text(date, 58, y, f_small, color=GRAY)
    text(content, 230, y, f_body, color="#111")

# ── 한 줄 요약 ────────────────────────────────────────────
rect([36, 802, W-36, 912], fill=SUM_BG, outline=YELLOW)
text("한 줄 요약", 58, 818, f_tag, color="#888")
summary = "방산·조선 강세, 반도체·2차전지 약세 한 주.\n다음 주 금통위 금리 결정이 코스피 방향성의 분수령."
for i, line in enumerate(summary.split("\n")):
    text(line, 58, 848 + i * 32, f_mid, color="#333")

# ── 해시태그 ─────────────────────────────────────────────
HASH_BG   = "#f5f5f5"
HASH_TEXT = "#777777"
f_hash    = font(FONT_REGULAR, 15)

rect([36, 924, W-36, 1050], fill=HASH_BG, outline="#dddddd", width=1)

hashtags = [
    # 고정
    ["#allround_news", "#주식", "#투자", "#재테크", "#주식투자"],
    # 카드 타입
    ["#주간리뷰", "#섹터분석", "#투자인사이트", "#이번주시장"],
    # 이번 주 키워드
    ["#방산주", "#방산ETF", "#한화에어로스페이스", "#LIG넥스원", "#방산랠리"],
]
for i, tags in enumerate(hashtags):
    text("  ".join(tags), 52, 940 + i * 34, f_hash, color=HASH_TEXT)

# ── 핸들 ─────────────────────────────────────────────────
text("@allround_news", W-44, H-14, f_small, color=GRAY, anchor="rb")

img.save("/home/user/news-card-images/insight_card_mockup.png")
print("저장 완료: insight_card_mockup.png")
