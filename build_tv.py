"""
JooN's Sushi TV - v8.0 (Food Quotes + Sushi BG / Person Quotes + Portrait BG)
"""
import json, os, re, base64, random
from menu_utils import find_local_image, img_to_base64

MENU_JSON  = "menu.json"
IMAGE_DIR  = "images"
SIG_DIR    = "signature_images"
OUTPUT_HTML= "index.html"
TV2_BASE   = "https://681014la-wq.github.io/joons-tv-2/signature_images/"
TV1_BASE   = "https://681014la-wq.github.io/joons-tv-1/"
VIDEO_FILES= ["video_1.mp4", "video_2.mp4", "video_3.mp4"]
QR_GOOGLE  = "qr_google.png"
QR_YELP    = "qr_yelp.png"

# 음식 관련 태그 (이 태그 → 스시 이미지 배경)
FOOD_TAGS = {"food", "sushi", "chef", "health", "history", "salmon"}

# 인물 초상화 매핑 (본인 전용 이미지)
WHO_TO_BG = {
    # 기존 초상화
    "SOCRATES":           "bg_socrates.png",
    "ARISTOTLE":          "bg_aristotle.png",
    "EINSTEIN":           "bg_einstein.png",
    "HIPPOKRATES":        "bg_hippokrates.png",
    "LAO TZU":            "bg_laotzu.png",
    "CONFUCIUS":          "bg_confucius.png",
    "CONFUCUIUS":         "bg_confucius.png",
    "STEVE JOBS":         "bg_jobs.png",
    "MAHATMA GANDHI":     "bg_gandhi.png",
    "BRUCE LEE":          "bg_brucelee.png",
    "ZEN WISDOM":         "bg_zen.png",
    "DALAI LAMA":         "bg_zen.png",
    "KOREAN PROVERB":     "bg_scholar.png",
    # Canva AI 생성 초상화
    "FRIEDRICH NIETZSCHE": "bg_nietzsche.png",
    "PLATO":              "bg_plato.png",
    "WINSTON CHURCHILL":  "bg_churchill.png",
    "BENJAMIN FRANKLIN":  "bg_franklin.png",
    "MARK TWAIN":         "bg_marktwain.png",
    "PABLO PICASSO":      "bg_picasso.png",
    "LEONARDO DA VINCI":  "bg_davinci.png",
    "MARCUS AURELIUS":    "bg_marcusaurelius.png",
    "HENRY FORD":         "bg_henryford.png",
    "HELEN KELLER":       "bg_helenkeller.png",
    "MAYA ANGELOU":       "bg_mayaangelou.png",
    "RUMI":               "bg_rumi.jpg",
    "RAY DALIO":          "bg_dalio.jpg",
    "SUSHI MASTER":       "bg_sushi_master.png",
    "SHOKUNIN":           "bg_sushi_master.png",
    "CHEF":               "bg_chef.png",
    # 추가 초상화 (10명)
    "ANNE FRANK":         "bg_annefrank.png",
    "SENECA":             "bg_seneca.png",
    "OSCAR WILDE":        "bg_oscarwilde.png",
    "VINCENT VAN GOGH":   "bg_vangogh.png",
    "EPICURUS":           "bg_epicurus.png",
    "WAYNE GRETZKY":      "bg_gretzky.png",
    "NAPOLEON HILL":      "bg_napoleonhill.png",
    "JIM ROHN":           "bg_jimrohn.png",
    "MARIE MODIANO":      "bg_mariemodiano.png",
    "ST. AUGUSTINE":      "bg_staugustine.png",
}

# 인물 초상화 색상
PORTRAIT_COLORS = {
    "bg_socrates.png":     {"accent": "#00FF9D", "atmos": "#0A2F1F"},
    "bg_aristotle.png":    {"accent": "#00E5FF", "atmos": "#0A1A2F"},
    "bg_einstein.png":     {"accent": "#BB86FC", "atmos": "#1A0A2F"},
    "bg_hippokrates.png":  {"accent": "#76FF03", "atmos": "#0F2F0A"},
    "bg_laotzu.png":       {"accent": "#FFD54F", "atmos": "#2F1A0A"},
    "bg_confucius.png":    {"accent": "#FFEA00", "atmos": "#2F2F0A"},
    "bg_jobs.png":         {"accent": "#FFFFFF", "atmos": "#0A0A0A"},
    "bg_gandhi.png":       {"accent": "#FFAB40", "atmos": "#2F1F0A"},
    "bg_brucelee.png":     {"accent": "#FF1744", "atmos": "#2F0A0A"},
    "bg_zen.png":          {"accent": "#B2FF59", "atmos": "#0A1F0F"},
    "bg_scholar.png":      {"accent": "#80D8FF", "atmos": "#0A1F2F"},
    "bg_nietzsche.png":    {"accent": "#FF8A65", "atmos": "#1A0A05"},
    "bg_plato.png":        {"accent": "#FFD54F", "atmos": "#1A1A0A"},
    "bg_churchill.png":    {"accent": "#90CAF9", "atmos": "#0A0F1A"},
    "bg_franklin.png":     {"accent": "#FFB74D", "atmos": "#1A0F05"},
    "bg_marktwain.png":    {"accent": "#BCAAA4", "atmos": "#1A0F0A"},
    "bg_picasso.png":      {"accent": "#CE93D8", "atmos": "#1A0A1A"},
    "bg_davinci.png":      {"accent": "#A1887F", "atmos": "#1A0F0A"},
    "bg_marcusaurelius.png": {"accent": "#FFD700", "atmos": "#1A1A05"},
    "bg_henryford.png":    {"accent": "#B0BEC5", "atmos": "#0A0F1A"},
    "bg_helenkeller.png":  {"accent": "#F48FB1", "atmos": "#1A0A0F"},
    "bg_mayaangelou.png":  {"accent": "#FFB300", "atmos": "#1A0F05"},
    "bg_rumi.jpg":         {"accent": "#FFD54F", "atmos": "#1A0F05"},
    "bg_dalio.jpg":        {"accent": "#8AB1FF", "atmos": "#050A1A"}, # Gemini Nano Style
    "bg_sushi_master.png": {"accent": "#FFD54F", "atmos": "#0A0A0A"},
    "bg_chef.png":         {"accent": "#C9A96E", "atmos": "#0F0F0F"},
    "bg_annefrank.png":    {"accent": "#FFB74D", "atmos": "#1A0F05"},
    "bg_seneca.png":       {"accent": "#CD853F", "atmos": "#1A0A05"},
    "bg_oscarwilde.png":   {"accent": "#CE93D8", "atmos": "#1A0A1A"},
    "bg_vangogh.png":      {"accent": "#FFD700", "atmos": "#0A0F1A"},
    "bg_epicurus.png":     {"accent": "#FFB74D", "atmos": "#1A0F0A"},
    "bg_gretzky.png":      {"accent": "#90CAF9", "atmos": "#0A0A1A"},
    "bg_napoleonhill.png": {"accent": "#FFB74D", "atmos": "#1A0F05"},
    "bg_jimrohn.png":      {"accent": "#FFB300", "atmos": "#1A0F05"},
    "bg_mariemodiano.png": {"accent": "#F48FB1", "atmos": "#1A0A0F"},
    "bg_staugustine.png":  {"accent": "#FFD54F", "atmos": "#1A0F0A"},
}

# 카테고리별 전용 배경 이미지 + 색상
CATEGORY_BG = {
    "history":    {"file": "bg_history.png",    "accent": "#FFB74D", "atmos": "#1A0F05"},
    "science":    {"file": "bg_science.png",    "accent": "#00E5FF", "atmos": "#050A1A"},
    "psychology": {"file": "bg_psychology.png", "accent": "#CE93D8", "atmos": "#0F051A"},
    "economics":  {"file": "bg_dalio.jpg",       "accent": "#8AB1FF", "atmos": "#051A0A"},
}

# 음식 명언 배경 색상 (스시 이미지용 - 따뜻한 골드 톤)
FOOD_ACCENT = {"accent": "#C9A96E", "atmos": "#0A0A0E"}

CAT_COLORS = {
    "APPETIZERS": "#FF4081", "SPECIAL ROLLS": "#FF6E40",
    "SUSHI": "#00E5FF", "SASHIMI": "#76FF03",
    "ENTREE": "#FFEA00",
}

to_b64 = img_to_base64
find_menu_img = find_local_image

