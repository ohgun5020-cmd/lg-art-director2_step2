import streamlit as st
import google.generativeai as genai
import json
import re
import os
import hashlib
from datetime import datetime

try:
    from prompt import LG_SYSTEM_PROMPT
    PROMPT_AVAILABLE = True
except ImportError:
    LG_SYSTEM_PROMPT = "LG Art Director System STEP 2 v5.9.0 System Prompt Placeholder"
    PROMPT_AVAILABLE = False

APP_TITLE = "LG Art Director System STEP 2 v5.9.0"
APP_CAPTION = "🏠 Interior & Background Prompt Generator"
SYSTEM_GREETING = (
    "Step 1 JSON을 붙여넣거나 직접 설정을 입력해주세요.\n\n"
    "**외관 + 인테리어 4분할 프롬프트**를 생성합니다.\n\n"
    "예시: `파리 아파트, 갤러리 큐레이터, 카멜 톤 인테리어`"
)

MODEL_OPTIONS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-flash-latest",
    "gemini-pro-latest",
]

MODEL_EXCLUDE_TOKENS = (
    "image", "audio", "tts", "native", "preview", "exp",
    "embedding", "gemma", "nano", "aqa", "imagen", "veo", "robotics",
)

# Step 2 전용 옵션들
HOUSING_TYPE_OPTIONS = ["STUDIO", "APARTMENT", "LOFT", "VILLA", "PENTHOUSE"]
HOUSING_TYPE_LABELS = {
    "STUDIO": "스튜디오 (20-35㎡)",
    "APARTMENT": "아파트 (60-90㎡)",
    "LOFT": "로프트 (80-120㎡)",
    "VILLA": "빌라 (150㎡+)",
    "PENTHOUSE": "펜트하우스 (150㎡+)",
}

INTERIOR_STYLE_OPTIONS = [
    "PARIS_STYLE", "LONDON_STYLE", "MILAN_STYLE", "BERLIN_STYLE",
    "SCANDI_STYLE", "VIENNA_STYLE", "MEDITERRANEAN_EU", "DUTCH_STYLE",
    "MEXICO_STYLE", "BRAZIL_STYLE", "ARGENTINA_STYLE", "LATAM_MODERN",
]
INTERIOR_STYLE_LABELS = {
    "PARIS_STYLE": "파리 스타일",
    "LONDON_STYLE": "런던 스타일",
    "MILAN_STYLE": "밀라노 스타일",
    "BERLIN_STYLE": "베를린 스타일",
    "SCANDI_STYLE": "스칸디나비안",
    "VIENNA_STYLE": "비엔나 스타일",
    "MEDITERRANEAN_EU": "지중해 스타일",
    "DUTCH_STYLE": "더치 스타일",
    "MEXICO_STYLE": "멕시코 스타일",
    "BRAZIL_STYLE": "브라질 스타일",
    "ARGENTINA_STYLE": "아르헨티나 스타일",
    "LATAM_MODERN": "라틴 모던",
}

ROOM_TYPE_OPTIONS = ["Kitchen", "Living", "Bedroom", "Laundry", "Bathroom", "Study", "Dining"]

ENTROPY_LEVELS = {
    1: "극미니멀 (1-5개)",
    2: "극미니멀 (1-5개)",
    3: "미니멀 (5-10개)",
    4: "미니멀 (5-10개)",
    5: "큐레이티드 ⭐기본",
    6: "큐레이티드 ⭐기본",
    7: "풍성함 (30-50개)",
    8: "풍성함 (30-50개)",
    9: "맥시멀리스트 (60+)",
    10: "맥시멀리스트 (60+)",
}

OUTPUT_PRESET_OPTIONS = ["BASIC", "DETAIL_PLUS", "NEGATIVE_PLUS", "COMPOSITE_READY"]
OUTPUT_PRESET_LABELS = {
    "BASIC": "기본",
    "DETAIL_PLUS": "디테일 강화",
    "NEGATIVE_PLUS": "여백 강화",
    "COMPOSITE_READY": "합성용",
}

REGION_OPTIONS = ["EU", "LATAM"]
REGION_LABELS = {"EU": "EU(유럽)", "LATAM": "LATAM(라틴아메리카)"}

