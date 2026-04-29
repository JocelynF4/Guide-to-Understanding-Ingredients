# app.py — Full UI redesign: back nav, dropdowns, color coding, polished styling

import streamlit as st

st.set_page_config(
    page_title="Ingredient Assistant",
    page_icon="🌿",
    initial_sidebar_state="expanded"
)

import io, os, base64, requests, json, re
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

# --- API clients ---
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
FDC_API_KEY = os.getenv("FDC_API_KEY")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Lato:wght@300;400;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    background-color: #0d1f13;
    color: #ddeedd;
}
#MainMenu, footer, [data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="stSidebar"] { display: block !important; transform: none !important; min-width: 250px; }
.block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 700px; }

/* ── Titles ── */
.app-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.0rem;
    font-weight: 900;
    color: #5a8c5e; /* Darker green */
    line-height: 1.3;
    padding-top: 0.5rem;
    margin-bottom: 0.2rem;
    word-wrap: break-word;
}
.sidebar-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: #cdeecc; /* Brighter to draw eyes */
    line-height: 1.05;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}
.step-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.0rem;
    font-weight: 900;
    color: #a8d5a2;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.app-subtitle {
    font-size: 1rem;
    color: #5a8c5e;
    font-weight: 300;
    margin-bottom: 1.8rem;
    letter-spacing: 0.02em;
}

