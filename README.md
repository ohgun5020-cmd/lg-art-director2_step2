# LG Art Director System STEP 2 v5.9.0

인테리어 & 배경 프롬프트 생성 시스템

## 개요

Step 1에서 생성된 인물/캐스팅 JSON을 받아서 **외관 + 인테리어 4분할 프롬프트**를 생성합니다.

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

## 사용법

### 1. Step 1 JSON 입력
- Step 1에서 생성된 JSON을 사이드바의 텍스트 영역에 붙여넣기
- "JSON 파싱" 버튼 클릭
- 파싱된 값이 자동으로 설정에 반영됨

### 2. Step 2 설정
- **주거 유형**: STUDIO / APARTMENT / LOFT / VILLA / PENTHOUSE
- **인테리어 스타일**: 지역별 스타일 선택
- **룸 타입**: 4분할에 포함될 방 선택
- **엔트로피 레벨**: 오브젝트 밀도 (1-10)
- **출력 프리셋**: BASIC / DETAIL_PLUS / NEGATIVE_PLUS / COMPOSITE_READY

### 3. 출력
- 외관 프롬프트 (마크다운)
- 인테리어 4분할 프롬프트 (마크다운)
- Step 3용 JSON 블록

## 프롬프트 로드 순서

1. `00_step2_core_rules.md` - 최우선
2. `10_step2_logic_physics.md`
3. `20_step2_output_handoff_qa.md`

충돌 시: 앞 파일(우선순위 높은 규칙) 승

## 버전업 방법

`prompts/` 폴더의 md 파일만 교체하면 자동 반영됨:
1. 해당 md 파일 덮어쓰기
2. 앱 재시작

## Step 1 → Step 2 데이터 플로우

```
Step 1 JSON
├── region, city, season
├── fixed.age, fixed.occupation, fixed.ethnicity
├── fashion_color, fashion_color_name
├── aspect_ratio
└── biometric_ids
        ↓
Step 2 처리
├── 주거 유형 결정 (나이 기반)
├── 인테리어 스타일 매핑
├── 60-30-10 컬러 하모니 적용
├── 직업별 앵커 오브젝트 배치
└── 네거티브 스페이스 확보
        ↓
Step 3용 JSON 출력
```
