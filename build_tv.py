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


    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JooN's Sushi Menu</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Cormorant+Garamond:wght@700&family=Inter:wght@300;400&display=swap" rel="stylesheet">
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

</style>
</head>
<body>
<div class="slideshow" id="ss">''' + "".join(slides) + '''</div>
<div id="promo-overlay" style="opacity:0;visibility:hidden;transition:opacity 1.2s ease;position:fixed;inset:0;z-index:9999;background:#000"><iframe id="promo-iframe" src="https://681014la-wq.github.io/joons-tv-3/" style="width:100%;height:100%;border:0;display:block"></iframe></div>
<script>(function(){const ov=document.getElementById('promo-overlay');let on=false,cnt=0;function p(){if(on)return;on=true;ov.style.visibility='visible';ov.style.opacity='1';setTimeout(()=>{ov.style.opacity='0';setTimeout(()=>{ov.style.visibility='hidden';on=false;},400);},24000);}const obs=new MutationObserver(ms=>{ms.forEach(m=>{const el=m.target;const wasActive=m.oldValue&&m.oldValue.includes('active');const isActive=el.classList.contains('active');if(!wasActive&&isActive&&el.classList.contains('slide')&&!on){cnt++;if(cnt%5===0)p();}});});document.querySelectorAll('.slide').forEach(s=>obs.observe(s,{attributes:true,attributeFilter:['class'],attributeOldValue:true}));})();</script>
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
</body>
</html>'''

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    
    total_extra = sum(1 for s in slides if 'slide-extra' in s)
    total_menu  = sum(1 for s in slides if 'slide-menu' in s)
    print(f"v8.0 Build OK | 명언:{total_extra} | 메뉴:{total_menu} | 총:{len(slides)} 슬라이드")

if __name__=="__main__":
    build()