/* ── Step pill ── */
.step-pill {
    display: inline-block;
    background: #1a3d20;
    color: #7dd87d;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    padding: 0.28rem 0.85rem;
    border-radius: 20px;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

/* ── Section label ── */
.section-label {
    font-size: 0.75rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #7dd87d;
    margin-bottom: 0.6rem;
    margin-top: 1.4rem;
    font-weight: 700;
}

/* ── Checkbox labels — HIGH CONTRAST ── */
div[data-testid="stCheckbox"] label p {
    color: #ffffff !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
div[data-testid="stCheckbox"] {
    background: #1a3a22 !important;
    border: 1px solid #2a4d2e !important;
    border-radius: 8px !important;
    padding: 0.2rem 0.4rem !important;
    margin-bottom: 0.2rem !important;
}

/* ── Text input ── */
div[data-baseweb="input"], .stTextInput div[data-baseweb="input"] {
    background-color: #1a3a22 !important;
    border: 1px solid #2a4d2e !important;
    border-radius: 8px !important;
}
.stTextInput input, div[data-baseweb="input"] input {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: #1a3a22 !important;
    font-family: 'Lato', sans-serif !important;
}
.stTextInput input::placeholder {
    color: #8fa888 !important;
}
.stTextInput label { color: #7dd87d !important; }

/* ── Buttons ── */
.stButton > button {
    background: #1e4d25 !important;
    color: #a8d5a2 !important;
    border: 1px solid #2e6e38 !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.3rem !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #2a6e35 !important;
    border-color: #4a9e55 !important;
}

/* ── Back button — distinct style ── */
.back-btn > button {
    background: transparent !important;
    color: #5a8c5e !important;
    border: 1px solid #2a4d2e !important;
    font-size: 0.82rem !important;
    padding: 0.35rem 0.9rem !important;
}
.back-btn > button:hover {
    color: #a8d5a2 !important;
    border-color: #5a8c5e !important;
    background: #132918 !important;
}

/* ── Product card ── */
.product-card {
    background: #132918;
    border: 1px solid #2a4d2e;
    border-left: 4px solid #4caf50;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 0.8rem 0 1.2rem 0;
}
.product-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 900;
    color: #a8d5a2;
    line-height: 1.1;
}
.product-variant {
    font-size: 0.95rem;
    color: #7dd87d;
    margin-top: 0.3rem;
    font-weight: 400;
}
.product-weight {
    font-size: 0.82rem;
    color: #4a7a50;
    margin-top: 0.15rem;
    font-weight: 300;
    letter-spacing: 0.04em;
}

}

/* ── Contains box ── */
.contains-box {
    background: #0f1f13;
    border: 1px solid #1e3d22;
    border-left: 4px solid #7dd87d;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1.5rem;
}
.contains-box-alert {
    background: #2a0d0d;
    border: 2px solid #ef5350;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 15px rgba(239, 83, 80, 0.4);
}
.contains-header {
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7dd87d;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.contains-header-alert {
    font-size: 0.9rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ef5350;
    font-weight: 900;
    margin-bottom: 0.8rem;
}
.contains-pill {
    font-size: 0.85rem;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    background: #132918;
    border: 1px solid #2a4d2e;
    color: #ddeedd;
    font-weight: 400;
}
.contains-pill.flagged {
    background: #ef5350;
    border: 1px solid #b71c1c;
    color: #ffffff;
    font-weight: 700;
}

/* ── Divider ── */
.soft-divider {
    border: none;
    border-top: 1px solid #1e3d22;
    margin: 1.5rem 0;
}

/* ── Ingredient expanders ── */
.stExpander {
    border-radius: 10px !important;
    margin-bottom: 0.5rem !important;
    border: none !important;
}

/* Safe ingredient expander */
.expander-safe > div:first-child {
    background: #0f2914 !important;
    border: 1px solid #1e4d22 !important;
    border-left: 4px solid #4caf50 !important;
    border-radius: 10px !important;
}

/* Warning ingredient expander */
.expander-warn > div:first-child {
    background: #211a09 !important;
    border: 1px solid #4d3a0a !important;
    border-left: 4px solid #ffb300 !important;
    border-radius: 10px !important;
}

/* Allergy ingredient expander */
.expander-allergy > div:first-child {
    background: #210d0d !important;
    border: 1px solid #4d1515 !important;
    border-left: 4px solid #ef5350 !important;
    border-radius: 10px !important;
}

/* Detail text inside expanders */
.detail-row {
    font-size: 0.88rem;
    color: #9abf9e;
    line-height: 1.65;
    padding: 0.1rem 0;
}
.detail-label {
    color: #5a8c5e;
    font-weight: 700;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Health flag box */
.flag-warn-box {
    background: #2a1f05;
    border: 1px solid #4d3a0a;
    border-left: 3px solid #ffb300;
    border-radius: 6px;
    padding: 0.6rem 0.9rem;
    margin-top: 0.6rem;
    font-size: 0.87rem;
    color: #ffd54f;
    line-height: 1.55;
}

/* Allergy alert box */
.flag-allergy-box {
    background: #2a0d0d;
    border: 1px solid #4d1515;
    border-left: 3px solid #ef5350;
    border-radius: 6px;
    padding: 0.6rem 0.9rem;
    margin-top: 0.6rem;
    font-size: 0.87rem;
    color: #ef9a9a;
    font-weight: 700;
    line-height: 1.55;
}

/* Safe badge */
.flag-safe-box {
    background: #0d2110;
    border: 1px solid #1e4d22;
    border-left: 3px solid #4caf50;
    border-radius: 6px;
    padding: 0.6rem 0.9rem;
    margin-top: 0.6rem;
    font-size: 0.87rem;
    color: #81c784;
    line-height: 1.55;
}

/* Legend */
.legend-row {
    display: flex;
    gap: 1.2rem;
    margin: 0.8rem 0 1.2rem 0;
    flex-wrap: wrap;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    color: #7dd87d;
}
.legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)



# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "show_camera": False,
    "scan_mode": "front",
    "captured_image_bytes": None,
    "identified_product": None,
    "usda_results": None,
    "usda_match_decision": None,
    "ingredients": None,
    "analysis_result": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Helpers ───────────────────────────────────────────────────────────────────
PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".ingredient_assistant_profile.json")

def load_allergy_profile():
    if os.path.exists(PROFILE_PATH):
        try:
            with open(PROFILE_PATH) as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_allergy_profile():
    profile = {
        "selected": [st.session_state.get(f"allergy_{i}", False) for i in range(9)],
        "custom_list": st.session_state.get("custom_allergen_list", []),
        "custom_active": st.session_state.get("custom_allergen_active", {}),
    }
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f)

def get_all_allergies():
    allergies = st.session_state.selected_allergies.copy()
    for a in st.session_state.get("custom_allergen_list", []):
        if st.session_state.get("custom_allergen_active", {}).get(a, True):
            allergies.append(a)
    return allergies

def go_back_to_scan():
    """Reset to camera step but keep allergy profile"""
    st.session_state.show_camera = False
    st.session_state.scan_mode = "front"
    st.session_state.captured_image_bytes = None
    st.session_state.identified_product = None
    st.session_state.usda_results = None
    st.session_state.usda_match_decision = None
    st.session_state.ingredients = None
    st.session_state.analysis_result = None