CITY_OPTIONS = {
    "EU": [
        "Paris (파리)", "London (런던)", "Rome (로마)", "Barcelona (바르셀로나)",
        "Amsterdam (암스테르담)", "Berlin (베를린)", "Prague (프라하)", "Vienna (비엔나)",
        "Madrid (마드리드)", "Florence (피렌체)", "Venice (베네치아)", "Lisbon (리스본)",
        "Athens (아테네)", "Munich (뮌헨)", "Budapest (부다페스트)", "Brussels (브뤼셀)",
    ],
    "LATAM": [
        "Mexico City (멕시코시티)", "Sao Paulo (상파울루)", "Buenos Aires (부에노스아이레스)",
        "Rio de Janeiro (리우데자네이루)", "Bogota (보고타)", "Lima (리마)",
        "Santiago (산티아고)", "Medellin (메데인)", "Cusco (쿠스코)", "Havana (아바나)",
    ],
}

ASPECT_RATIO_OPTIONS = ["9:16", "16:9", "4:5", "1:1"]
ASPECT_RATIO_LABELS = {
    "9:16": "9:16 (세로)",
    "16:9": "16:9 (와이드)",
    "4:5": "4:5 (룩북)",
    "1:1": "1:1 (정사각)",
}

JSON_BLOCK_RE = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)


def default_settings():
    return {
        "project_id": "LG_AD_2026_STEP2_01",
        "region": "EU",
        "city": CITY_OPTIONS["EU"][0],
        "season": "WINTER",
        "age": 35,
        "occupation": "Gallery Curator",
        "fashion_color": "#C19A6B",
        "fashion_color_name": "Camel",
        "aspect_ratio": "4:5",
        # Step 2 전용
        "housing_type": "APARTMENT",
        "interior_style": "PARIS_STYLE",
        "room_types": ["Kitchen", "Living", "Bedroom", "Laundry"],
        "entropy_level": 5,
        "output_preset": "BASIC",
    }


def parse_step1_json(json_text):
    """Step 1 JSON 파싱"""
    if not json_text or not json_text.strip():
        return None, "JSON이 비어있습니다."
    
    try:
        match = JSON_BLOCK_RE.search(json_text)
        if match:
            json_text = match.group(1)
        data = json.loads(json_text.strip())
        return data, None
    except json.JSONDecodeError as e:
        return None, f"JSON 파싱 오류: {e}"


def extract_step1_values(step1_json):
    """Step 1 JSON에서 값 추출"""
    if not step1_json:
        return {}
    
    extracted = {}
    extracted["region"] = step1_json.get("region", "EU")
    extracted["city"] = step1_json.get("city", "Paris")
    extracted["season"] = step1_json.get("season", "WINTER")
    extracted["fashion_color"] = step1_json.get("fashion_color", "#C19A6B")
    extracted["fashion_color_name"] = step1_json.get("fashion_color_name", "Camel")
    extracted["aspect_ratio"] = step1_json.get("aspect_ratio", "4:5")
    extracted["project_id"] = step1_json.get("project_id", "")
    extracted["biometric_ids"] = step1_json.get("biometric_ids", [])
    
    fixed = step1_json.get("fixed", {})
    extracted["age"] = fixed.get("age", 35)
    extracted["occupation"] = fixed.get("occupation", "Gallery Curator")
    
    return extracted


def fingerprint_key(api_key):
    if not api_key:
        return ""
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:12]


def load_model_options(api_key):
    if not api_key:
        return MODEL_OPTIONS
    
    fingerprint = fingerprint_key(api_key)
    cached = st.session_state.get("model_options_cache", {})
    if cached.get("fingerprint") == fingerprint and cached.get("options"):
        return cached["options"]
    
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        options = []
        for model in models:
            name = getattr(model, "name", "")
            methods = getattr(model, "supported_generation_methods", []) or []
            if "generateContent" not in methods:
                continue
            if name.startswith("models/"):
                name = name.split("/", 1)[1]
            options.append(name)
        options = [
            option for option in options
            if option.startswith("gemini-")
            and not any(token in option for token in MODEL_EXCLUDE_TOKENS)
        ]
        options = sorted(set(options))
        if not options:
            options = MODEL_OPTIONS
    except Exception:
        options = MODEL_OPTIONS
    
    st.session_state["model_options_cache"] = {
        "fingerprint": fingerprint,
        "options": options,
    }
    return options