# 음식 명언 키워드 → 배경 이미지 매칭
FOOD_KEYWORDS = {
    "sushi":  {"words": ["sushi", "roll", "nori", "born from the sea", "experience"],
               "prefix": "bg_kw_sushi_"},
    "salmon": {"words": ["salmon"],
               "prefix": "bg_kw_salmon_"},
    "chef":   {"words": ["cook", "chef", "craft", "kitchen", "skill", "ingredient",
                         "basics", "balance", "journey", "repeat", "elevate", "transform"],
               "prefix": "bg_kw_chef_"},
    "health": {"words": ["health", "medicine", "body", "moderation", "wealth", "you are what"],
               "prefix": "bg_kw_health_"},
    "food":   {"words": ["food", "eat", "dine", "taste", "flavor", "fresh", "mood",
                         "king", "symphony", "love of food"],
               "prefix": "bg_kw_food_"},
}

def find_keyword_bg(quote_en):
    """명언 텍스트에서 키워드 매칭하여 해당 배경 이미지 반환"""
    en_lower = quote_en.lower()
    for kw, info in FOOD_KEYWORDS.items():
        if any(w in en_lower for w in info["words"]):
            prefix = info["prefix"]
            matches = sorted([f for f in os.listdir(".") if f.startswith(prefix) and f.endswith(".jpg")])
            if matches:
                return matches
    return None


# ─── TV3 promo slides (embedded as native slides, every 5 main slides) ───
TV3_LOGO_URL = "https://681014la-wq.github.io/joons-tv-3/joon_logo.png"

_TV3_SOJU_SVG = (
    '<g stroke="#000" stroke-width="3" stroke-linejoin="round">'
    '<rect x="25" y="2" width="10" height="22" fill="#1A6B33"/>'
    '<path d="M22,24 L38,24 L40,38 L20,38 Z" fill="#1A6B33"/>'
    '<rect x="8" y="38" width="44" height="118" rx="6" fill="#2EA84F"/>'
    '<rect x="10" y="68" width="40" height="44" fill="#FFF"/>'
    '<text x="30" y="98" font-family="Bangers" font-size="20" fill="#E63946" text-anchor="middle">SOJU</text>'
    '</g>'
)

def _tv3_burst_block(title, huge, sub):
    return (
        '<div class="burst">'
        '<svg class="burst-svg" viewBox="-20 -20 340 190" preserveAspectRatio="xMidYMid meet"></svg>'
        '<div class="burst-text">'
        f'<div class="burst-title">{title}</div>'
        f'<div class="burst-huge">{huge}</div>'
        f'<div class="burst-sub">{sub}</div>'
        '</div></div>'
    )

def _tv3_promo_slide(tv3_class, title, huge, sub, with_soju=False):
    soju_html = ""
    if with_soju:
        soju_html = "".join(
            f'<svg class="soju fly{i}" viewBox="0 0 60 160">{_TV3_SOJU_SVG}</svg>'
            for i in range(1, 9)
        )
    return (
        f'<div class="slide tv3-scope {tv3_class}">'
        '<div class="bg-halftone"></div>'
        '<div class="speed-lines"></div>'
        f'{soju_html}'
        '<div class="crazy-banner">BOSS GONE CRAZY!<span class="line2">WHAT IS THIS PRICE?!</span></div>'
        '<div class="real-stamp">FOR<br>REAL?!</div>'
        '<div class="bubble b1"></div><div class="bubble b2"></div>'
        '<div class="bubble b3"></div><div class="bubble b4"></div>'
        + _tv3_burst_block(title, huge, sub) +
        '</div>'
    )

def _tv3_logo_slide():
    return (
        '<div class="slide tv3-scope tv3-logo">'
        '<div class="bg-halftone"></div>'
        f'<img class="joon-img" src="{TV3_LOGO_URL}" alt="JooN\'s Sushi">'
        '</div>'
    )

def make_tv3_promo_pool():
    """6개 TV3 프로모 슬라이드 (cycling pool)"""
    return [
        _tv3_promo_slide("tv3-1", "TV AD!", "50% OFF", "LIMITED TIME"),
        _tv3_promo_slide("tv3-2", "BEER!", "2 FOR 1", "ALL NIGHT"),
        _tv3_logo_slide(),
        _tv3_promo_slide("tv3-3", "SOJU!", "50% OFF", "ICE COLD", with_soju=True),
        _tv3_logo_slide(),
        _tv3_promo_slide("tv3-4", "ALL YOU CAN EAT", "100 ITEMS", "ONE PRICE"),
    ]