def full_reset():
    for key in defaults:
        st.session_state[key] = defaults[key]

def extract_contains(ingredients_text):
    """Pull the 'Contains: ...' statement from the ingredient string."""
    match = re.search(r'contains?:?\s*([^.]+\.?)', ingredients_text, re.IGNORECASE)
    if match:
        raw = match.group(1).strip().rstrip('.')
        items = [i.strip() for i in re.split(r'[,;]', raw) if i.strip()]
        return items
    return []

def render_contains_box(contains_items, user_allergies):
    """Render the Contains box with intense allergy flagging."""
    if not contains_items:
        return
    allergy_lower = [a.lower() for a in user_allergies]
    
    has_alert = False
    pills = ""
    for item in contains_items:
        # Check if this contains item matches any user allergy
        flagged = any(
            a.replace("🥜 ", "").replace("🌰 ", "").replace("🥛 ", "")
             .replace("🥚 ", "").replace("🌾 ", "").replace("🐟 ", "")
             .replace("🦐 ", "").replace("🫘 ", "").replace("🌿 ", "").lower()
            in item.lower() or item.lower() in a.lower()
            for a in allergy_lower
        )
        if flagged:
            has_alert = True
            
        cls = "flagged" if flagged else ""
        flag_icon = " 🚨" if flagged else ""
        pills += f'<span class="contains-pill {cls}">{item}{flag_icon}</span>'

    box_class = "contains-box-alert" if has_alert else "contains-box"
    header_text = "⚠️ ALLERGEN ALERT: PRODUCT CONTAINS" if has_alert else "ℹ️ PRODUCT EXPLICITLY CONTAINS"
    header_class = "contains-header-alert" if has_alert else "contains-header"

    st.markdown(f"""
    <div class="{box_class}">
        <div class="{header_class}">{header_text}</div>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            {pills}
        </div>
    </div>
    """, unsafe_allow_html=True)

def identify_product(image_bytes):
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    prompt = """
Look at this food or beverage product image.
Identify the following and return ONLY a valid JSON object — no explanation, no markdown:

{
  "brand": "brand name",
  "product_name": "product line name",
  "variant": "specific flavor or variety if visible, else null",
  "net_weight": "net weight if visible, else null",
  "search_query": "best search string to find this in a food database"
}

If you cannot identify the product at all, return:
{"error": "Could not identify product"}
"""
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            {"type": "text", "text": prompt}
        ]}],
        max_tokens=300
    )
    raw = response.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    return json.loads(raw)

def search_usda(query):
    params = {
        "api_key": FDC_API_KEY,
        "query": query,
        "dataType": ["Branded"],
        "pageSize": 8,
    }
    response = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search", params=params)
    if response.status_code != 200:
        return []
    return [f for f in response.json().get("foods", []) if f.get("ingredients")]

def pick_best_usda_match(identified_product, usda_results):
    options = [{"index": i, "description": f.get("description",""), "brand": f.get("brandOwner","")}
               for i, f in enumerate(usda_results)]
    prompt = f"""
I scanned a product identified as:
- Brand: {identified_product.get('brand')}
- Product: {identified_product.get('product_name')}
- Variant: {identified_product.get('variant')}
- Net weight: {identified_product.get('net_weight')}

Database results:
{json.dumps(options, indent=2)}

Return ONLY valid JSON, no markdown:
If confident: {{"match": <index>, "confidence": "high"}}
If unsure: {{"match": null, "candidates": [<index>, <index>], "confidence": "low"}}
If no match: {{"match": null, "candidates": [], "confidence": "none"}}
"""
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    raw = response.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    return json.loads(raw)

def extract_ingredients_from_image(image_bytes):
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    prompt = """
Look carefully at this food product label.
Find the ingredient list — it may appear below or beside the Nutrition Facts table,
in small print labeled "INGREDIENTS:".

Return ONLY the raw ingredient list as plain text.
If you cannot find it, return exactly: NOT FOUND
"""
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            {"type": "text", "text": prompt}
        ]}],
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