def build_chat_history(messages):
    history = []
    for msg in messages:
        role = msg.get("role")
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        if role == "user":
            history.append({"role": "user", "parts": [content]})
        elif role == "assistant":
            history.append({"role": "model", "parts": [content]})
    return history


def get_chat_session(api_key, model_name, history):
    genai.configure(api_key=api_key)
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=LG_SYSTEM_PROMPT,
    )
    
    return model.start_chat(history=history)


def parse_response(text):
    json_data = None
    clean_text = text
    
    for match in JSON_BLOCK_RE.finditer(text):
        candidate = match.group(1).strip()
        try:
            json_data = json.loads(candidate)
            clean_text = (text[:match.start()] + text[match.end():]).strip()
            break
        except json.JSONDecodeError:
            continue
    
    return json_data, clean_text


def build_combined_prompt(settings, step1_data, user_input):
    """Step 2용 프롬프트 조합"""
    lines = [
        "[STEP2_SYSTEM_OVERRIDE_DATA]",
        f"Project_ID: {settings['project_id']}",
        "",
        "[STEP1_INHERITED_DATA]",
        f"Region: {settings['region']}",
        f"City: {settings['city']}",
        f"Season: {settings['season']}",
        f"Model_Age: {settings['age']}",
        f"Occupation: {settings['occupation']}",
        f"Fashion_Color: {settings['fashion_color']}",
        f"Fashion_Color_Name: {settings['fashion_color_name']}",
        f"Aspect_Ratio: {settings['aspect_ratio']}",
    ]
    
    if step1_data:
        lines.append("")
        lines.append("[STEP1_JSON_BLOCK]")
        lines.append("```json")
        lines.append(json.dumps(step1_data, indent=2, ensure_ascii=False))
        lines.append("```")
    
    lines.extend([
        "",
        "[STEP2_SETTINGS]",
        f"Housing_Type: {settings['housing_type']}",
        f"Interior_Style: {settings['interior_style']}",
        f"Room_Types: {', '.join(settings['room_types'])}",
        f"Entropy_Level: {settings['entropy_level']}",
        f"Output_Preset: {settings['output_preset']}",
        "",
        "[USER_CREATIVE_DIRECTION]",
        user_input,
    ])
    
    return "\n".join(lines).strip()


