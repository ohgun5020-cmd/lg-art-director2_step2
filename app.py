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
    1: "극미니멀 (1-5개 오브젝트)",
    2: "극미니멀 (1-5개 오브젝트)",
    3: "미니멀 (5-10개 오브젝트)",
    4: "미니멀 (5-10개 오브젝트)",
    5: "큐레이티드 (15-25개) ⭐기본",
    6: "큐레이티드 (15-25개) ⭐기본",
    7: "풍성함 (30-50개)",
    8: "풍성함 (30-50개)",
    9: "맥시멀리스트 (60+개)",
    10: "맥시멀리스트 (60+개)",
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
        "Paris", "London", "Rome", "Barcelona", "Amsterdam", "Berlin",
        "Prague", "Vienna", "Madrid", "Florence", "Venice", "Lisbon",
        "Athens", "Munich", "Budapest", "Brussels", "Zurich", "Copenhagen",
    ],
    "LATAM": [
        "Mexico City", "São Paulo", "Buenos Aires", "Rio de Janeiro",
        "Bogotá", "Lima", "Santiago", "Medellín", "Cusco", "Havana",
        "Cartagena", "Quito", "Panama City", "Montevideo",
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
        "city": "Paris",
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
        # ```json ... ``` 블록 추출
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
    
    # 기본 필드
    extracted["region"] = step1_json.get("region", "EU")
    extracted["city"] = step1_json.get("city", "Paris")
    extracted["season"] = step1_json.get("season", "WINTER")
    extracted["fashion_color"] = step1_json.get("fashion_color", "#C19A6B")
    extracted["fashion_color_name"] = step1_json.get("fashion_color_name", "Camel")
    extracted["aspect_ratio"] = step1_json.get("aspect_ratio", "4:5")
    extracted["project_id"] = step1_json.get("project_id", "")
    extracted["biometric_ids"] = step1_json.get("biometric_ids", [])
    
    # fixed 객체에서 추출
    fixed = step1_json.get("fixed", {})
    extracted["age"] = fixed.get("age", 35)
    extracted["occupation"] = fixed.get("occupation", "Gallery Curator")
    extracted["ethnicity"] = fixed.get("ethnicity", "")
    extracted["gender"] = fixed.get("gender", "")
    
    return extracted


def resolve_api_key(user_input):
    if "GOOGLE_API_KEY" in st.secrets:
        secret_key = str(st.secrets["GOOGLE_API_KEY"]).strip()
        if secret_key:
            return secret_key, "secrets"
    
    user_key = (user_input or "").strip()
    if user_key:
        return user_key, "input"
    
    env_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if env_key:
        return env_key, "env"
    
    return "", ""


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


def build_combined_prompt(settings, step1_data, user_input, model_name):
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
    .json-header { color: #10B981; font-weight: bold; }
    section[data-testid="stSidebar"] {
        background-color: #222a3a;
        border-right: 1px solid #1f2937;
        width: 42rem !important;
        min-width: 42rem !important;
        max-width: 42rem !important;
    }
    .context-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 14px;
        color: #e2e8f0;
    }
    .context-flash {
        animation: flash 0.5s ease-out;
        border-color: #10B981;
    }
    @keyframes flash {
        0% { background-color: #10B98133; }
        100% { background-color: #1e293b; }
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

previous_settings = st.session_state["applied_settings"].copy()
settings = st.session_state["applied_settings"]
flash_context = False

# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Step 2 설정")
    
    # API Key
    st.markdown("---")
    st.markdown("**🔑 API 설정**")
    api_key_input = st.text_input(
        "Google API Key",
        type="password",
        placeholder="secrets.toml 또는 여기에 입력",
        key="api_key_input",
    )
    api_key, key_source = resolve_api_key(api_key_input)
    
    if api_key:
        st.success(f"✅ API Key 연결됨 ({key_source})")
    else:
        st.warning("⚠️ API Key를 입력해주세요")
    
    model_options = load_model_options(api_key)
    model_option = st.selectbox("모델 선택", model_options, index=0, key="model_select")
    
    # Step 1 JSON 입력
    st.markdown("---")
    st.markdown("**📥 Step 1 JSON 입력**")
    step1_json_input = st.text_area(
        "Step 1 JSON 붙여넣기",
        height=150,
        placeholder='{"schema_version": "5.9.0", "region": "EU", ...}',
        key="step1_json_input",
    )
    
    if st.button("📋 JSON 파싱", key="parse_json_btn"):
        parsed, error = parse_step1_json(step1_json_input)
        if error:
            st.error(error)
            st.session_state["step1_json_data"] = None
        else:
            st.session_state["step1_json_data"] = parsed
            extracted = extract_step1_values(parsed)
            # 설정에 반영
            for key, value in extracted.items():
                if key in settings and value:
                    settings[key] = value
            st.success("✅ JSON 파싱 완료")
    
    step1_data = st.session_state.get("step1_json_data")
    if step1_data:
        st.markdown('<div class="step1-status step1-ok">✅ Step 1 데이터 로드됨</div>', unsafe_allow_html=True)
        with st.expander("파싱된 Step 1 데이터", expanded=False):
            st.json(step1_data)
    else:
        st.markdown('<div class="step1-status step1-warn">⚠️ Step 1 JSON 없음 - 직접 입력 모드</div>', unsafe_allow_html=True)
    
    # Step 1 상속 설정 (오버라이드 가능)
    st.markdown("---")
    st.markdown("**📍 Step 1 상속값** (오버라이드 가능)")
    
    col_region, col_city = st.columns(2)
    with col_region:
        region = st.selectbox(
            "지역",
            REGION_OPTIONS,
            index=REGION_OPTIONS.index(settings["region"]),
            format_func=lambda x: REGION_LABELS[x],
            key="region",
        )
    with col_city:
        city_list = CITY_OPTIONS[region]
        current_city = settings["city"] if settings["city"] in city_list else city_list[0]
        city = st.selectbox(
            "도시",
            city_list,
            index=city_list.index(current_city),
            key="city",
        )
    
    col_age, col_occ = st.columns(2)
    with col_age:
        age = st.number_input("나이", min_value=18, max_value=100, value=int(settings["age"]), key="age")
    with col_occ:
        occupation = st.text_input("직업", value=settings["occupation"], key="occupation")
    
    col_color, col_colorname = st.columns(2)
    with col_color:
        fashion_color = st.text_input("패션 컬러 (HEX)", value=settings["fashion_color"], key="fashion_color")
    with col_colorname:
        fashion_color_name = st.text_input("컬러명", value=settings["fashion_color_name"], key="fashion_color_name")
    
    aspect_ratio = st.selectbox(
        "비율",
        ASPECT_RATIO_OPTIONS,
        index=ASPECT_RATIO_OPTIONS.index(settings["aspect_ratio"]),
        format_func=lambda x: ASPECT_RATIO_LABELS[x],
        key="aspect_ratio",
    )
    
    # Step 2 전용 설정
    st.markdown("---")
    st.markdown("**🏠 Step 2 전용 설정**")
    
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
    <div class="context-box{' context-flash' if flash_context else ''}">
        <strong>현재 컨텍스트</strong><br>
        지역: {REGION_LABELS[applied_settings["region"]]} / 도시: {applied_settings["city"]} /
        {applied_settings["age"]}세 / {applied_settings["occupation"]}
        <br>
        패션컬러: {applied_settings["fashion_color_name"]} ({applied_settings["fashion_color"]}) / 
        비율: {ASPECT_RATIO_LABELS[applied_settings["aspect_ratio"]]}
        <br>
        <span style="color: #10B981;">
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
        st.error("API 키를 사이드바에서 설정해주세요.")
        st.stop()
    
    if st.session_state.get("chat_session") is None:
        st.error("채팅 세션이 초기화되지 않았습니다. 새로고침 해주세요.")
        st.stop()
    
    step1_data = st.session_state.get("step1_json_data")
    combined_prompt = build_combined_prompt(
        st.session_state["applied_settings"],
        step1_data,
        user_input,
        model_option,
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