def analyze_ingredients(ingredients, allergy_context):
    prompt = f"""
You are a food ingredient analyst.

User allergies/sensitivities: {allergy_context if allergy_context else "none"}

For each ingredient, use EXACTLY this format — no deviations:

[Ingredient Name]
→ What it is: [one plain-English sentence]
→ Purpose in this product: [one sentence on why it's in this specific product]
→ Health flag: [ONLY include if it's an artificial dye, preservative, artificial sweetener, gut-health emulsifier, HFCS, MSG, or has a known regulatory warning. Omit entirely if safe.]
→ Allergy alert: [ONLY include if relevant to user allergies: {allergy_context}. Omit entirely if no concern.]

Rules:
- Only flag genuinely concerning ingredients
- No commentary between ingredients
- No summary at the end

Ingredient list:
{ingredients}
"""
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2500
    )
    return response.choices[0].message.content

def parse_ingredient_blocks(raw_text):
    """Parse AI output into structured ingredient dicts"""
    blocks = [b.strip() for b in raw_text.split("\n\n") if b.strip()]
    parsed = []
    for block in blocks:
        lines = block.split("\n")
        if not lines:
            continue
        name = lines[0].strip().strip("[]")
        item = {"name": name, "what": "", "purpose": "", "flag": "", "allergy": ""}
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("→ What it is:"):
                item["what"] = line.replace("→ What it is:", "").strip()
            elif line.startswith("→ Purpose in this product:"):
                item["purpose"] = line.replace("→ Purpose in this product:", "").strip()
            elif line.startswith("→ Health flag:"):
                item["flag"] = line.replace("→ Health flag:", "").strip()
            elif line.startswith("→ Allergy alert:"):
                item["allergy"] = line.replace("→ Allergy alert:", "").strip()
        parsed.append(item)
    return parsed

# ── Load persisted allergy profile once per session ───────────────────────────
if "_profile_loaded" not in st.session_state:
    _p = load_allergy_profile()
    if _p:
        for i, val in enumerate(_p.get("selected", [])):
            st.session_state[f"allergy_{i}"] = val
        st.session_state["custom_allergen_list"] = _p.get("custom_list", [])
        st.session_state["custom_allergen_active"] = _p.get("custom_active", {})
    st.session_state["_profile_loaded"] = True

# ── Sidebar: Health Profile & Reset ───────────────────────────────────────────
with st.sidebar:

    if st.button("↻ Start Over / Clear", use_container_width=True):
        full_reset()
        st.rerun()

    st.markdown('<div class="section-label" style="margin-top:1rem;">🛡 Your Health Profile</div>', unsafe_allow_html=True)
    st.caption("Toggle allergies at any time:")

    common_allergens = [
        "🥜 Peanuts", "🌰 Tree Nuts", "🥛 Dairy", "🥚 Eggs",
        "🌾 Gluten", "🐟 Fish", "🦐 Shellfish", "🫘 Soy", "🌿 Sesame"
    ]
    
    selected = []
    cols = st.columns(2)
    for i, allergen in enumerate(common_allergens):
        with cols[i % 2]:
            if st.checkbox(allergen, key=f"allergy_{i}"):
                selected.append(allergen)
    st.session_state.selected_allergies = selected
    
    st.markdown('<div class="section-label">Other ingredients to watch</div>', unsafe_allow_html=True)

    if "custom_allergen_list" not in st.session_state:
        st.session_state.custom_allergen_list = []
    if "custom_allergen_active" not in st.session_state:
        st.session_state.custom_allergen_active = {}

    # Render existing custom allergens as removable checkboxes
    to_remove = None
    for allergen in st.session_state.custom_allergen_list:
        c1, c2 = st.columns([5, 1])
        with c1:
            checked = st.checkbox(allergen, value=st.session_state.custom_allergen_active.get(allergen, True), key=f"custom_cb_{allergen}")
            st.session_state.custom_allergen_active[allergen] = checked
        with c2:
            st.markdown("<div style='margin-top:0.35rem'>", unsafe_allow_html=True)
            if st.button("✕", key=f"rm_{allergen}"):
                to_remove = allergen
    if to_remove:
        st.session_state.custom_allergen_list.remove(to_remove)
        st.session_state.custom_allergen_active.pop(to_remove, None)
        st.rerun()

    with st.form("add_allergen_form", clear_on_submit=True):
        new_a = st.text_input("add", label_visibility="collapsed", placeholder="e.g. sulfites, carmine, MSG...")
        if st.form_submit_button("＋ Add", use_container_width=True) and new_a.strip():
            name = new_a.strip()
            if name not in st.session_state.custom_allergen_list:
                st.session_state.custom_allergen_list.append(name)
                st.session_state.custom_allergen_active[name] = True
            st.rerun()