# ─────────────────────────────────────────────────────────────
# Streamlit UI
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .stChatMessage { font-family: 'Helvetica', sans-serif; }
    div[data-testid="stExpander"] {
        border: 1px solid #2b3447;
        border-radius: 8px;
        background-color: #1c2333;
    }
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
        color: #f8fafc;
    }
    div[data-testid="stExpander"] svg,
    div[data-testid="stExpander"] path {
        color: #f8fafc;
        fill: currentColor;
    }
    button[data-testid="stCopyButton"] {
        background-color: rgba(16, 185, 129, 0.5) !important;
        border: 1px solid rgba(16, 185, 129, 0.65) !important;
        border-radius: 6px !important;
    }
    button[data-testid="stCopyButton"] svg,
    button[data-testid="stCopyButton"] path {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
    .json-header { color: #10B981; font-weight: bold; }
    section[data-testid="stSidebar"] {
        background-color: #222a3a;
        border-right: 1px solid #1f2937;
        width: 42rem !important;
        min-width: 42rem !important;
        max-width: 42rem !important;
    }
    section[data-testid="stSidebar"] > div {
        width: 42rem !important;
        min-width: 42rem !important;
        max-width: 42rem !important;
    }
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="input"] > div {
        background-color: #0f1117 !important;
    }
    .sidebar-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #ffffff;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .context-box {
        background-color: #f0f2f6;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #333;
        margin-bottom: 20px;
    }
    .context-box .context-meta {
        font-size: 0.8rem;
        color: #666;
    }
    .step1-status {
        padding: 8px 12px;
        border-radius: 6px;
        margin: 8px 0;
        font-size: 13px;
    }
    .step1-ok { background-color: #10B98122; border: 1px solid #10B981; color: #10B981; }
    .step1-warn { background-color: #F5920022; border: 1px solid #F59200; color: #F59200; }
</style>
""",
    unsafe_allow_html=True,
)

if "applied_settings" not in st.session_state:
    st.session_state["applied_settings"] = default_settings()

if "step1_json_data" not in st.session_state:
    st.session_state["step1_json_data"] = None

api_key = ""
api_source = ""
model_option = MODEL_OPTIONS[0]
flash_context = False

# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    # 로고 헤더 (Step 1과 동일)
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center;">
                <svg viewBox="0 0 593 114" xmlns="http://www.w3.org/2000/svg" style="height:30px; width:auto; display:block;">
                    <path d="M487.606 59.5181H473.577V111.884H452.05V59.5181H438.021V41.0145H452.05V19.9712H473.577V41.0145H487.606V59.5181Z" fill="#10B981"/>
                    <path d="M417.277 6.78893C421.067 6.78893 424.211 8.03863 426.711 10.538C429.21 13.0374 430.46 16.1818 430.46 19.9712C430.46 23.7606 429.21 26.905 426.711 29.4044C424.211 31.9038 421.067 33.1535 417.277 33.1535C413.488 33.1535 410.344 31.9038 407.844 29.4044C405.345 26.905 404.095 23.7606 404.095 19.9712C404.095 16.1818 405.345 13.0374 407.844 10.538C410.344 8.03863 413.488 6.78893 417.277 6.78893ZM428.041 112.126H406.514V41.0145H428.041V112.126Z" fill="#10B981"/>
                    <path d="M323.085 113.578C315.99 113.578 309.621 111.965 303.977 108.74C298.414 105.596 294.06 101.202 290.916 95.5578C287.771 89.914 286.199 83.5446 286.199 76.4495C286.199 69.3544 287.771 62.985 290.916 57.3412C294.06 51.6974 298.414 47.3033 303.977 44.1589C309.621 40.9339 315.99 39.3214 323.085 39.3214C330.18 39.3214 336.509 40.9339 342.073 44.1589C347.716 47.3033 352.11 51.6974 355.255 57.3412C358.399 62.985 359.971 69.3544 359.971 76.4495C359.971 78.7876 359.81 81.0855 359.488 83.343H307.605C308.411 87.4549 310.185 90.6396 312.926 92.8971C315.668 95.1546 319.054 96.2834 323.085 96.2834C326.149 96.2834 328.85 95.7996 331.188 94.8321C333.607 93.784 335.26 92.4134 336.147 90.7202H357.795C356.585 95.2353 354.328 99.1859 351.022 102.572C347.716 106.039 343.645 108.74 338.807 110.675C333.97 112.61 328.729 113.578 323.085 113.578ZM338.928 69.4351C338.041 65.1619 336.227 61.9369 333.486 59.76C330.745 57.5025 327.278 56.3737 323.085 56.3737C318.893 56.3737 315.466 57.5025 312.805 59.76C310.145 61.9369 308.371 65.1619 307.484 69.4351H338.928Z" fill="#10B981"/>
                    <path d="M244.354 85.8827L235.768 95.5578V111.884H214.241V10.2961H235.768V69.9188L260.802 41.0145H284.748L257.537 71.2491L286.199 111.884H261.648L244.354 85.8827Z" fill="#10B981"/>
                    <path d="M156.148 113.578C149.456 113.578 143.489 111.965 138.249 108.74C133.008 105.596 128.936 101.202 126.034 95.5578C123.131 89.914 121.68 83.5446 121.68 76.4495C121.68 69.3544 123.131 62.985 126.034 57.3412C128.936 51.6974 133.008 47.3033 138.249 44.1589C143.489 40.9339 149.456 39.3214 156.148 39.3214C165.258 39.3214 172.031 42.3045 176.465 48.2708V41.0145H197.992V111.884H176.465V104.628C172.031 110.594 165.258 113.578 156.148 113.578ZM159.534 95.195C164.775 95.195 168.967 93.4615 172.112 89.9946C175.256 86.4471 176.828 81.932 176.828 76.4495C176.828 70.9669 175.256 66.4922 172.112 63.0253C168.967 59.4778 164.775 57.704 159.534 57.704C154.454 57.704 150.383 59.4778 147.319 63.0253C144.255 66.4922 142.723 70.9669 142.723 76.4495C142.723 81.932 144.255 86.4471 147.319 89.9946C150.383 93.4615 154.454 95.195 159.534 95.195Z" fill="#10B981"/>
                    <path d="M0 41.0145H21.527V47.7871C23.7039 44.8845 26.163 42.748 28.9043 41.3773C31.7262 40.0067 35.0722 39.3214 38.9422 39.3214C43.3766 39.3214 47.4079 40.2083 51.036 41.982C54.6642 43.6752 57.6473 46.1746 59.9855 49.4802C62.6461 46.0939 65.9115 43.5542 69.7815 41.8611C73.6515 40.1679 78.2472 39.3214 83.5685 39.3214C88.9704 39.3214 93.7273 40.6114 97.8392 43.1914C101.951 45.6908 105.136 49.319 107.393 54.0759C109.651 58.8328 110.78 64.4363 110.78 70.8863V111.884H89.2526V74.5145C89.2526 69.1126 88.2448 65.0006 86.2291 62.1787C84.2135 59.2762 81.2303 57.825 77.2797 57.825C73.8128 57.825 71.1118 59.1553 69.1768 61.8159C67.3224 64.4766 66.3146 68.3466 66.1534 73.426V111.884H44.6263V74.5145C44.6263 69.1126 43.6185 65.0006 41.6028 62.1787C39.5872 59.2762 36.604 57.825 32.6534 57.825C29.1865 57.825 26.4855 59.1553 24.5505 61.8159C22.6961 64.4766 21.6883 68.3466 21.527 73.426V111.884H0V41.0145Z" fill="#10B981"/>
                    <path d="M512.897 32C512.897 14.3269 527.224 0 544.897 0H560.897C578.57 0 592.897 14.3269 592.897 32C592.897 49.6731 578.57 64 560.897 64H544.897C527.224 64 512.897 49.6731 512.897 32Z" fill="#10B981"/>
                    <path d="M575.051 13.6008V49.134H567.116V13.6008H575.051Z" fill="white"/>
                    <path d="M552.213 42.2454H538.435L535.95 49.134H527.753L541.531 13.6008H549.771L563.548 49.134H554.698L552.213 42.2454ZM549.771 35.3567L545.324 22.9746L540.877 35.3567H549.771Z" fill="white"/>
                </svg>
            </div>
            <div>
                <div style="font-weight: bold; font-size: 1.1rem;">Art Director <span style="color: #10B981;">STEP 2</span></div>
                <div style="font-size: 0.7rem; color: #888;">v5.9.0 PROFESSIONAL</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if not PROMPT_AVAILABLE:
        st.warning("prompt.py를 찾지 못했습니다. 기본 프롬프트로 동작합니다.")

    with st.expander("🔐 시스템 설정", expanded=False):
        # API Key - secrets.toml 또는 환경변수에서 로드
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = str(st.secrets["GOOGLE_API_KEY"]).strip()
            api_source = "secrets"
            st.success("✅ API Key 연결됨 (secrets)")
        else:
            api_key = os.getenv("GOOGLE_API_KEY", "").strip()
            if api_key:
                api_source = "env"
                st.success("✅ API Key 연결됨 (env)")
            else:
                api_key = ""
                api_source = ""
                st.error("❌ API Key가 없습니다. .streamlit/secrets.toml을 설정해주세요.")

        model_options = load_model_options(api_key)
        if "model_option" not in st.session_state or st.session_state["model_option"] not in model_options:
            st.session_state["model_option"] = model_options[0]
        model_option = st.selectbox(
            "모델 선택",
            model_options,
            key="model_option",
        )

    st.markdown("---")
    
    # Step 1 JSON 입력
    st.markdown('<p class="sidebar-label">📥 Step 1 JSON 입력</p>', unsafe_allow_html=True)
    step1_json_input = st.text_area(
        "Step 1 JSON 붙여넣기",
        height=120,
        placeholder='{"schema_version": "5.9.0", "region": "EU", ...}',
        key="step1_json_input",
        label_visibility="collapsed",
    )
    
    if st.button("📋 JSON 파싱", key="parse_json_btn"):
        parsed, error = parse_step1_json(step1_json_input)
        if error:
            st.error(error)
            st.session_state["step1_json_data"] = None
        else:
            st.session_state["step1_json_data"] = parsed
            extracted = extract_step1_values(parsed)
            settings = st.session_state["applied_settings"]
            for key, value in extracted.items():
                if key in settings and value:
                    settings[key] = value
            st.session_state["applied_settings"] = settings
            st.success("✅ JSON 파싱 완료")
    
    step1_data = st.session_state.get("step1_json_data")
    if step1_data:
        st.markdown('<div class="step1-status step1-ok">✅ Step 1 데이터 로드됨</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="step1-status step1-warn">⚠️ Step 1 JSON 없음 - 직접 입력 모드</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="sidebar-label">📍 Step 1 상속값</p>', unsafe_allow_html=True)
    
    settings = st.session_state["applied_settings"]
    previous_settings = settings.copy()

    col_region, col_city = st.columns(2)
    with col_region:
        region = st.selectbox(
            "지역",
            REGION_OPTIONS,
            index=REGION_OPTIONS.index(settings["region"]),
            format_func=lambda x: REGION_LABELS[x],
            key="region",
        )
    city_list = CITY_OPTIONS[region]
    current_city = settings["city"] if settings["city"] in city_list else city_list[0]
    with col_city:
        city = st.selectbox("도시", city_list, index=city_list.index(current_city), key="city")

    col_age, col_occ = st.columns(2)
    with col_age:
        age = st.number_input("나이", min_value=18, max_value=100, value=int(settings["age"]), key="age")
    with col_occ:
        occupation = st.text_input("직업", value=settings["occupation"], key="occupation")

    col_color, col_colorname = st.columns(2)
    with col_color:
        fashion_color = st.text_input("패션컬러 (HEX)", value=settings["fashion_color"], key="fashion_color")
    with col_colorname:
        fashion_color_name = st.text_input("컬러명", value=settings["fashion_color_name"], key="fashion_color_name")

    aspect_ratio = st.selectbox(
        "비율",
        ASPECT_RATIO_OPTIONS,
        index=ASPECT_RATIO_OPTIONS.index(settings["aspect_ratio"]),
        format_func=lambda x: ASPECT_RATIO_LABELS[x],
        key="aspect_ratio",
    )

    st.markdown("---")
    st.markdown('<p class="sidebar-label">🏠 Step 2 전용 설정</p>', unsafe_allow_html=True)

    housing_type = st.selectbox(
        "주거 유형",
        HOUSING_TYPE_OPTIONS,
        index=HOUSING_TYPE_OPTIONS.index(settings["housing_type"]),
        format_func=lambda x: HOUSING_TYPE_LABELS[x],
        key="housing_type",
    )

    interior_style = st.selectbox(
        "인테리어 스타일",
        INTERIOR_STYLE_OPTIONS,
        index=INTERIOR_STYLE_OPTIONS.index(settings["interior_style"]),
        format_func=lambda x: INTERIOR_STYLE_LABELS[x],
        key="interior_style",
    )

    room_types = st.multiselect(
        "룸 타입 (4분할)",
        ROOM_TYPE_OPTIONS,
        default=settings["room_types"],
        key="room_types",
    )
    if len(room_types) == 0:
        room_types = ["Kitchen", "Living", "Bedroom", "Laundry"]

    entropy_level = st.slider(
        "엔트로피 레벨",
        min_value=1,
        max_value=10,
        value=settings["entropy_level"],
        key="entropy_level",
    )
    st.caption(ENTROPY_LEVELS.get(entropy_level, ""))

    output_preset = st.selectbox(
        "출력 프리셋",
        OUTPUT_PRESET_OPTIONS,
        index=OUTPUT_PRESET_OPTIONS.index(settings["output_preset"]),
        format_func=lambda x: OUTPUT_PRESET_LABELS[x],
        key="output_preset",
    )

    # 설정 업데이트
    new_settings = {
        "project_id": settings.get("project_id", "LG_AD_2026_STEP2_01"),
        "region": region,
        "city": city,
        "season": settings.get("season", "WINTER"),
        "age": age,
        "occupation": occupation,
        "fashion_color": fashion_color,
        "fashion_color_name": fashion_color_name,
        "aspect_ratio": aspect_ratio,
        "housing_type": housing_type,
        "interior_style": interior_style,
        "room_types": room_types,
        "entropy_level": entropy_level,
        "output_preset": output_preset,
    }
    flash_context = new_settings != previous_settings
    st.session_state["applied_settings"] = new_settings

    st.markdown("---")
    st.caption(f"시스템: LG Step2 Schema v5.9.0\n모델: {model_option}")

    if st.button("🗑️ 대화 초기화", type="secondary"):
        for key in ("messages", "model_messages", "chat_session", "step1_json_data"):
            st.session_state.pop(key, None)
        st.rerun()

# ─────────────────────────────────────────────────────────────
# Main Content
# ─────────────────────────────────────────────────────────────
st.title(APP_TITLE)
st.caption(APP_CAPTION)

applied_settings = st.session_state["applied_settings"]

# Context Box
st.markdown(
    f"""
    <div class="context-box">
        <strong>현재 컨텍스트</strong><br>
        지역: {REGION_LABELS[applied_settings["region"]]} / 도시: {applied_settings["city"]} /
        {applied_settings["age"]}세 / {applied_settings["occupation"]}
        <br>
        패션컬러: {applied_settings["fashion_color_name"]} ({applied_settings["fashion_color"]}) / 
        비율: {ASPECT_RATIO_LABELS[applied_settings["aspect_ratio"]]}
        <br>
        <span class="context-meta">
        🏠 {HOUSING_TYPE_LABELS[applied_settings["housing_type"]]} / 
        {INTERIOR_STYLE_LABELS[applied_settings["interior_style"]]} /
        엔트로피: {applied_settings["entropy_level"]} /
        프리셋: {OUTPUT_PRESET_LABELS[applied_settings["output_preset"]]}
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Chat Messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": SYSTEM_GREETING}]

if "model_messages" not in st.session_state:
    st.session_state["model_messages"] = []

api_key_fingerprint = fingerprint_key(api_key)
if (
    st.session_state.get("active_model") != model_option
    or st.session_state.get("api_key_fingerprint") != api_key_fingerprint
):
    st.session_state["chat_session"] = None
    st.session_state["active_model"] = model_option
    st.session_state["api_key_fingerprint"] = api_key_fingerprint

if st.session_state.get("chat_session") is None and api_key:
    try:
        history = build_chat_history(st.session_state["model_messages"])
        st.session_state["chat_session"] = get_chat_session(api_key, model_option, history)
    except Exception as e:
        st.error(f"모델 연결 실패: {e}")

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        with st.chat_message("assistant"):
            json_data, text_content = parse_response(msg["content"])

            if json_data:
                with st.expander("📦 STEP 3 데이터 핸드오프(JSON)", expanded=False):
                    st.json(json_data)
                    st.caption("이 JSON 데이터를 복사하여 Step 3에 전달하세요.")

            if text_content:
                st.markdown(text_content)

# Chat Input
if user_input := st.chat_input("인테리어 컨셉이나 추가 지시사항을 입력하세요..."):
    if not api_key:
        st.error("API 키가 설정되지 않았습니다. .streamlit/secrets.toml을 확인해주세요.")
        st.stop()

    if st.session_state.get("chat_session") is None:
        st.error("채팅 세션이 초기화되지 않았습니다. 새로고침 해주세요.")
        st.stop()

    step1_data = st.session_state.get("step1_json_data")
    combined_prompt = build_combined_prompt(
        st.session_state["applied_settings"],
        step1_data,
        user_input,
    )

    st.chat_message("user").write(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["model_messages"].append({"role": "user", "content": combined_prompt})

    with st.spinner("Art Director가 인테리어 & 배경을 설계 중입니다..."):
        try:
            chat = st.session_state["chat_session"]
            response = chat.send_message(combined_prompt)
            full_response = response.text or ""

            with st.chat_message("assistant"):
                json_data, text_content = parse_response(full_response)

                if json_data:
                    with st.expander("📦 STEP 3 데이터 핸드오프(JSON)", expanded=True):
                        st.json(json_data)
                        st.info("✅ Step 3용 데이터가 생성되었습니다.")

                if text_content:
                    st.markdown(text_content)

            st.session_state["messages"].append({"role": "assistant", "content": full_response})
            st.session_state["model_messages"].append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"생성 중 오류 발생: {e}")