def build():
    # 비디오 파일명 리스트 (지연 로드 방식)
    video_src_list = [vf for vf in VIDEO_FILES if os.path.exists(vf)]
    print(f"Video files: {len(video_src_list)}개")

    # 메뉴 로드
    with open(MENU_JSON, "r", encoding="utf-8") as f:
        all_items = json.load(f)
    
    # signature_images에 있는 고화질 파일 목록
    from urllib.parse import quote
    sig_files = {}
    if os.path.exists(SIG_DIR):
        for f in os.listdir(SIG_DIR):
            if f.lower().endswith(".jpg"):
                name_key = os.path.splitext(f)[0].lower()
                sig_files[name_key] = f

    def find_sig_match(name):
        """메뉴 이름에서 Roll/Sushi/Sashimi 등 접미사 제거 후 매칭"""
        n = name.lower()
        if n in sig_files:
            return sig_files[n]
        for suffix in [" roll", " sushi", " sashimi", " plate", " don"]:
            stripped = n.replace(suffix, "").strip()
            if stripped in sig_files:
                return sig_files[stripped]
        return None

    cats = {}
    sig_count = 0
    for item in all_items:
        name = item["name"]
        sig_match = find_sig_match(name)
        if sig_match:
            item["img_src"] = TV2_BASE + quote(sig_match)
            sig_count += 1
        else:
            img_path = find_menu_img(name)
            if img_path:
                item["img_src"] = to_b64(img_path)
            else:
                continue
        cats.setdefault(item["category"].strip(), []).append(item)
    print(f"고화질 URL 매칭: {sig_count}개 / 총 {len(all_items)}개")
    
    # 명언 로드 - 메인 + 하위 폴더 전체
    wisdom_list = []
    wisdom_dir = "wisdom_data"
    # 메인 quotes.json
    main_path = os.path.join(wisdom_dir, "quotes.json")
    if os.path.exists(main_path):
        with open(main_path, "r", encoding="utf-8") as f:
            wisdom_list.extend(json.load(f))
    # 하위 폴더 (history, science, psychology, economics)
    for sub in os.listdir(wisdom_dir):
        sub_path = os.path.join(wisdom_dir, sub, "quotes.json")
        if os.path.isdir(os.path.join(wisdom_dir, sub)) and os.path.exists(sub_path):
            with open(sub_path, "r", encoding="utf-8") as f:
                wisdom_list.extend(json.load(f))
    random.shuffle(wisdom_list)
    print(f"명언 총: {len(wisdom_list)}개")

    # 배경 이미지 풀 확장: 시그니처 고화질 + 기존 배경 + 일반 메뉴 이미지
    sig_bg    = [os.path.join(SIG_DIR, f) for f in os.listdir(SIG_DIR) if f.lower().endswith(".jpg")] if os.path.exists(SIG_DIR) else []
    basic_bg  = sorted([f for f in os.listdir(".") if f.startswith("bg_sushi_") and f.endswith(".jpg")])
    menu_bg   = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.lower().endswith(".jpg")] if os.path.exists(IMAGE_DIR) else []
    
    # 전체 리스트 합치기 (고화질 우선 노출을 위해 순서 조정)
    sushi_bg_images = sig_bg + basic_bg + menu_bg
    random.shuffle(sushi_bg_images)
    
    print(f"배경 이미지 풀 확장 완료: 총 {len(sushi_bg_images)}개 확보")
    
    sushi_bg_idx = 0
    cat_counters = {}
    used_once = set()      # 초상화/카테고리 - 절대 재사용 금지
    used_sushi = set()     # 스시 이미지 - 1사이클 소진 시 리셋

    # 배경 이미지 → URL 참조 (TV1 레포에서 로딩)
    bg_cache = {}
    def get_bg_url(path):
        if path not in bg_cache:
            fname = os.path.basename(path)
            if path.startswith(SIG_DIR):
                bg_cache[path] = TV2_BASE + quote(fname)
            else:
                bg_cache[path] = TV1_BASE + quote(fname)
        return bg_cache[path]

    # QR 이미지 URL
    qr_google_b64 = TV1_BASE + quote(QR_GOOGLE) if os.path.exists(QR_GOOGLE) else ""
    qr_yelp_b64   = TV1_BASE + quote(QR_YELP) if os.path.exists(QR_YELP) else ""

    slides = []
    wisdom_idx = 0
    web_idx = 0

    # 커버 슬라이드
    cover_b64  = TV1_BASE + quote("bg_cover.png")
    title_b64  = TV1_BASE + quote("bg_title.png")
    menu_b64   = TV1_BASE + quote("bg_menu.png")

    slides.append(
        f'<div class="slide slide-title active" data-accent="#C9A96E" data-atmos="#060609"'
        f' style="background-image:url(\'{cover_b64}\');background-size:cover;background-position:center;">'
        '<div class="cover-wrap">'
        '<div class="cover-title">JooN\'s Sushi</div>'
        '<div class="cover-sub">— M E N U —</div>'
        '<div class="cover-line"></div>'
        '<div class="cover-addr">29910 Murrieta Hot Springs Rd L, Murrieta, CA</div>'
        '</div>'
        '</div>'
    )

    # 커버 직후 음식 명언 1개 삽입
    food_quotes = [q for q in wisdom_list if q.get("bg_tag", "") in FOOD_TAGS]
    if food_quotes:
        d = food_quotes[0]
        wisdom_list.remove(d)
        bg_path = sushi_bg_images[sushi_bg_idx % len(sushi_bg_images)]
        sushi_bg_idx += 1
        bg_b64 = get_bg_url(bg_path)
        ac, at = FOOD_ACCENT["accent"], FOOD_ACCENT["atmos"]
        slides.append(
            f'<div class="slide slide-extra" data-accent="{ac}" data-atmos="{at}">'
            f'<div class="extra-left">'
            f'  <div class="zoom-wrap"><div class="zoom-img" style="background-image:url(\'{bg_b64}\')"></div></div>'
            f'  <div class="extra-overlay" style="background:linear-gradient(to right,transparent 55%,{at} 96%)"></div>'
            f'</div>'
            f'<div class="extra-right" style="background:{at}">'
            f'  <div class="extra-content">'
            f'    <div class="extra-who" style="color:{ac};border-color:{ac}55">{d["who"]}</div>'
            f'    <div class="extra-en">{d["en"]}</div>'
            f'    <div class="extra-ko" style="color:{ac}">{d["ko"]}</div>'
            f'  </div>'
            f'</div>'
            f'</div>'
        )

    def make_qr_slide():
        return (
            '<div class="slide slide-qr" data-accent="#C9A96E" data-atmos="#0D0D18">'
            '<div class="qr-content">'
            '<div class="qr-tag">We Value Your Feedback</div>'
            '<div class="qr-title">Thank You for Dining with Us!</div>'
            '<div class="qr-divider"></div>'
            '<div class="qr-tagline">placeholder</div>'
            '<div class="qr-reward">One Free Drink &nbsp;&middot;&nbsp; or 10% Off Your Next Visit</div>'
            '</div>'
            f'<div class="qr-flyer qr-left"><img src="{qr_google_b64}" alt="Google QR"><div class="qr-flyer-label">Google</div></div>'
            f'<div class="qr-flyer qr-right"><img src="{qr_yelp_b64}" alt="Yelp QR"><div class="qr-flyer-label">Yelp</div></div>'
            '</div>'
        )

    qr_interval = 0  # 카테고리 카운터 (2개마다 QR 삽입)

    for cat, items in cats.items():
        accent = CAT_COLORS.get(cat.upper(), "#C9A96E")

        # 카테고리 타이틀 슬라이드 (3초)
        slides.append(
            f'<div class="slide slide-title" data-accent="{accent}" data-atmos="#050810"'
            f' style="background-image:url(\'{title_b64}\');background-size:cover;background-position:center;">'
            f'<div class="cover-wrap">'
            f'<div class="title-cat" style="color:{accent}">{cat}</div>'
            f'<div class="title-sub" style="color:{accent}">✦ {len(items)} Selections ✦</div>'
            f'</div>'
            f'</div>'
        )

        # 메뉴 아이템 (3개씩, 3초)
        for i in range(0, len(items), 3):
            chunk = items[i:i+3]
            cards_html = ""
            for it in chunk:
                cards_html += (
                    f'<div class="card" style="border-color:{accent}55">'
                    f'<div class="card-img"><img src="{it["img_src"]}" alt="{it["name"]}"></div>'
                    f'<div class="card-body">'
                    f'<div class="card-name">{it["name"]}</div>'
                    f'<div class="card-price" style="color:{accent}">{it["price"]}</div>'
                    f'</div></div>'
                )
            slides.append(
                f'<div class="slide slide-menu" data-accent="{accent}" data-atmos="#000000"'
                f' style="background-image:url(\'{menu_b64}\');background-size:cover;background-position:center;">'
                f'<div class="menu-header"><span style="color:{accent}">{cat}</span></div>'
                f'<div class="cards cards-{len(chunk)}">{cards_html}</div>'
                f'</div>'
            )

            # 메뉴 슬라이드 사이에 명언 삽입
            if wisdom_idx < len(wisdom_list):
                d = wisdom_list[wisdom_idx]; wisdom_idx += 1
                who = d.get("who", "").upper()
                tag = d.get("bg_tag", "")

                def pick_sushi_bg():
                    """스시 배경 선택 (소진 시 리셋, 초상화/카테고리는 보호)"""
                    nonlocal sushi_bg_idx
                    for _ in range(len(sushi_bg_images)):
                        path = sushi_bg_images[sushi_bg_idx % len(sushi_bg_images)]
                        sushi_bg_idx += 1
                        if path not in used_sushi:
                            used_sushi.add(path)
                            return path
                    # 스시만 리셋 (초상화/카테고리는 절대 안 건드림)
                    used_sushi.clear()
                    path = sushi_bg_images[sushi_bg_idx % len(sushi_bg_images)]
                    sushi_bg_idx += 1
                    used_sushi.add(path)
                    return path

                if tag in CATEGORY_BG:
                    # 카테고리: 1회만 사용, 이후 스시 로테이션
                    cat_info = CATEGORY_BG[tag]
                    cat_file = cat_info["file"]
                    if cat_file not in used_once and os.path.exists(cat_file):
                        used_once.add(cat_file)
                        bg_b64 = get_bg_url(cat_file)
                    else:
                        bg_b64 = get_bg_url(pick_sushi_bg())
                    col = {"accent": cat_info["accent"], "atmos": cat_info["atmos"]}
                elif tag in FOOD_TAGS:
                    # 음식 명언 → 키워드 매칭 우선
                    kw_imgs = find_keyword_bg(d["en"])
                    picked = False
                    if kw_imgs:
                        for img in kw_imgs:
                            if img not in used_once:
                                used_once.add(img)
                                bg_b64 = get_bg_url(img)
                                picked = True
                                break
                    if not picked:
                        bg_b64 = get_bg_url(pick_sushi_bg())
                    col = FOOD_ACCENT
                else:
                    # 비음식 명언 → 인물 초상화 (1회만 우선 사용)
                    bg_file = None
                    for k, v in WHO_TO_BG.items():
                        if k in who:
                            bg_file = v; break

                    if bg_file and os.path.exists(bg_file) and bg_file not in used_once:
                        used_once.add(bg_file)
                        bg_b64 = get_bg_url(bg_file)
                        col = PORTRAIT_COLORS.get(bg_file, FOOD_ACCENT)
                    else:
                        # ⚠️ 중요: 인물 초상화가 없거나 이미 사용된 경우, 절대 고정 이미지로 '돌려막기' 하지 않음
                        # 120장 이상의 고화질 스시 사진 풀에서 순차적으로 하나씩 꺼내어 중복 없이 배치
                        bg_b64 = get_bg_url(pick_sushi_bg())
                        col = FOOD_ACCENT

                ac = col["accent"]
                at = col["atmos"]

                slides.append(
                    f'<div class="slide slide-extra" data-accent="{ac}" data-atmos="{at}">'
                    f'<div class="extra-left">'
                    f'  <div class="zoom-wrap"><div class="zoom-img" style="background-image:url(\'{bg_b64}\')"></div></div>'
                    f'  <div class="extra-overlay" style="background:linear-gradient(to right,transparent 55%,{at} 96%)"></div>'
                    f'</div>'
                    f'<div class="extra-right" style="background:{at}">'
                    f'  <div class="extra-content">'
                    f'    <div class="extra-who" style="color:{ac};border-color:{ac}55">{d["who"]}</div>'
                    f'    <div class="extra-en">{d["en"]}</div>'
                    f'    <div class="extra-ko" style="color:{ac}">{d["ko"]}</div>'
                    f'  </div>'
                    f'</div>'
                    f'</div>'
                )

        # 카테고리 2개마다 QR 슬라이드 삽입
        qr_interval += 1
        if qr_interval % 2 == 0 and qr_google_b64:
            slides.append(make_qr_slide())

    # 마지막에도 QR 슬라이드 추가
    if qr_google_b64:
        slides.append(make_qr_slide())

    # 비디오: 1번은 커버 바로 다음, 나머지는 중간중간 균등 배치 (2회 반복 = 6개)
    if video_src_list:
        video_slides = []
        for vsrc in (video_src_list * 2):
            video_slides.append(
                f'<div class="slide slide-video" data-accent="#C9A96E" data-atmos="#000000" data-video="{vsrc}">'
                f'</div>'
            )
        # 첫 번째: 커버(index 0) 바로 다음
        slides.insert(1, video_slides[0])
        # 나머지: 균등 배치
        rest = video_slides[1:]
        if rest:
            gap = (len(slides) - 2) // (len(rest) + 1)
            for idx, vs in enumerate(rest):
                pos = 2 + gap * (idx + 1) + idx
                slides.insert(pos, vs)

    # TV3 promo 슬라이드: 5장마다 1장씩 cycling
    tv3_pool = make_tv3_promo_pool()
    new_slides = []
    tv3_idx = 0
    for i, s in enumerate(slides):
        new_slides.append(s)
        if (i + 1) % 5 == 0:
            new_slides.append(tv3_pool[tv3_idx % len(tv3_pool)])
            tv3_idx += 1
    slides = new_slides

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JooN's Sushi Menu</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Cormorant+Garamond:wght@700&family=Inter:wght@300;400&family=Bangers&family=Luckiest+Guy&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{width:100vw;height:100vh;overflow:hidden;background:#060609;color:#F0EDE6;font-family:'Inter',sans-serif;cursor:none;}
.slideshow{position:relative;width:100vw;height:100vh;}
.slide{position:absolute;inset:0;opacity:0;transition:opacity 1.2s ease;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.slide.active{opacity:1;z-index:10;}

/* 커버 & 타이틀 */
.cover-wrap{text-align:center;}
.cover-title{font-family:'Playfair Display';font-size:clamp(50px,8vw,110px);letter-spacing:clamp(2px,0.5vw,8px);color:#C9A96E;}
.cover-sub{font-size:22px;letter-spacing:18px;color:#C9A96E;opacity:0.8;margin-top:20px;margin-bottom:30px;}
.cover-line{width:250px;height:1px;background:rgba(201,169,110,0.5);margin:0 auto 30px auto;}
.cover-addr{font-size:15px;letter-spacing:5px;color:#C9A96E;font-weight:300;}
.title-cat{font-family:'Cormorant Garamond';font-size:clamp(24px,3.5vw,48px);letter-spacing:clamp(3px,0.8vw,10px);text-transform:uppercase;white-space:nowrap;text-shadow:0 0 40px rgba(0,0,0,0.9),0 0 80px rgba(0,0,0,0.7);}
.title-sub{font-size:22px;letter-spacing:12px;margin-top:20px;border-top:1.5px solid;padding-top:20px;text-shadow:0 0 20px rgba(0,0,0,0.8);}
.slide-title{background:#050810;}

/* 메뉴 카드 - TV overscan safe area (5% 여백) */
.slide-menu{background:#000;justify-content:flex-start;padding:4vh 5vw 4vh 5vw;}
.menu-header{font-family:'Cormorant Garamond';font-size:clamp(28px,3.5vmin,48px);letter-spacing:10px;text-transform:uppercase;margin-bottom:2.5vh;text-align:center;}
.cards{display:flex;gap:2.5vw;justify-content:center;padding:0;}
.card{border:1px solid;border-radius:18px;overflow:hidden;background:rgba(8,8,16,0.95);display:flex;flex-direction:column;}
.cards-1 .card{width:35vw;height:80vh;}
.cards-2 .card{width:30vw;height:78vh;}
.cards-3 .card{width:26vw;height:76vh;}
.card-img{flex:1;overflow:hidden;min-height:0;}
.card-img img{width:100%;height:100%;object-fit:cover;}
.card-body{padding:2vh 1.5vw;text-align:center;flex-shrink:0;}
.card-name{font-size:clamp(16px,2.2vmin,26px);font-weight:400;margin-bottom:0.8vh;}
.card-price{font-size:clamp(22px,2.8vmin,34px);font-weight:800;}

/* 명언 슬라이드 - 50:50 + Ken Burns 줌 */
.slide-extra{flex-direction:row;align-items:stretch;}
.extra-left{flex:1;position:relative;overflow:hidden;}
.zoom-wrap{position:absolute;inset:-20px;}
@keyframes kenBurns{
  0%{transform:scale(1);}
  100%{transform:scale(1.18);}
}
.zoom-img{width:100%;height:100%;background-size:cover;background-position:center;}
.slide.active .zoom-img{animation:kenBurns 18s ease-in-out forwards;}
.extra-overlay{position:absolute;inset:0;z-index:2;}
.extra-right{flex:1;display:flex;align-items:center;justify-content:center;padding:80px;z-index:5;}
.extra-content{text-align:center;}

@keyframes fadeUp{from{opacity:0;transform:translateY(30px);}to{opacity:1;transform:translateY(0);}}
.extra-who{font-size:19px;letter-spacing:14px;font-weight:800;border-bottom:2px solid;padding-bottom:12px;display:inline-block;margin-bottom:38px;opacity:0;}
.extra-en{font-family:'Playfair Display';font-size:46px;text-transform:uppercase;line-height:1.2;margin-bottom:32px;opacity:0;}
.extra-ko{font-size:26px;font-weight:300;letter-spacing:2px;opacity:0;}
.slide.active .extra-who{animation:fadeUp 1s ease 0.5s forwards;}
.slide.active .extra-en{animation:fadeUp 1.2s ease 0.9s forwards;}
.slide.active .extra-ko{animation:fadeUp 1.2s ease 1.3s forwards;}

/* 비디오 슬라이드 */
.slide-video{background:#000;justify-content:center;align-items:center;overflow:hidden;}
.slide-video .vid{max-width:85vw;max-height:85vh;width:auto;height:auto;object-fit:contain;display:block;margin:auto;}

/* QR 리뷰 슬라이드 */
.slide-qr{
  background:radial-gradient(ellipse at 50% 40%,#0D0D18 0%,#000 100%);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center;overflow:hidden;
}
.qr-content{position:relative;z-index:20;display:flex;flex-direction:column;align-items:center;}
.qr-tag{font-size:11px;letter-spacing:18px;color:#C9A96E;margin-bottom:20px;text-transform:uppercase;opacity:0;}
.qr-title{font-family:'Playfair Display';font-size:clamp(40px,5.5vw,74px);color:#fff;margin-bottom:14px;opacity:0;}
.qr-divider{width:220px;height:1px;background:linear-gradient(90deg,transparent,#C9A96E,transparent);margin:22px auto;opacity:0;}
.qr-tagline{
  font-size:clamp(28px,3.4vw,50px);color:rgba(240,237,230,0.92);
  line-height:1.55;margin-bottom:22px;max-width:900px;
  font-style:italic;font-family:'Cormorant Garamond','Playfair Display',serif;
  text-shadow:0 2px 20px rgba(0,0,0,0.8);opacity:0;
}
.qr-reward{font-family:'Playfair Display';font-size:clamp(17px,2.1vw,28px);color:#C9A96E;opacity:0;}
.qr-flyer{
  position:absolute;background:#fff;border-radius:16px;padding:14px;
  width:clamp(130px,13vw,190px);
  display:flex;flex-direction:column;align-items:center;gap:8px;
  box-shadow:0 8px 40px rgba(0,0,0,0.7);z-index:5;
  opacity:0;transition:opacity .6s ease;pointer-events:none;
}
.qr-left{left:3vw;top:50%;transform:translateY(-50%);}
.qr-right{right:3vw;bottom:8vh;}
.qr-flyer img{width:100%;display:block;border-radius:4px;}
.qr-flyer-label{font-size:10px;letter-spacing:4px;color:#555;text-transform:uppercase;font-family:'Inter',sans-serif;}
.slide-qr.active .qr-flyer{opacity:1;}
.slide.active .qr-tag{animation:fadeUp .8s ease .2s both;}
.slide.active .qr-title{animation:fadeUp 1s ease .4s both;}
.slide.active .qr-divider{animation:fadeUp .7s ease .7s both;}
.slide.active .qr-tagline{animation:fadeUp .8s ease .9s both;}
.slide.active .qr-reward{animation:fadeUp .8s ease 1.1s both;}

/* ==================== TV3 PROMO SLIDES (scoped via .tv3-scope) ==================== */
.tv3-scope{font-family:'Bangers',cursive;gap:24px;}
.tv3-scope .bg-halftone{position:absolute;inset:0;background-image:radial-gradient(circle,#222 1.5px,transparent 1.6px),radial-gradient(circle,#222 1.5px,transparent 1.6px);background-size:18px 18px,18px 18px;background-position:0 0,9px 9px;opacity:0.18;}
.tv3-scope .speed-lines{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 50% 50%,transparent 0deg,rgba(0,0,0,0.55) 0.6deg,transparent 1.2deg,transparent 6deg);mask-image:radial-gradient(circle at center,transparent 25%,#000 55%,transparent 90%);-webkit-mask-image:radial-gradient(circle at center,transparent 25%,#000 55%,transparent 90%);animation:tv3spin 14s linear infinite;}
@keyframes tv3spin{to{transform:rotate(360deg);}}
.tv3-scope .burst{position:relative;width:min(44vw,700px);aspect-ratio:2/1;display:flex;align-items:center;justify-content:center;flex-direction:column;animation:tv3bounce 0.55s cubic-bezier(.34,1.8,.64,1) infinite alternate;}
.tv3-scope .burst svg{position:absolute;inset:0;width:100%;height:100%;filter:drop-shadow(8px 10px 0 #000);}
.tv3-scope .burst-text{position:relative;z-index:5;text-align:center;line-height:0.95;}
@keyframes tv3bounce{from{transform:scale(0.94) rotate(-3deg);}to{transform:scale(1.06) rotate(3deg);}}
.tv3-scope .burst-title{font-family:'Luckiest Guy',cursive;font-size:clamp(40px,7vmin,110px);color:#FFF;text-shadow:-5px -5px 0 #000,5px -5px 0 #000,-5px 5px 0 #000,5px 5px 0 #000,-5px 0 0 #000,5px 0 0 #000,0 -5px 0 #000,0 5px 0 #000,12px 12px 0 #000;letter-spacing:4px;transform:rotate(-4deg);}
.tv3-scope .burst-huge{font-family:'Luckiest Guy',cursive;font-size:clamp(80px,14vmin,220px);color:#FFEB3B;text-shadow:-7px -7px 0 #000,7px -7px 0 #000,-7px 7px 0 #000,7px 7px 0 #000,-7px 0 0 #000,7px 0 0 #000,0 -7px 0 #000,0 7px 0 #000,14px 14px 0 #000;margin-top:10px;transform:rotate(2deg);}
.tv3-scope .burst-sub{display:inline-block;font-family:'Luckiest Guy',cursive;font-size:clamp(16px,2.2vmin,34px);color:#000;background:#FFEB3B;padding:6px 20px;border:4px solid #000;border-radius:28px;letter-spacing:3px;transform:rotate(-2deg);margin-top:18px;box-shadow:5px 5px 0 #000;}
.tv3-scope.tv3-1{background:#FFD93D;}
.tv3-scope.tv3-1 .burst svg .burst-fill{fill:#E63946;}
.tv3-scope.tv3-2{background:#FFF;}
.tv3-scope.tv3-2 .burst svg .burst-fill{fill:#1D9BF0;}
.tv3-scope.tv3-2 .burst-title{color:#E63946;font-size:clamp(56px,10vmin,160px);}
.tv3-scope.tv3-3{background:#0F2E1D;}
.tv3-scope.tv3-3 .bg-halftone{opacity:0.30;}
.tv3-scope.tv3-3 .burst svg .burst-fill{fill:#2EA84F;}
.tv3-scope.tv3-3 .burst-title{color:#1D9BF0;font-size:clamp(56px,10vmin,160px);}
.tv3-scope.tv3-3 .burst-huge{color:#E63946;}
.tv3-scope.tv3-4{background:#1a1a1a;}
.tv3-scope.tv3-4 .bg-halftone{opacity:0.25;background-image:radial-gradient(circle,#FFEB3B 1.5px,transparent 1.6px),radial-gradient(circle,#FFEB3B 1.5px,transparent 1.6px);}
.tv3-scope.tv3-4 .burst svg .burst-fill{fill:#FF6B00;}
.tv3-scope.tv3-4 .burst-title{color:#FFF;text-shadow:6px 6px 0 #000,8px 8px 0 #C70000;}
.tv3-scope.tv3-4 .burst-huge{color:#FFEB3B;text-shadow:7px 7px 0 #000,10px 10px 0 #C70000;}
.tv3-scope.tv3-logo{background:#FFF;}
.tv3-scope.tv3-logo .bg-halftone{opacity:0.10;}
.tv3-scope.tv3-logo .joon-img{position:relative;z-index:5;max-width:80vw;max-height:75vh;width:auto;height:auto;mix-blend-mode:multiply;animation:tv3logoBounce 2s ease-in-out infinite alternate;}
@keyframes tv3logoBounce{from{transform:scale(0.97) rotate(-1deg);}to{transform:scale(1.03) rotate(1deg);}}
.tv3-scope .sushi-roll{position:absolute;width:clamp(70px,10vmin,150px);z-index:50;pointer-events:none;filter:drop-shadow(5px 7px 0 #000);top:0;left:0;}
.tv3-scope .sushi-roll svg{width:100%;height:auto;display:block;}
.tv3-scope .sushi-roll.sf1{animation:tv3sfly1 7s linear infinite;}
.tv3-scope .sushi-roll.sf2{animation:tv3sfly2 8s linear infinite;animation-delay:-2s;}
.tv3-scope .sushi-roll.sf3{animation:tv3sfly3 6.5s linear infinite;animation-delay:-4s;}
.tv3-scope .sushi-roll.sf4{animation:tv3sfly4 7.5s linear infinite;animation-delay:-1.5s;}
.tv3-scope .sushi-roll.sf5{animation:tv3sfly5 8.5s linear infinite;animation-delay:-3s;}
.tv3-scope .sushi-roll.sf6{animation:tv3sfly6 6s linear infinite;animation-delay:-5s;}
.tv3-scope .sushi-roll.sf7{animation:tv3sfly7 7.2s linear infinite;animation-delay:-2.5s;}
.tv3-scope .sushi-roll.sf8{animation:tv3sfly8 8.2s linear infinite;animation-delay:-4.5s;}
.tv3-scope .sushi-roll.sf9{animation:tv3sfly1 7.8s linear infinite;animation-delay:-3.5s;}
.tv3-scope .sushi-roll.sf10{animation:tv3sfly3 7.3s linear infinite;animation-delay:-1s;}
@keyframes tv3sfly1{0%{transform:translate(-15vw,80vh) rotate(0deg);}100%{transform:translate(115vw,-15vh) rotate(540deg);}}
@keyframes tv3sfly2{0%{transform:translate(115vw,75vh) rotate(0deg);}100%{transform:translate(-18vw,-12vh) rotate(-720deg);}}
@keyframes tv3sfly3{0%{transform:translate(-12vw,-15vh) rotate(0deg) scale(0.8);}100%{transform:translate(115vw,90vh) rotate(720deg) scale(0.8);}}
@keyframes tv3sfly4{0%{transform:translate(110vw,15vh) rotate(0deg) scale(1.1);}100%{transform:translate(-15vw,80vh) rotate(-540deg) scale(1.1);}}
@keyframes tv3sfly5{0%{transform:translate(40vw,108vh) rotate(0deg);}100%{transform:translate(60vw,-15vh) rotate(900deg);}}
@keyframes tv3sfly6{0%{transform:translate(-15vw,40vh) rotate(0deg) scale(0.9);}100%{transform:translate(115vw,55vh) rotate(720deg) scale(0.9);}}
@keyframes tv3sfly7{0%{transform:translate(50vw,-15vh) rotate(0deg) scale(0.85);}100%{transform:translate(20vw,108vh) rotate(-720deg) scale(0.85);}}
@keyframes tv3sfly8{0%{transform:translate(-15vw,55vh) rotate(0deg) scale(1.05);}100%{transform:translate(115vw,30vh) rotate(540deg) scale(1.05);}}
.tv3-scope .soju{position:absolute;width:60px;height:160px;z-index:6;pointer-events:none;filter:drop-shadow(4px 6px 0 #000);}
.tv3-scope .soju.fly1{animation:tv3fly1 5s linear infinite;}
.tv3-scope .soju.fly2{animation:tv3fly2 6s linear infinite;animation-delay:-1.5s;}
.tv3-scope .soju.fly3{animation:tv3fly3 7s linear infinite;animation-delay:-3s;}
.tv3-scope .soju.fly4{animation:tv3fly4 5.5s linear infinite;animation-delay:-2s;}
.tv3-scope .soju.fly5{animation:tv3fly5 6.5s linear infinite;animation-delay:-4s;}
.tv3-scope .soju.fly6{animation:tv3fly6 4.8s linear infinite;animation-delay:-1s;}
.tv3-scope .soju.fly7{animation:tv3fly7 7.5s linear infinite;animation-delay:-3.5s;}
.tv3-scope .soju.fly8{animation:tv3fly8 5.8s linear infinite;animation-delay:-0.5s;}
@keyframes tv3fly1{0%{transform:translate(-15vw,90vh) rotate(0deg);}100%{transform:translate(110vw,-20vh) rotate(720deg);}}
@keyframes tv3fly2{0%{transform:translate(115vw,80vh) rotate(0deg);}100%{transform:translate(-20vw,-15vh) rotate(-540deg);}}
@keyframes tv3fly3{0%{transform:translate(-10vw,-20vh) rotate(0deg);}100%{transform:translate(108vw,95vh) rotate(900deg);}}
@keyframes tv3fly4{0%{transform:translate(50vw,110vh) rotate(0deg) scale(0.7);}100%{transform:translate(50vw,-25vh) rotate(720deg) scale(0.7);}}
@keyframes tv3fly5{0%{transform:translate(-15vw,40vh) rotate(0deg) scale(1.2);}100%{transform:translate(115vw,55vh) rotate(540deg) scale(1.2);}}
@keyframes tv3fly6{0%{transform:translate(20vw,-20vh) rotate(0deg) scale(0.85);}100%{transform:translate(85vw,110vh) rotate(-720deg) scale(0.85);}}
@keyframes tv3fly7{0%{transform:translate(110vw,30vh) rotate(0deg);}100%{transform:translate(-20vw,75vh) rotate(-900deg);}}
@keyframes tv3fly8{0%{transform:translate(70vw,115vh) rotate(0deg) scale(0.9);}100%{transform:translate(15vw,-25vh) rotate(540deg) scale(0.9);}}
.tv3-scope .bubble{position:absolute;width:clamp(110px,16vmin,220px);z-index:5;animation:tv3floaty 2.4s ease-in-out infinite;pointer-events:none;}
.tv3-scope .bubble svg{width:100%;height:auto;display:block;filter:drop-shadow(5px 7px 0 #000);}
.tv3-scope .bubble-text{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-5deg);font-family:'Luckiest Guy',cursive;font-size:clamp(15px,2.2vmin,34px);text-align:center;line-height:1;letter-spacing:1px;white-space:nowrap;text-shadow:-1px -1px 0 #000,1px -1px 0 #000,-1px 1px 0 #000,1px 1px 0 #000;}
@keyframes tv3floaty{0%,100%{transform:translateY(0) rotate(-6deg);}50%{transform:translateY(-14px) rotate(6deg);}}
.tv3-scope .bubble.b1{top:11%;left:11%;animation-delay:0s;}
.tv3-scope .bubble.b2{top:13%;right:11%;animation-delay:0.4s;}
.tv3-scope .bubble.b3{bottom:16%;left:12%;animation-delay:0.8s;}
.tv3-scope .bubble.b4{bottom:13%;right:11%;animation-delay:0.2s;}
.tv3-scope .crazy-banner{position:relative;transform:rotate(-3deg);font-family:'Luckiest Guy',cursive;font-size:clamp(28px,4vmin,64px);color:#FFF;background:#E63946;padding:14px 38px;border:5px solid #000;border-radius:14px;text-shadow:-3px -3px 0 #000,3px -3px 0 #000,-3px 3px 0 #000,3px 3px 0 #000,-3px 0 0 #000,3px 0 0 #000,0 -3px 0 #000,0 3px 0 #000;box-shadow:8px 8px 0 #000;letter-spacing:3px;z-index:20;text-align:center;line-height:1.1;animation:tv3wiggle 1.2s ease-in-out infinite alternate;}
.tv3-scope .crazy-banner .line2{display:block;font-size:0.55em;color:#FFEB3B;text-shadow:-2px -2px 0 #000,2px -2px 0 #000,-2px 2px 0 #000,2px 2px 0 #000,-2px 0 0 #000,2px 0 0 #000,0 -2px 0 #000,0 2px 0 #000;margin-top:8px;}
@keyframes tv3wiggle{from{transform:rotate(-4deg) scale(0.97);}to{transform:rotate(-1deg) scale(1.03);}}
.tv3-scope .real-stamp{position:absolute;top:18%;right:5%;z-index:20;width:clamp(110px,13vmin,180px);height:clamp(110px,13vmin,180px);display:flex;align-items:center;justify-content:center;border:5px solid #000;border-radius:50%;background:#FFEB3B;transform:rotate(15deg);box-shadow:5px 5px 0 #000;animation:tv3stamp 0.9s ease-in-out infinite alternate;font-family:'Luckiest Guy',cursive;font-size:clamp(20px,2.6vmin,40px);color:#E63946;text-align:center;line-height:1;letter-spacing:2px;text-shadow:-2px -2px 0 #000,2px -2px 0 #000,-2px 2px 0 #000,2px 2px 0 #000,-2px 0 0 #000,2px 0 0 #000,0 -2px 0 #000,0 2px 0 #000;}
@keyframes tv3stamp{from{transform:rotate(12deg) scale(0.95);}to{transform:rotate(18deg) scale(1.08);}}

</style>
</head>
<body>
<div class="slideshow" id="ss">''' + "".join(slides) + '''</div>
<script>
const slides=document.querySelectorAll('.slide');
let cur=0, t0=Date.now(), paused=false, videoPlaying=false;

function cleanupVideo(slide){
  const v=slide.querySelector('video');
  if(v){v.pause();v.removeAttribute('src');v.load();v.remove();}
}

function prefetchNextVideo(){
  for(let i=1;i<slides.length;i++){
    const next=slides[(cur+i)%slides.length];
    const vsrc=next.dataset.video;
    if(vsrc){fetch(vsrc,{cache:'force-cache'}).catch(()=>{});break;}
  }
}

function show(i){
  // 이전 비디오 제거 (메모리 해제)
  cleanupVideo(slides[cur]);
  videoPlaying=false;

  slides[cur].classList.remove('active');
  cur=(i+slides.length)%slides.length;
  slides[cur].classList.add('active');
  const s=slides[cur];
  document.body.style.background=s.dataset.atmos||'#060609';
  t0=Date.now();

  prefetchNextVideo();

  // 비디오 슬라이드면 지연 로드 후 재생
  const vsrc=s.dataset.video;
  if(vsrc){
    videoPlaying=true;
    const v=document.createElement('video');
    v.className='vid';
    v.muted=true;v.playsInline=true;v.preload='auto';
    v.addEventListener('ended',()=>{cleanupVideo(s);videoPlaying=false;show(cur+1);});
    v.addEventListener('error',()=>{cleanupVideo(s);videoPlaying=false;t0=Date.now();});
    s.appendChild(v);
    v.src=vsrc;
    v.play().catch(()=>{cleanupVideo(s);videoPlaying=false;t0=Date.now();});
  }
}
function tick(){
  if(!paused && !videoPlaying){
    const s=slides[cur];
    const fast=s.classList.contains('slide-title')||s.classList.contains('slide-menu');
    const dur=fast?3000:10000;
    const pct=Math.min((Date.now()-t0)/dur*100,100);
    if(pct>=100)show(cur+1);
  }
  requestAnimationFrame(tick);
}
document.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight')show(cur+1);
  else if(e.key==='ArrowLeft')show(cur-1);
  else if(e.key===' '){
      paused = !paused;
      if(!paused) t0 = Date.now();
  }
  else if(e.key==='f'||e.key==='F'){
      if(!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
  }
});
document.addEventListener('click',()=>show(cur+1));

const QR_TAGLINES = [
  "You chose us for your evening. We will never forget that.",
  "Thank you for letting us be part of your story tonight.",
  "Every guest who walks through our door is a gift.",
  "Tonight meant everything to us. Thank you for being here.",
  "You didn't just dine with us \\u2014 you made our day.",
  "We are grateful for every moment you spent with us.",
  "Your presence at our table is the highest honor we know.",
  "From our kitchen to your heart \\u2014 thank you.",
  "You trusted us with your evening. We don't take that lightly.",
  "Tonight, you were not just a guest. You were family.",
  "Every roll was made with love \\u2014 your words help us share that love further.",
  "We didn't just serve food. We gave you our very best.",
  "Behind every bite is a chef who cares deeply about you.",
  "Our chefs wake up every morning thinking about moments like tonight.",
  "Each roll is a promise \\u2014 that we gave everything we had.",
  "We put our soul into every dish. Hope you felt it.",
  "Great sushi is not made. It is cared for, one roll at a time.",
  "Perfection is our daily pursuit. Tonight was no exception.",
  "Every ingredient was chosen with you in mind.",
  "We cook as if our family were sitting at your table.",
  "Your kindness tonight fuels our passion tomorrow.",
  "Your review is the reason we come back better every day.",
  "A few words from you can inspire a thousand better rolls.",
  "Your honest words make us stronger chefs and kinder people.",
  "We grow because guests like you believe in us.",
  "Your feedback is the compass that guides us forward.",
  "We read every review. Every single one.",
  "One kind word from you echoes through our entire team.",
  "You help us become the restaurant we always dreamed of being.",
  "Your voice shapes the future of JooN's Sushi.",
  "Good food fades. But the feeling of a great meal \\u2014 that stays.",
  "We hope tonight gave you a memory worth keeping.",
  "A great meal shared is a story worth telling.",
  "The best table in the house was always yours.",
  "We live for the moments when food becomes a memory.",
  "If tonight made you smile, our work here is done.",
  "Some evenings are just meals. We hope yours was more.",
  "Tonight, we cooked for you like you were the only guest.",
  "The joy on your face \\u2014 that is why we do this.",
  "We hope this was a night you will tell someone about.",
  "Every review helps another family discover their new favorite spot.",
  "Your words bring new friends to our table.",
  "Help us share this love with the whole community.",
  "Together, we build something worth coming back to.",
  "Your review is a gift to every guest who comes after you.",
  "What you say next could change someone's night.",
  "One review. One family. One unforgettable first visit.",
  "You are part of the JooN's Sushi story now.",
  "We are nothing without the community that lifts us up.",
  "Thank you \\u2014 from JooN, from our chefs, from all of us."
];
let qrTaglineQueue=[...QR_TAGLINES].sort(()=>Math.random()-0.5);
function nextQRTagline(){if(!qrTaglineQueue.length)qrTaglineQueue=[...QR_TAGLINES].sort(()=>Math.random()-0.5);return qrTaglineQueue.pop();}

const origShow=show;
show=function(i){
  origShow(i);
  const s=slides[cur];
  if(s.classList.contains('slide-qr')){
    const tl=s.querySelector('.qr-tagline');
    if(tl)tl.textContent=nextQRTagline();
  }
};
// init first QR
document.querySelectorAll('.slide-qr .qr-tagline').forEach(el=>el.textContent=nextQRTagline());

tick();
</script>
<script>
/* ==================== TV3 PROMO SLIDES JS (scoped to .tv3-scope) ==================== */
(function tv3Promo(){
  const SUSHI=[
    `<circle cx="50" cy="50" r="46" fill="#2c2c2c" stroke="#000" stroke-width="4"/><circle cx="50" cy="50" r="38" fill="#FFF8E1" stroke="#000" stroke-width="3"/><circle cx="50" cy="50" r="20" fill="#FF7043" stroke="#000" stroke-width="3"/><path d="M40,45 Q50,40 60,45 Q60,55 50,60 Q40,55 40,45 Z" fill="none" stroke="#FFAB91" stroke-width="2"/><ellipse cx="36" cy="40" rx="3" ry="2.2" fill="#FFF" stroke="#000" stroke-width="1.5"/><ellipse cx="64" cy="60" rx="3" ry="2.2" fill="#FFF" stroke="#000" stroke-width="1.5"/>`,
    `<circle cx="50" cy="50" r="46" fill="#2c2c2c" stroke="#000" stroke-width="4"/><circle cx="50" cy="50" r="38" fill="#FFF8E1" stroke="#000" stroke-width="3"/><circle cx="50" cy="50" r="20" fill="#D32F2F" stroke="#000" stroke-width="3"/><path d="M40,50 Q50,45 60,50 Q50,55 40,50 Z" fill="#B71C1C"/><ellipse cx="64" cy="40" rx="3" ry="2.2" fill="#FFF" stroke="#000" stroke-width="1.5"/><ellipse cx="36" cy="60" rx="3" ry="2.2" fill="#FFF" stroke="#000" stroke-width="1.5"/>`,
    `<circle cx="50" cy="50" r="46" fill="#FFF8E1" stroke="#000" stroke-width="4"/><circle cx="50" cy="50" r="20" fill="#8BC34A" stroke="#000" stroke-width="3"/><path d="M42,48 L50,42 L58,48 L58,55 L50,58 L42,55 Z" fill="#FF7043" stroke="#000" stroke-width="2"/><circle cx="35" cy="35" r="2" fill="#FF8A65"/><circle cx="65" cy="65" r="2" fill="#FF8A65"/><circle cx="65" cy="35" r="2" fill="#FF8A65"/><circle cx="35" cy="65" r="2" fill="#FF8A65"/><ellipse cx="30" cy="50" rx="2.5" ry="2" fill="#FFF" stroke="#000" stroke-width="1.2"/><ellipse cx="70" cy="50" rx="2.5" ry="2" fill="#FFF" stroke="#000" stroke-width="1.2"/>`,
    `<circle cx="50" cy="50" r="46" fill="#2c2c2c" stroke="#000" stroke-width="4"/><circle cx="50" cy="50" r="38" fill="#FFF8E1" stroke="#000" stroke-width="3"/><circle cx="50" cy="50" r="18" fill="#7CB342" stroke="#000" stroke-width="3"/><circle cx="50" cy="50" r="10" fill="#AED581" stroke="#558B2F" stroke-width="1.5"/><ellipse cx="36" cy="44" rx="3" ry="2.2" fill="#FFF" stroke="#000" stroke-width="1.5"/><ellipse cx="64" cy="56" rx="3" ry="2.2" fill="#FFF" stroke="#000" stroke-width="1.5"/>`,
    `<circle cx="50" cy="50" r="46" fill="#2c2c2c" stroke="#000" stroke-width="4"/><circle cx="50" cy="50" r="38" fill="#FFF8E1" stroke="#000" stroke-width="3"/><circle cx="50" cy="50" r="20" fill="#6D4C41" stroke="#000" stroke-width="3"/><path d="M38,50 Q50,42 62,50 Q50,58 38,50 Z" fill="#8D6E63"/><line x1="40" y1="50" x2="60" y2="50" stroke="#3E2723" stroke-width="1.5"/><ellipse cx="36" cy="62" rx="3" ry="2.2" fill="#FFF" stroke="#000" stroke-width="1.5"/><ellipse cx="64" cy="38" rx="3" ry="2.2" fill="#FFF" stroke="#000" stroke-width="1.5"/>`
  ];
  const FACE=`<g class="face"><ellipse cx="40" cy="68" rx="3.5" ry="2.5" fill="#FFB7C5" opacity="0.8"/><ellipse cx="60" cy="68" rx="3.5" ry="2.5" fill="#FFB7C5" opacity="0.8"/><circle cx="42" cy="62" r="2" fill="#000"/><circle cx="58" cy="62" r="2" fill="#000"/><circle cx="42.7" cy="61.3" r="0.7" fill="#FFF"/><circle cx="58.7" cy="61.3" r="0.7" fill="#FFF"/><path d="M46,68 Q50,72 54,68" stroke="#000" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>`;
  document.querySelectorAll('.tv3-scope').forEach(scope=>{
    if(scope.classList.contains('tv3-logo'))return;
    for(let i=1;i<=10;i++){
      const el=document.createElement('div');
      el.className=`sushi-roll sf${i}`;
      const s=SUSHI[Math.floor(Math.random()*SUSHI.length)];
      el.innerHTML=`<svg viewBox="0 0 100 100">${s}${FACE}</svg>`;
      scope.appendChild(el);
    }
  });
  const BUBBLES=[
    {svg:'<polygon fill="#E63946" stroke="#000" stroke-width="6" stroke-linejoin="round" points="100,5 122,38 158,22 152,60 192,68 162,92 195,128 152,124 162,158 118,140 100,158 82,142 38,158 50,124 5,128 38,92 8,68 48,60 42,22 78,38"/>',tc:'#FFF',words:['WHAM!','BAM!','POW!']},
    {svg:'<polygon fill="#FFEB3B" stroke="#000" stroke-width="6" stroke-linejoin="round" points="100,5 122,38 158,22 152,60 192,68 162,92 195,128 152,124 162,158 118,140 100,158 82,142 38,158 50,124 5,128 38,92 8,68 48,60 42,22 78,38"/>',tc:'#1D9BF0',words:['SMASH!','BANG!','POP!']},
    {svg:'<path fill="#FFF" stroke="#000" stroke-width="6" stroke-linejoin="round" d="M50,40 Q25,40 30,65 Q5,75 30,95 Q15,125 55,125 Q65,150 100,140 Q120,155 145,140 Q185,150 190,120 Q215,115 200,90 Q220,70 195,55 Q205,28 170,30 Q155,12 120,28 Q100,8 80,28 Q55,18 50,40 Z"/>',tc:'#FFEB3B',words:['ZZZZ...','HMMM...']},
    {svg:'<path fill="#FFF" stroke="#000" stroke-width="6" stroke-linejoin="round" d="M40,40 Q20,40 25,65 Q5,75 25,95 Q15,120 50,120 Q60,145 90,135 Q105,150 125,135 Q160,150 165,120 Q190,115 180,90 Q200,75 180,55 Q190,30 160,32 Q145,15 115,28 Q95,10 75,28 Q50,18 40,40 Z"/>',tc:'#FF9800',words:['POOF!','PUFF!','WHOOSH!']},
    {svg:'<path fill="#2EA84F" stroke="#000" stroke-width="6" stroke-linejoin="round" d="M40,90 Q20,60 50,40 Q70,15 100,30 Q130,15 150,40 Q180,60 160,90 Q190,110 170,135 Q180,160 145,150 Q130,168 100,150 Q70,168 55,150 Q20,160 30,135 Q10,110 40,90 Z"/>',tc:'#FFEB3B',words:['SPLASH!','DRIP!']},
    {svg:'<path fill="#FF9800" stroke="#000" stroke-width="6" stroke-linejoin="round" d="M30,30 Q15,55 25,80 Q5,100 30,115 Q35,140 65,128 Q80,150 110,135 Q140,148 155,125 Q185,120 175,95 Q195,70 170,55 Q170,25 140,30 Q120,10 95,28 Q65,15 50,32 Q30,30 30,30 Z"/>',tc:'#E63946',words:['OMG!!','WOW!!']}
  ];
  function shuffleBubbles(){
    document.querySelectorAll('.tv3-scope').forEach(slide=>{
      const cells=slide.querySelectorAll('.bubble');
      if(!cells.length)return;
      const pool=[...Array(BUBBLES.length).keys()].sort(()=>Math.random()-0.5).slice(0,cells.length);
      cells.forEach((cell,i)=>{
        const b=BUBBLES[pool[i]];
        const word=b.words[Math.floor(Math.random()*b.words.length)];
        cell.innerHTML=`<svg viewBox="0 0 200 160">${b.svg}</svg><span class="bubble-text" style="color:${b.tc}">${word}</span>`;
      });
    });
  }
  const BURST_POOL=[
    {fill:'#E63946',d:'M150,4 L172,40 L218,18 L210,55 L268,42 L240,75 L296,68 L260,98 L298,128 L235,118 L262,148 L208,128 L188,148 L155,118 L120,148 L92,128 L38,148 L65,118 L2,128 L42,98 L4,68 L60,75 L32,42 L90,55 L82,18 L128,40 Z'},
    {fill:'#FFEB3B',d:'M150,2 L168,32 L195,8 L195,40 L240,18 L228,50 L268,32 L250,68 L298,55 L268,85 L296,118 L255,108 L278,142 L228,122 L222,148 L188,128 L160,148 L150,118 L140,148 L112,128 L78,148 L72,122 L22,142 L45,108 L4,118 L32,85 L2,55 L50,68 L32,32 L72,50 L60,18 L105,40 L105,8 L132,32 Z'},
    {fill:'#2EA84F',d:'M40,75 Q15,30 60,30 Q80,8 110,28 Q140,8 170,28 Q200,8 240,30 Q260,15 270,35 Q290,45 280,75 Q295,95 285,125 Q288,142 250,140 Q230,155 200,135 Q170,148 140,135 Q100,148 80,135 Q40,142 30,125 Q8,100 25,80 Q8,60 40,75 Z'},
    {fill:'#1D9BF0',d:'M150,2 L168,32 L195,8 L195,40 L240,18 L228,50 L268,32 L250,68 L298,55 L268,85 L296,118 L255,108 L278,142 L228,122 L222,148 L188,128 L160,148 L150,118 L140,148 L112,128 L78,148 L72,122 L22,142 L45,108 L4,118 L32,85 L2,55 L50,68 L32,32 L72,50 L60,18 L105,40 L105,8 L132,32 Z'}
  ];
  const BURST_MAP={'tv3-1':0,'tv3-2':2,'tv3-3':1,'tv3-4':0};
  function shuffleBurst(){
    document.querySelectorAll('.tv3-scope').forEach(slide=>{
      const svg=slide.querySelector('.burst-svg');
      if(!svg)return;
      let idx=0;
      Object.keys(BURST_MAP).forEach(cls=>{if(slide.classList.contains(cls))idx=BURST_MAP[cls];});
      const b=BURST_POOL[idx];
      svg.innerHTML=`<path fill="${b.fill}" stroke="#000" stroke-width="6" stroke-linejoin="round" d="${b.d}"/>`;
    });
  }
  const PHRASES=[
    ["BOSS GONE CRAZY!","WHAT IS THIS PRICE?!"],
    ["FOR REAL?!","IS THIS PRICE REAL?"],
    ["CRAZY!!","CRAZY CRAZY!!"],
    ["BOSS RAN AWAY!","SAVE WHILE HE'S GONE!"],
    ["HQ DOESN'T KNOW!","OUR LITTLE SECRET!"],
    ["REGULARS ONLY KNEW!","THE SECRET PRICE!"],
    ["BUY ONCE!","YOU'LL COME BACK!"],
    ["IS THIS PRICE REAL?","SERIOUSLY?!"]
  ];
  const STAMPS=["FOR<br>REAL?!","NO<br>WAY!","WOW!!","CRAZY!","HOT<br>DEAL!","ONLY<br>NOW!","JUST<br>DO IT!","WHAT?!"];
  let pIdx=0;
  function rotatePhrase(){
    const banners=document.querySelectorAll('.tv3-scope .crazy-banner');
    const stamps=document.querySelectorAll('.tv3-scope .real-stamp');
    const [a,b]=PHRASES[pIdx%PHRASES.length];
    banners.forEach(el=>{el.innerHTML=`${a}<span class="line2">${b}</span>`;});
    stamps.forEach(el=>{el.innerHTML=STAMPS[pIdx%STAMPS.length];});
    pIdx++;
  }
  shuffleBubbles();
  shuffleBurst();
  rotatePhrase();
  setInterval(rotatePhrase,4500);
})();
</script>
</body>
</html>'''

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    
    total_extra = sum(1 for s in slides if 'slide-extra' in s)
    total_menu  = sum(1 for s in slides if 'slide-menu' in s)
    print(f"v8.0 Build OK | 명언:{total_extra} | 메뉴:{total_menu} | 총:{len(slides)} 슬라이드")

if __name__=="__main__":
    build()