save_allergy_profile()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP FLOW
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="app-title" style="margin-bottom: 0.3rem;">🌿 Your Ingredient Assistant</div>', unsafe_allow_html=True)

if (st.session_state.identified_product is None
      and st.session_state.ingredients is None):

    st.markdown('<div class="app-subtitle">Point your camera at a food label to unpack every ingredient.</div>', unsafe_allow_html=True)

    if st.session_state.scan_mode == "front":
        st.markdown('<div class="step-pill">Step 1 of 4 — Scan Product Front</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Point camera at the front of the package</div>', unsafe_allow_html=True)
        st.caption("Make sure the brand name and product name are clearly visible.")
    else:
        st.markdown('<div class="step-pill">Step 1 of 4 — Scan Ingredient Panel</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Point camera at the ingredient list on the package</div>', unsafe_allow_html=True)
        st.caption("Usually printed beside or below the Nutrition Facts table.")

    with st.expander("💡 Tips for a good scan"):
        st.write("""
        - **Lighting:** Make sure there's no glare blocking the text.
        - **Distance:** Get close enough that text is legible, but keep the whole section in frame.
        - **Focus:** Tap the camera to focus if things look blurry.
        """)

    cam_tab, upload_tab = st.tabs(["📷 Camera", "📁 Upload Photo"])

    with cam_tab:
        if not st.session_state.show_camera:
            if st.button("Open Camera", use_container_width=True):
                st.session_state.show_camera = True
                st.rerun()
        else:
            photo = st.camera_input(label="cam", label_visibility="collapsed")
            if photo is not None:
                st.session_state.captured_image_bytes = photo.getvalue()
                st.session_state.show_camera = False
                st.rerun()
            if st.button("✖ Cancel"):
                st.session_state.show_camera = False
                st.rerun()

    with upload_tab:
        uploaded = st.file_uploader(
            "Choose a photo", type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )
        if uploaded is not None:
            st.session_state.captured_image_bytes = uploaded.read()
            st.session_state.show_camera = False
            st.rerun()

    # Process captured photo
    if (st.session_state.captured_image_bytes is not None
            and st.session_state.identified_product is None
            and st.session_state.ingredients is None):

        if st.session_state.scan_mode == "front":
            msg = st.empty()
            bar = st.progress(0)
            try:
                msg.markdown("**1 / 3** — Identifying product...")
                bar.progress(33)
                result = identify_product(st.session_state.captured_image_bytes)
                if "error" in result:
                    bar.empty()
                    msg.error("❌ Couldn't identify this product. Try a clearer photo.")
                    st.session_state.captured_image_bytes = None
                else:
                    bar.progress(100)
                    msg.success("✅ Product identified!")
                    st.session_state.identified_product = result
                    st.rerun()
            except Exception as e:
                bar.empty()
                msg.error(f"❌ Error: {e}")
                st.session_state.captured_image_bytes = None
        else:
            msg = st.empty()
            bar = st.progress(0)
            msg.markdown("Extracting ingredient list via Vision AI...")
            bar.progress(50)
            extracted = extract_ingredients_from_image(st.session_state.captured_image_bytes)
            if extracted == "NOT FOUND":
                bar.empty()
                msg.error("❌ Couldn't find ingredients. Try getting closer.")
                st.session_state.captured_image_bytes = None
            else:
                bar.progress(100)
                msg.success("✅ Ingredients imported!")
                st.session_state.ingredients = extracted
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — CONFIRM PRODUCT
# ══════════════════════════════════════════════════════════════════════════════
elif (st.session_state.identified_product is not None
      and st.session_state.usda_results is None
      and st.session_state.usda_match_decision is None
      and st.session_state.ingredients is None):

    with st.container():
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Retake Photo"):
            go_back_to_scan()
            st.session_state.show_camera = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-pill">Step 2 of 4 — Confirm Product</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Is this what you scanned?</div>', unsafe_allow_html=True)

    p = st.session_state.identified_product
    variant_text = p.get('variant') or ""
    weight_text = p.get('net_weight') or ""

    st.markdown(f"""
    <div class="product-card">
        <div class="product-brand">{p.get('brand', 'Unknown Brand')}</div>
        <div class="product-variant">{p.get('product_name', '')}{"  ·  " + variant_text if variant_text else ""}</div>
        <div class="product-weight">{weight_text}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, that's it"):
            msg = st.empty()
            bar = st.progress(33)
            msg.markdown("**2 / 3** — Searching USDA database...")
            bar.progress(55)
            results = search_usda(p.get("search_query", ""))
            if results:
                msg.markdown("**3 / 3** — Finding best match...")
                bar.progress(80)
                decision = pick_best_usda_match(p, results)
            else:
                decision = {"match": None, "candidates": [], "confidence": "none"}
            bar.progress(100)
            msg.success("✅ Done!")
            st.session_state.usda_results = results
            st.session_state.usda_match_decision = decision
            st.rerun()
    with col2:
        if st.button("🔄 Retake Photo"):
            go_back_to_scan()
            st.session_state.show_camera = True
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — SMART USDA MATCHING
# ══════════════════════════════════════════════════════════════════════════════
elif (st.session_state.usda_results is not None
      and st.session_state.ingredients is None):

    results = st.session_state.usda_results

    with st.container():
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back to Confirm"):
            st.session_state.usda_results = None
            st.session_state.usda_match_decision = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if not results:
        st.markdown('<div class="step-pill">Step 3 of 4 — Not in Database</div>', unsafe_allow_html=True)
        st.warning("⚠️ This product wasn't found in the USDA database.")
        st.write("We'll scan the ingredient panel directly instead.")
        if st.button("📷 Scan Ingredient Panel"):
            st.session_state.scan_mode = "ingredients"
            st.session_state.usda_results = None
            st.session_state.usda_match_decision = None
            st.session_state.identified_product = None
            st.session_state.captured_image_bytes = None
            st.session_state.show_camera = True
            st.rerun()
    else:
        decision = st.session_state.usda_match_decision
        if decision is None:
            st.rerun()

        if decision.get("confidence") == "high":
            idx = decision["match"]
            st.session_state.ingredients = results[idx].get("ingredients")
            st.session_state.usda_match_decision = None
            st.rerun()

        elif decision.get("confidence") == "low":
            st.markdown('<div class="step-pill">Step 3 of 4 — Select Exact Product</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Which of these is yours?</div>', unsafe_allow_html=True)

            candidates = [results[i] for i in decision.get("candidates", []) if i < len(results)]
            for i, food in enumerate(candidates):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                    <div class="product-card" style="margin-bottom:0.4rem">
                        <div class="product-brand" style="font-size:1.2rem">{food.get('brandOwner','')}</div>
                        <div class="product-variant">{food.get('description','')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("Select", key=f"pick_{i}"):
                        st.session_state.ingredients = food.get("ingredients")
                        st.session_state.usda_results = None
                        st.session_state.usda_match_decision = None
                        st.rerun()

            st.markdown("---")
            if st.button("📷 None of these — Scan Ingredient Panel"):
                st.session_state.scan_mode = "ingredients"
                st.session_state.usda_results = None
                st.session_state.usda_match_decision = None
                st.session_state.identified_product = None
                st.session_state.captured_image_bytes = None
                st.session_state.show_camera = True
                st.rerun()
        else:
            st.markdown('<div class="step-pill">Step 3 of 4 — No Match Found</div>', unsafe_allow_html=True)
            st.warning("⚠️ Couldn't find a confident match in the USDA database.")
            if st.button("📷 Scan Ingredient Panel"):
                st.session_state.scan_mode = "ingredients"
                st.session_state.usda_results = None
                st.session_state.usda_match_decision = None
                st.session_state.identified_product = None
                st.session_state.captured_image_bytes = None
                st.session_state.show_camera = True
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.ingredients is not None:

    with st.container():
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Scan Again"):
            go_back_to_scan()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-pill">Step 4 of 4 — Ingredient Analysis</div>', unsafe_allow_html=True)

    # Show product name if available
    if st.session_state.identified_product:
        p = st.session_state.identified_product
        variant = p.get('variant') or ""
        variant_display = f"  ·  {variant}" if variant else ""
        st.markdown(f"""
        <div class="product-card">
            <div class="product-brand">{p.get('brand','')}</div>
            <div class="product-variant">{p.get('product_name','')}{variant_display}</div>
            <div class="product-weight">{p.get('net_weight','')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Contains box
    contains_items = extract_contains(st.session_state.ingredients)
    if contains_items:
        render_contains_box(contains_items, get_all_allergies())

    # Run analysis
    if st.session_state.analysis_result is None:
        allergy_context = ", ".join(get_all_allergies()) or "none"
        with st.status("🔬 Analyzing ingredients...", expanded=True) as status:
            st.write("Reading ingredient list...")
            st.write("Checking for health flags & allergies...")
            res = analyze_ingredients(st.session_state.ingredients, allergy_context)
            status.update(label="✅ Analysis complete!", state="complete", expanded=False)
            st.session_state.analysis_result = res
            st.rerun()

    if st.session_state.analysis_result:
        # Legend
        ingredients = parse_ingredient_blocks(st.session_state.analysis_result)

        n_allergy = sum(1 for i in ingredients if i["allergy"])
        n_flag = sum(1 for i in ingredients if i["flag"] and not i["allergy"])
        n_safe = len(ingredients) - n_allergy - n_flag

        st.markdown(f"""
        <div style="display:flex;gap:1rem;padding:0.5rem 0 1.2rem 0;border-bottom:1px solid #1e3d22;margin-bottom:1rem;flex-wrap:wrap;">
            <div style="flex:1;text-align:center;"><div style="font-size:1.5rem;font-weight:900;color:#ddeedd">{len(ingredients)}</div><div style="font-size:0.72rem;color:#7dd87d;text-transform:uppercase;letter-spacing:0.1em">Ingredients</div></div>
            <div style="flex:1;text-align:center;"><div style="font-size:1.5rem;font-weight:900;color:#4caf50">{n_safe}</div><div style="font-size:0.72rem;color:#7dd87d;text-transform:uppercase;letter-spacing:0.1em">Safe</div></div>
            <div style="flex:1;text-align:center;"><div style="font-size:1.5rem;font-weight:900;color:#ffb300">{n_flag}</div><div style="font-size:0.72rem;color:#7dd87d;text-transform:uppercase;letter-spacing:0.1em">Flagged</div></div>
            <div style="flex:1;text-align:center;"><div style="font-size:1.5rem;font-weight:900;color:#ef5350">{n_allergy}</div><div style="font-size:0.72rem;color:#7dd87d;text-transform:uppercase;letter-spacing:0.1em">Allergens</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">Click any ingredient to learn more</div>', unsafe_allow_html=True)

        details_html = ""
        for item in ingredients:
            if item["allergy"]:
                border, bg, icon = "#ef5350", "#210d0d", "🚨"
            elif item["flag"]:
                border, bg, icon = "#ffb300", "#211a09", "⚠️"
            else:
                border, bg, icon = "#4caf50", "#0f2914", "✅"

            content = ""
            if item["what"]:
                content += f'<div class="detail-label">What it is</div><div class="detail-row">{item["what"]}</div>'
            if item["purpose"]:
                content += f'<div class="detail-label" style="margin-top:0.6rem">Purpose</div><div class="detail-row">{item["purpose"]}</div>'
            if item["flag"]:
                content += f'<div class="flag-warn-box">⚠️ {item["flag"]}</div>'
            if item["allergy"]:
                content += f'<div class="flag-allergy-box">🚨 Allergy concern: {item["allergy"]}</div>'
            if not item["flag"] and not item["allergy"]:
                content += '<div class="flag-safe-box">✅ No known health concerns for this ingredient</div>'

            details_html += f"""<details style="margin-bottom:0.5rem;">
<summary style="background:{bg};border:1px solid #2a4d2e;border-left:4px solid {border};border-radius:10px;padding:0.75rem 1rem;cursor:pointer;list-style:none;color:#ddeedd;font-family:'Lato',sans-serif;font-size:0.95rem;font-weight:500;">{icon} {item['name']}</summary>
<div style="background:{bg};border:1px solid #2a4d2e;border-top:none;border-radius:0 0 10px 10px;padding:0.8rem 1rem;">{content}</div>
</details>"""

        st.markdown(details_html, unsafe_allow_html=True)

    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
    if st.button("🔁 Scan Another Product"):
        full_reset()
        st.rerun()