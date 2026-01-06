# LG Art Director System STEP 2 v5.9.0

인테리어 & 배경 프롬프트 생성 시스템

## 구조

```
lg_art_director_step2_v5.9.0/
├── app.py                 # Streamlit 메인 앱
├── prompt.py              # 시스템 프롬프트 로더
├── prompts/               # 시스템 프롬프트 모듈
│   ├── INDEX_STEP2.md     # 로드 순서 정의
│   ├── 00_step2_core_rules.md       # 보안 + 스키마 (STEP2-CORE)
│   ├── 10_step2_logic_physics.md    # 로직 + 물리 (STEP2-LOGIC)
│   └── 20_step2_output_handoff_qa.md # 출력 + QA (STEP2-OUTPUT)
├── schemas/
│   └── LG_Step2_Schema_v1_1.json    # JSON 스키마
├── .streamlit/
│   └── secrets.toml       # API 키 설정
├── requirements.txt       # 의존성
├── check.py              # API 테스트 스크립트
└── .gitignore
```

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
streamlit run app.py
```

## API Key 설정

`.streamlit/secrets.toml` 파일에 API 키를 설정하세요:

```toml
GOOGLE_API_KEY = "your-api-key-here"
```

## 사용법

### 1. Step 1 JSON 입력
- Step 1에서 생성된 JSON을 사이드바의 텍스트 영역에 붙여넣기
- "JSON 파싱" 버튼 클릭
- 파싱된 값이 자동으로 설정에 반영됨

### 2. Step 2 전용 설정
- **주거 유형**: STUDIO / APARTMENT / LOFT / VILLA / PENTHOUSE
- **인테리어 스타일**: 지역별 스타일 선택
- **룸 타입**: 4분할에 포함될 방 선택
- **엔트로피 레벨**: 오브젝트 밀도 (1-10)
- **출력 프리셋**: BASIC / DETAIL_PLUS / NEGATIVE_PLUS / COMPOSITE_READY

### 3. 출력
- 외관 프롬프트 (마크다운)
- 인테리어 4분할 프롬프트 (마크다운)
- Step 3용 JSON 블록

## 버전업 방법

`prompts/` 폴더의 md 파일만 교체하면 자동 반영됨
