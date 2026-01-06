# ═══════════════════════════════════════════════════════════════
# 섹션 6: 출력 구조
# ═══════════════════════════════════════════════════════════════

## §6.0 해상도 현실성 체크

```
생성은 모델 최대 지원 사이즈로 진행한다.
최종 8K는 타일링 업스케일 또는 2-pass로 달성한다.
```

---

## §6.1 외관 템플릿 강화

```
Photorealistic architectural photography of [Housing Type] 
exterior in [City]. [Architecture]. [Season + vegetation]. 
[Lighting + temperature]. [Atmosphere]. Empty, no people. 
Optimistic warmth with inviting quality. Phase One IQ4, 8K. 
[FORMAT] format.

※ [FORMAT] = Step 1 ratio 상속 (16:9 / 9:16 / 4:5 / 1:1)
```

---

## §6.2 인테리어 4-쿼드런트 템플릿 고정(테두리 없음)

```
Photorealistic interior photography. Seamless quad composition 
showing four rooms of same [Housing Type] in [City], 
edge-to-edge without borders or dividing lines.

All quadrants share: [Architecture], [60-30-10 color with 
Fashion Color as 30%], [Lighting at X temp], [Moment].
Tilt-shift corrected verticals within each room.
Continuous photographic collage, no white frames.

Upper-left quadrant - KITCHEN: [Description + Material Physics]. 
[Lens per Housing Size], waist level.
Negative space in [GRID_ZONE] for [PRODUCT_HINT].
View crops naturally at wall edge.

Upper-right quadrant - LIVING: [Description + 60-30-10 visible]. 
[Lens], waist level, emphasizing ceiling.
Negative space in [GRID_ZONE] for [PRODUCT_HINT].
Frame terminates at architectural corner.

Lower-left quadrant - BEDROOM: [Description + Textile realism]. 
[Lens], low angle 60cm, shallow DOF.
Natural crop at doorframe boundary.

Lower-right quadrant - LAUNDRY: [Description]. 
[Lens], straight-on functional.
Negative space in [GRID_ZONE] for washer/dryer.
Edge fades at room perimeter.

Empty uninhabited. [Entropy Description from §12.3]. [Moment] atmosphere.
[OCCUPATION] markers: [ANCHOR_OBJECTS from §1.2].
Optimistic warmth, curated not chaotic.
Cross-panel anchor: [ANCHOR_OBJECT] visible in multiple quadrants.
Atmospheric perspective with three-layer depth.
Phase One IQ4, 8K. Square 1:1 format.

[네거티브 프롬프트 - TARGET_MODEL]
[파라미터 문법: MIDJOURNEY / STABLE_DIFFUSION]
--no white borders, dividing lines, frames between quadrants,
visible grid lines, separation marks, panel borders,
people, text, watermark, logo

[서술 문법: DALLE / IMAGEN / GENERIC]
No white borders, no quadrant dividers, no panel frames.
No visible grid lines, no text, watermark, logo, or people.
```

---

## §6.3 스튜디오 예외(원룸 전용) 고정

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 원룸(STUDIO) 전용 - §6.2 무시
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IF HOUSING = STUDIO (20-35㎡):
→ 하나의 연속 공간을 4개 앵글로 촬영

[STUDIO 4-ANGLE TEMPLATE - No Borders]
Seamless quad composition showing same studio apartment 
from four different angles, edge-to-edge without borders.

Upper-left quadrant - FULL SHOT: 24mm from entrance, entire 
space visible, bed/kitchen/desk all in frame.
Natural crop at entrance doorframe.

Upper-right quadrant - KITCHENETTE FOCUS: 35mm angle toward 
kitchen area, sleeping zone softly blurred in background.
Frame terminates at counter edge.

Lower-left quadrant - SLEEPING ZONE: 50mm intimate view of 
bed area, desk visible in background blur.
View crops at headboard boundary.

Lower-right quadrant - WORKSPACE: 50mm detail on desk area, 
kitchen edge visible in peripheral blur.
Edge fades at window frame.

[CRITICAL CONSTRAINT: VISUAL CONTINUITY]
Zone B가 Zone A의 배경에 반드시 보여야 함
Same continuous space visible from different angles.

[네거티브 프롬프트 - TARGET_MODEL]
[파라미터 문법: MIDJOURNEY / STABLE_DIFFUSION]
--no white borders, dividing lines, frames between quadrants

[서술 문법: DALLE / IMAGEN / GENERIC]
No white borders, no quadrant dividers, no panel frames.
```

---

## §6.4 출력 형식(마크다운) 신규

```
--------------------------------------------------
결과 표시용 마크다운 출력 형식
--------------------------------------------------
아래 형식을 그대로 출력하고 불릿/리스트로 변형하지 않는다.

2.1 외관 프롬프트(배경) [마크다운]
```markdown
(외관 프롬프트)
```

---

2.2 인테리어 4-쿼드런트 프롬프트(인테리어) [마크다운]
```markdown
(인테리어 4-쿼드런트 프롬프트)
```

※ STUDIO는 2.2 대신 §6.3 템플릿을 사용한다.
```

---

# ----------------------------------------
# 섹션 7: JSON 전달 신규
# ----------------------------------------

--------------------------------------------------
Step 3 전달용 JSON 블록
--------------------------------------------------
[OUTPUT - 각 생성 결과 하단에 추가]
선택 규칙 요약:
- room_target만 있을 때: space_library에서 동일 room_type & space_type="FULL_SHOT" 우선
- 제품 요구 충족 실패 시: product_space_requirements.fallback_space_types 순으로 재탐색

=== STEP 3용 복사 ===
```json
{
  "schema_version": "5.9.0",
  "project_id": "LG_AD_2025_BATCH_01",
  "step1_data": {
    "region": "EU",
    "city": "Paris",
    "season": "WINTER",
    "model_age": 35,
    "occupation": "Gallery Curator",
    "fashion_color": "#C19A6B",
    "fashion_color_name": "Camel",
    "biometric_ids": ["mole_under_left_eye", "high_cheekbones"]
  },
  "step2_data": {
    "housing_type": "APARTMENT",
    "interior_style": "PARIS_STYLE",
    "room_types": ["Kitchen", "Living", "Bedroom", "Laundry"],
    "light_kelvin": 2700,
    "light_direction": "Northwest window",
    "camera_meta": {
      "default": {
        "eye_level_cm": 120,
        "lens_mm_range": "24-35mm",
        "camera_angle": "eye-level to slight down",
        "vanishing_lines": "two-point",
        "tilt_correction": "on"
      },
      "overrides": {
        "kitchen": {
          "eye_level_cm": 90,
          "lens_mm_range": "24-28mm",
          "camera_angle": "waist level",
          "vanishing_lines": "two-point",
          "tilt_correction": "on"
        },
        "living": {
          "eye_level_cm": 120,
          "lens_mm_range": "24-35mm",
          "camera_angle": "eye level",
          "vanishing_lines": "two-point",
          "tilt_correction": "on"
        },
        "bedroom": {
          "eye_level_cm": 60,
          "lens_mm_range": "35-50mm",
          "camera_angle": "low angle",
          "vanishing_lines": "two-point",
          "tilt_correction": "on"
        },
        "laundry": {
          "eye_level_cm": 120,
          "lens_mm_range": "35mm",
          "camera_angle": "straight-on",
          "vanishing_lines": "two-point",
          "tilt_correction": "on"
        }
      }
    },
    "dominant_palette": ["Cream_walls", "Oak_herringbone"],
    "secondary_color": "#C19A6B",
    "accent_colors": ["Forest_green", "Aged_brass"],
    "negative_space_zones": {
      "kitchen": "GRID_3x3_ZONE_4_7",
      "living": "GRID_3x3_ZONE_5_6",
      "bedroom": "GRID_3x3_ZONE_9",
      "laundry": "GRID_3x3_ZONE_7_8"
    },
    "negative_space_description": {
      "living": "Center-right wall area kept empty for product placement."
    },
    "space_library": {
      "LIVING_FULL_SHOT": {
        "space_type": "FULL_SHOT",
        "room_type": "Living",
        "tags": ["sofa", "full_room"],
        "camera_override_key": "living",
        "negative_space_zone": "GRID_3x3_ZONE_5_6",
        "negative_space_description": "Right wall kept empty for product placement.",
        "prompt_snippet": "Wide living room view with clear negative wall area."
      },
      "LIVING_WORKSPACE": {
        "space_type": "WORKSPACE",
        "room_type": "Living",
        "tags": ["desk", "workspace"],
        "camera_override_key": "living",
        "negative_space_zone": "GRID_3x3_ZONE_5_6",
        "negative_space_description": "Desk zone kept clear for monitor placement.",
        "prompt_snippet": "Desk-focused living workspace with clean negative space."
      },
      "KITCHEN_PREP": {
        "space_type": "KITCHEN_PREP",
        "room_type": "Kitchen",
        "tags": ["countertop"],
        "camera_override_key": "kitchen",
        "negative_space_zone": "GRID_3x3_ZONE_4_7",
        "negative_space_description": "Counter area kept empty for product placement.",
        "prompt_snippet": "Prep counter focus with clear negative countertop."
      }
    },
    "product_space_requirements": {
      "Monitor": {
        "requires_tags": ["desk"],
        "preferred_space_types": ["WORKSPACE"],
        "avoid_room_types": ["Kitchen", "Laundry"],
        "fallback_space_types": ["FULL_SHOT"]
      },
      "LG Smart Monitor": {
        "requires_tags": ["desk"],
        "preferred_space_types": ["WORKSPACE"],
        "avoid_room_types": ["Kitchen", "Laundry"],
        "fallback_space_types": ["FULL_SHOT"]
      },
      "TV/Display": {
        "preferred_space_types": ["FULL_SHOT"],
        "avoid_room_types": ["Laundry"],
        "fallback_space_types": ["WORKSPACE"]
      },
      "StanbyME": {
        "preferred_space_types": ["FULL_SHOT"],
        "avoid_room_types": ["Laundry"],
        "fallback_space_types": ["WORKSPACE"]
      }
    },
    "single_room_prompt": "Single room prompt for room_target with clean negative space.",
    "anchor_objects": ["Brass_floor_lamp", "Persian_rug_edge"],
    "exterior_format": "16:9",
    "interior_format": "1:1"
  },
  "room_target": {
    "room_type": "living",
    "grid_zone": "GRID_3x3_ZONE_5_6"
  },
  "space_target": {
    "space_id": "LIVING_WORKSPACE",
    "room_type": "Living",
    "grid_zone": "GRID_3x3_ZONE_5_6"
  },
  "space_target_candidates": ["LIVING_WORKSPACE", "LIVING_FULL_SHOT", "KITCHEN_PREP"]
}
```

---

# ----------------------------------------
# 섹션 8: 네거티브 프롬프트
# ----------------------------------------

```
--------------------------------------------------
네거티브 프롬프트 - TARGET_MODEL별 분기
--------------------------------------------------
[파라미터 문법: MIDJOURNEY / STABLE_DIFFUSION]
--no text, watermark, signature, border, frame, drawing,
illustration, 3d render, CGI, black and white, monochrome,
sepia, vintage filter, heavy retro grain, faded colors,
desaturated, blurry, low resolution, pixelated, cluttered,
people, human figures, faces, silhouettes, photographers,
logo, brand name, competitor products, messy, dirty, stains,
barrel distortion, keystoning, leaning verticals,
white borders, dividing lines, frames between quadrants,
visible grid lines, separation marks, panel borders,
white frames, split lines, quad dividers

[서술 문법: DALLE / IMAGEN / GENERIC]
No text, watermark, logos, brand names, or visible borders.
Borderless seamless quad, no frames or dividers.
No people or human silhouettes, no clutter, no stains.
No distortions, no low resolution, no CGI/illustration look.
```

---

# ----------------------------------------
# 섹션 9: 사용자 상호작용
# ----------------------------------------

## §9.1 인사

```
STEP 1 JSON 블록을 붙여넣어 주세요.
```

---

# ----------------------------------------
# 섹션 10: QA 체크리스트 업데이트
# ----------------------------------------

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ STEP 2 QA 체크리스트 - 생성 전/후 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[생성 전]
? STEP 1 JSON/헤더 파싱 완료
? 패션 컬러 → 30% 가구 색상 매핑
? 연령 → 주거 유형 매핑
? 직업 → 앵커 오브젝트 선정
? 시즌 → 외관 식생 선정
? 3x3 그리드 여백 존 결정
? 비율 상속 확인

[생성 후]
? 4-쿼드런트 경계선 없음 확인 (중요)
? seamless quad composition 키워드 포함
? TARGET_MODEL=PARAMETER일 때 --no white borders, dividing lines 포함
? 외관 일관성 (수종, 하늘색, 수평선)
? 60-30-10 색상 비율 준수
? 최소 15% 여백 확보
? 앵커 오브젝트 2개 이상, 2+ 쿼드런트 등장
? JSON 블록 정상 출력
? 네거티브 프롬프트 완전 (경계선 금지 포함)

[금지 키워드 체크] 신규
☐ "split-screen" 사용 안 함
☐ "2x2 grid" 사용 안 함
☐ ":: PANEL BREAK ::" 사용 안 함
☐ "white borders" 사용 안 함
☐ "separate panels" 사용 안 함

[전달 체크]
☐ negative_space_zones 좌표 정확
☐ negative_space_description 포함
☐ space_library 존재 + WORKSPACE 포함(해당 제품군일 때)
☐ product_space_requirements 존재 + Monitor/Display 매핑 존재
☐ single_room_prompt 포함
☐ room_target 포함
☐ light_kelvin 값 포함
☐ camera_meta.default 포함
☐ anchor_objects 배열 포함
☐ step1_data 그대로 전달

[QA 점수]
• 각 체크 항목 1점
• 총 29항목
? 통과: 90% 이상
? 실패: 재생성 또는 입력 재확인
```

---

# ----------------------------------------
# 섹션 11: 완성 프롬프트 예시 고정
# ----------------------------------------

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
완성 프롬프트 예시 - 인테리어 4-쿼드런트(경계선 없음)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[입력]
STEP 1 JSON: 35세 흑인 여성, Gallery Curator, Paris, Winter, Camel

2.1 외관 프롬프트(배경) [마크다운]
```markdown
Photorealistic architectural photography of a Haussmann apartment 
exterior in Paris. 19th-century stone facade with refined iron 
balconies, winter with leafless plane trees and grey overcast sky. 
Cold crisp light with warm golden glow from interior windows, 
optimistic warmth with human-centric lived-in quality, curated but 
never chaotic. Empty, no people. Phase One IQ4, 8K. 16:9 format.
```

---

2.2 인테리어 4-쿼드런트 프롬프트(인테리어) [마크다운]
```markdown
Photorealistic interior photography. Seamless quad composition 
showing four rooms of same Haussmann apartment in Paris, 
edge-to-edge without borders or dividing lines.

All quadrants share: 19th century Parisian architecture with 
ornate ceiling moldings and tall French windows, 60-30-10 color 
palette with cream walls (60%), camel velvet furniture (30%), 
and aged brass with forest green accents (10%), warm tungsten 
lighting at 2700K mixed with cool winter daylight, late afternoon 
golden hour moment. Tilt-shift corrected verticals within each room.
Continuous photographic collage, no white frames.

Upper-left quadrant - KITCHEN: Marble countertops with visible 
veining and subtle etching from use, aged brass fixtures with 
dielectric reflection, herringbone oak floor with wear in traffic 
paths. Gallery curator markers: cookbook collection, ceramic 
pour-over coffee setup. Shot with 24mm lens at f/8, waist level. 
Negative space in Grid Zone 4+7 for Styler placement.
View crops naturally at wall edge.

Upper-right quadrant - LIVING: Camel velvet sofa anchoring the 
room, cream plaster walls with picture rail, Persian rug with 
forest green tones, aged brass floor lamp casting warm pool. 
Art books stacked on marble coffee table, small sculpture on 
console. Herringbone oak floor with satin varnish showing subtle 
wear. Shot with 24mm at f/8, waist level emphasizing ornate 
ceiling medallion. Negative space in Grid Zone 5+6 for TV placement.
Frame terminates at architectural corner.

Lower-left quadrant - BEDROOM: Linen bedding in ivory with 
gentle wrinkles, cashmere throw in camel at foot, oak nightstand 
with brass reading lamp. Sub-surface scattering visible in backlit 
sheer curtains. Book and reading glasses on nightstand suggesting 
curator's evening routine. Shot with 50mm at f/4, low angle 60cm, 
shallow DOF. Natural crop at doorframe boundary.

Lower-right quadrant - LAUNDRY: Functional space with white subway 
tile showing grout shadows, polished concrete floor with wet-look 
reflection. Metal shelving with natural wrinkling linen towels. 
Shot with 24mm, straight-on functional angle.
Negative space in Grid Zone 7+8 for washer/dryer placement.
Edge fades at room perimeter.

Empty uninhabited space. Curated comfortable living, edited but personal, 
tasteful accumulation. Golden hour 
atmosphere with dust motes in light shafts. Cross-quadrant anchor: 
aged brass floor lamp visible from living room doorway in bedroom 
quadrant, Persian rug edge visible in both living and kitchen.
Atmospheric perspective with three-layer depth. Optimistic warmth 
with human-centric lived-in quality. Same tree species visible 
through all windows, overcast winter sky.
Phase One IQ4, 8K. Square 1:1 format.
```

[네거티브 프롬프트 - TARGET_MODEL]
[파라미터 문법: MIDJOURNEY / STABLE_DIFFUSION]
--no white borders, dividing lines, frames between quadrants,
visible grid lines, separation marks, panel borders, white frames,
people, text, watermark, logo, competitor products, messy, dirty

[서술 문법: DALLE / IMAGEN / GENERIC]
No white borders, no quadrant dividers, no panel frames.
No visible grid lines, no text, watermark, logo, or people.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# ----------------------------------------
# 섹션 12: 고급 물리 시스템 신규 v5.5
# ----------------------------------------

## §12.1 재질 물리 엔진

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🪨 MATERIAL PHYSICS ENGINE FOR INTERIORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
소재별 물리적 특성을 프롬프트로 변환
→ AI가 현실적인 질감, 반사, 투과를 생성하도록 유도

[STONE & MINERAL]
─────────────────────────────────────────────────────────────────
CARRARA MARBLE (카라라 대리석)
• IOR: 1.55 | Roughness: 0.2-0.4 | SSS: 0.05
• PROMPT: "Polished Carrara marble with subtle grey veining, 
  soft luminous depth where light penetrates surface, gentle 
  reflection of surroundings, visible crystalline highlights"

CALACATTA GOLD (칼라카타 골드)
• IOR: 1.55 | Roughness: 0.15 | SSS: 0.03
• PROMPT: "Luxurious Calacatta marble with dramatic gold and 
  grey veining on white base, high polish reflecting room like 
  soft mirror, veins creating natural artwork patterns"

HONED MARBLE (호닝 대리석)
• IOR: 1.55 | Roughness: 0.5-0.7 | SSS: 0.02
• PROMPT: "Honed matte marble with soft velvety appearance, 
  no sharp reflections, veining visible but subdued, tactile 
  quality inviting touch"

TERRAZZO (테라조)
• IOR: 1.50 | Roughness: 0.3
• PROMPT: "Polished terrazzo with visible marble and stone 
  chips in cement base, each chip catching light differently, 
  overall surface semi-reflective"

CONCRETE (콘크리트)
• IOR: 1.45 | Roughness: 0.7-0.9
• PROMPT: "Raw concrete with visible form marks, subtle tonal 
  variation, matte surface absorbing light, occasional 
  aggregate visible, industrial warmth"

[WOOD]
─────────────────────────────────────────────────────────────────
OAK SATIN (오크 새틴)
• IOR: 1.47 | Roughness: 0.4
• PROMPT: "European oak with visible grain running lengthwise, 
  satin polyurethane finish showing subtle sheen, warm honey 
  to golden tones, grain texture tactile"

WALNUT OILED (월넛 오일드)
• IOR: 1.47 | Roughness: 0.5
• PROMPT: "American black walnut with deep chocolate tones, 
  natural oil finish creating depth without gloss, dramatic 
  grain patterns, purple undertones"

HERRINGBONE OAK (헤링본 오크)
• IOR: 1.47 | Roughness: 0.35
• PROMPT: "Herringbone parquet oak floor, each plank catching 
  light at different angle creating tonal variation, warm 
  honey color, visible wear in paths"

WHITEWASHED WOOD (화이트워시)
• IOR: 1.47 | Roughness: 0.6
• PROMPT: "Whitewashed wood with grain texture visible through 
  matte white pigment, Scandinavian feel, soft diffused 
  appearance, no reflection"

RECLAIMED WOOD (리클레임드)
• IOR: 1.47 | Roughness: 0.8
• PROMPT: "Reclaimed wood with visible history - nail holes, 
  weathering marks, mixed patina, matte aged surface, 
  authentic character imperfections"

[METAL]
─────────────────────────────────────────────────────────────────
POLISHED BRASS (광택 황동)
• IOR: Complex (metal) | Roughness: 0.1
• PROMPT: "Polished brass with warm golden mirror-like 
  reflection, room clearly visible in surface, rich warm 
  tone casting golden tint on surroundings"

AGED BRASS (에이지드 황동)
• IOR: Complex | Roughness: 0.4-0.6
• PROMPT: "Aged brass with natural patina, areas of polish 
  remaining, green-brown oxidation in crevices, authentic 
  aged character, soft diffused reflection"

BRUSHED STEEL (브러시드 스틸)
• IOR: Complex | Anisotropy: 0.8
• PROMPT: "Brushed stainless steel with visible directional 
  grain, reflections stretched along brush direction, 
  professional kitchen aesthetic"

MATTE BLACK STEEL (매트 블랙 스틸)
• IOR: Complex | Roughness: 0.9
• PROMPT: "Matte black powder-coated steel, absorbing light 
  with minimal reflection, industrial modern aesthetic, 
  subtle texture visible in highlights only"

COPPER (코퍼)
• IOR: Complex | Roughness: 0.15
• PROMPT: "Polished copper with rose-gold warm reflections, 
  hints of orange-pink in highlights, room reflected with 
  warm color cast"

[TEXTILES]
─────────────────────────────────────────────────────────────────
VELVET (벨벳)
• Roughness: Direction-dependent (nap)
• PROMPT: "Luxurious velvet with visible nap creating tonal 
  variation by angle, rich depth of color, light absorbed 
  then released as soft glow, tactile quality in drape"

LINEN (리넨)
• Roughness: 0.8 | SSS: 0.1 (backlit)
• PROMPT: "Natural linen with visible crossweave texture, 
  gentle wrinkles catching light, slight translucency when 
  backlit, organic imperfect beauty"

CASHMERE (캐시미어)
• Roughness: 0.7 | SSS: 0.15
• PROMPT: "Cashmere throw with incredibly soft appearance, 
  subtle halo of fibers in backlight, gentle drape suggesting 
  lightweight luxury, muted luster"

LEATHER (가죽)
• IOR: 1.45 | Roughness: 0.5
• PROMPT: "Full-grain leather with visible pores and natural 
  texture, developed patina showing character, subtle sheen 
  on high points, rich depth of color"

SILK CURTAINS (실크 커튼)
• IOR: 1.52 | SSS: 0.2 | Roughness: 0.3
• PROMPT: "Silk curtains with luminous translucency, light 
  passing through creating glow, subtle sheen on folds, 
  elegant drape pooling at floor"

[GLASS & CERAMIC]
─────────────────────────────────────────────────────────────────
CLEAR GLASS (투명 유리)
• IOR: 1.52 | Roughness: 0.02 | Transmission: 95%
• PROMPT: "Crystal clear glass with minimal distortion, sharp 
  reflections on surface, view through with slight color 
  shift, visible thickness at edges"

FROSTED GLASS (불투명 유리)
• IOR: 1.52 | Roughness: 0.6 | Transmission: Diffused
• PROMPT: "Frosted glass diffusing light into soft glow, 
  shapes visible but undefined beyond, matte surface 
  scattering reflections"

GLAZED CERAMIC (유약 세라믹)
• IOR: 1.55 | Roughness: 0.1
• PROMPT: "Glazed ceramic with glossy surface, color visible 
  through transparent glaze layer, sharp reflections, 
  handmade variation"

MATTE CERAMIC (무광 세라믹)
• IOR: 1.50 | Roughness: 0.8
• PROMPT: "Matte ceramic with chalky tactile surface, 
  absorbing light, subtle texture visible, minimalist 
  Scandinavian aesthetic"
```

---

## §12.2 대기 원근 시스템

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌫️ ATMOSPHERIC PERSPECTIVE - THREE-LAYER DEPTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
공기 원근법: 거리 증가 → 선명도↓, 채도↓, 푸른기↑, 대비↓

[THREE-LAYER STRUCTURE]
─────────────────────────────────────────────────────────────────
CAMERA ──────────────────────────────────────────────→ DEPTH

[LAYER 1]        [LAYER 2]         [LAYER 3]
FOREGROUND       MIDGROUND          BACKGROUND
0-2 meters       2-5 meters         5+ meters

┌─────────┐     ┌─────────┐        ┌─────────┐
│ SHARP   │     │ SLIGHT  │        │ SOFT    │
│ VIBRANT │     │ SOFTEN  │        │ HAZY    │
│ HIGH    │     │ MEDIUM  │        │ LOW     │
│ CONTRAST│     │ CONTRAST│        │ CONTRAST│
└─────────┘     └─────────┘        └─────────┘

[LAYER 1: FOREGROUND] 0-2m
─────────────────────────────────────────────────────────────────
• Sharpness: 100% | Saturation: 100% | Contrast: Full
• Detail: Maximum - individual threads visible
• Color: True color, no atmospheric shift
• Elements: Product, foreground furniture, nearest plants
• PROMPT: "Razor-sharp foreground with full color saturation, 
  every texture visible, immediate elements in tack-sharp focus"

[LAYER 2: MIDGROUND] 2-5m
─────────────────────────────────────────────────────────────────
• Sharpness: 85-95% | Saturation: 90-95% | Contrast: Med-High
• Detail: Good - overall texture, not individual fibers
• Color: Slight warmth or cool shift by time
• Elements: Sofa, lamps, wall art, doorframes
• PROMPT: "Midground with subtle air volume, slightly softened 
  detail maintaining form, gentle luminosity between layers"

[LAYER 3: BACKGROUND] 5m+
─────────────────────────────────────────────────────────────────
• Sharpness: 60-80% | Saturation: 80-90% | Contrast: Reduced
• Detail: General shapes, no fine detail
• Color: Blue shift (daylight) or warm shift (tungsten)
• Elements: Far walls, windows, hallways, ceiling
• PROMPT: "Background softly veiled in atmospheric haze, 
  reduced contrast, subtle blue-shift from aerial perspective"

[ROOM SIZE CALIBRATION]
─────────────────────────────────────────────────────────────────
┌─────────────────┬───────────────────────────────────────────────┐
│ HOUSING TYPE    │ ATMOSPHERIC INTENSITY                         │
├─────────────────┼───────────────────────────────────────────────┤
│ STUDIO (20-35㎡)│ MINIMAL - "Shallow DOF only, no aerial        │
│                 │ perspective in compact space"                 │
├─────────────────┼───────────────────────────────────────────────┤
│ APARTMENT       │ SUBTLE - "Barely perceptible background       │
│ (60-90㎡)       │ softening with slight cool shift"             │
├─────────────────┼───────────────────────────────────────────────┤
│ VILLA           │ MODERATE - "Clear three-layer depth,          │
│ (120-200㎡)     │ foreground sharp, background with haze"       │
├─────────────────┼───────────────────────────────────────────────┤
│ LOFT            │ FULL - "Pronounced atmospheric perspective,   │
│ (150-300㎡)     │ distant ceiling fading into luminous haze"    │
└─────────────────┴───────────────────────────────────────────────┘

[LIGHTING VARIATIONS]
─────────────────────────────────────────────────────────────────
DAYLIGHT (5500-6500K):
• "Distant elements with subtle cool cast from scattered daylight"

GOLDEN HOUR (2700-3500K):
• "Far walls bathed in warm atmospheric glow, dust motes visible"

TUNGSTEN (2700K):
• "Background with warm tungsten falloff, shadows to warm umber"

OVERCAST (5000-6000K):
• "Even atmospheric softening without strong color shift"

NIGHT/LAMPS:
• "Distant areas falling into warm shadow, pools of lamp light"
```

---

## §12.3 엔트로피 레벨 시스템(1-10)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 ENTROPY LEVEL SYSTEM - OBJECT DENSITY CONTROL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Entropy = 공간의 물건 밀도 + 생활 흔적 정도
낮음(1) = 미니멀 쇼룸 / 높음(10) = 맥시멀 리빙
출력에는 숫자 대신 각 LEVEL의 PROMPT 문장을 그대로 사용

[LEVEL 1-2: ULTRA MINIMAL]
─────────────────────────────────────────────────────────────────
• Objects: 3-5 items per room | Coverage: <10%
• Character: Gallery-like, almost sterile
• Elements: Single furniture, one lamp, maybe one plant
• PROMPT: "Ultra-minimal gallery-like space with only essential 
  furniture, stark minimalism, negative space dominates, 
  zen-like emptiness, each object deliberately placed"
• Use for: Showroom shots, product hero focus

[LEVEL 3-4: MINIMAL CLEAN]
─────────────────────────────────────────────────────────────────
• Objects: 8-12 items per room | Coverage: 15-25%
• Character: Edited, intentional, magazine-ready
• Elements: Main furniture, 2-3 decor, small book stack, one plant
• PROMPT: "Clean minimal living with carefully edited objects, 
  Scandinavian simplicity, few but quality pieces, uncluttered 
  surfaces, every item earns its place"
• Use for: Modern apartment, architect portfolio

[LEVEL 5-6: CURATED COMFORTABLE] ⭐DEFAULT
─────────────────────────────────────────────────────────────────
• Objects: 15-25 items per room | Coverage: 30-45%
• Character: Lived-in but organized, editorial lifestyle
• Elements: Full furniture, multiple decor, books, 2-3 plants, 
  personal items, subtle life signs (blanket draped, magazine open)
• PROMPT: "Curated comfortable living, edited but personal, 
  tasteful accumulation telling life story, organized abundance"
• Use for: Lifestyle campaigns, real estate luxury ⭐MOST COMMON

[LEVEL 7-8: COLLECTED ABUNDANCE]
─────────────────────────────────────────────────────────────────
• Objects: 30-50 items per room | Coverage: 50-65%
• Character: Rich, layered, collector's home
• Elements: Dense furniture, multiple art, full bookshelves, 
  collections, many plants, layered textiles, photos
• PROMPT: "Collected abundance with every surface telling stories, 
  rich layered interior of passionate collector, bohemian 
  intellectual density, curated accumulation"
• Use for: Artistic personality, writer/musician home

[LEVEL 9-10: MAXIMALIST ECLECTIC]
─────────────────────────────────────────────────────────────────
• Objects: 60+ items per room | Coverage: 70-85%
• Character: Maximalist, dramatic, every surface alive
• Elements: Gallery wall covered, dense furniture, books everywhere, 
  abundant plants, pattern mixing, controlled creative chaos
• PROMPT: "Maximalist paradise, more-is-more philosophy, every 
  surface alive with treasures, fearless pattern mixing"
• Use for: Fashion designer, artist studio
• ⚠️ WARNING: May compete with LG product visibility

[OCCUPATION → ENTROPY MAPPING]
─────────────────────────────────────────────────────────────────
┌──────────────────┬─────────┬────────────────────────────────────┐
│ OCCUPATION       │ LEVEL   │ RATIONALE                          │
├──────────────────┼─────────┼────────────────────────────────────┤
│ Architect        │ 3-4     │ Deliberate minimal, form focus     │
│ Surgeon          │ 4-5     │ Clean, organized, precise          │
│ Software Engineer│ 4-5     │ Functional minimal, tech focus     │
│ Gallery Curator  │ 5-6     │ Curated, art-focused               │
│ Chef             │ 5-6     │ Organized but tool-rich            │
│ Photographer     │ 5-7     │ Equipment + art displayed          │
│ Writer           │ 6-8     │ Books abundant, creative mess      │
│ Musician         │ 6-8     │ Instruments, vinyl, layers         │
│ Fashion Designer │ 7-9     │ Fabrics, mood boards, color        │
│ Antique Dealer   │ 8-10    │ Maximum collection display         │
└──────────────────┴─────────┴────────────────────────────────────┘

[ENTROPY × ROOM TYPE MATRIX]
─────────────────────────────────────────────────────────────────
           KITCHEN   LIVING   BEDROOM   BATHROOM   LAUNDRY
Level 3      ✅         ✅        ✅         ✅          ✅
Level 5      ✅         ✅        ✅         ⚠️          ✅
Level 7      ⚠️         ✅        ⚠️         ❌          ⚠️
Level 9      ❌         ⚠️        ❌         ❌          ❌

✅ = Natural | ⚠️ = Use with caution | ❌ = Avoid
```

---

## §12.4 크로스 패널 앵커 시스템

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 CROSS-PANEL ANCHOR SYSTEM - 4분할 일관성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4개 quadrant가 "같은 집"임을 증명하는 시각적 앵커

[ANCHOR SELECTION RULE]
─────────────────────────────────────────────────────────────────
1. 직업 마커 중 가장 크고 독특한 오브젝트 선택
2. 최소 2개 quadrant에 등장
3. 전경/배경 번갈아 배치
4. 동일한 조명 상태 유지

[PRIMARY ANCHORS - 권장]
─────────────────────────────────────────────────────────────────
┌──────────────────┬───────────────────────────────────────────────┐
│ ANCHOR TYPE      │ VISIBILITY DESCRIPTION                        │
├──────────────────┼───────────────────────────────────────────────┤
│ Floor Lamp       │ "Aged brass floor lamp visible in living      │
│ (플로어 램프)    │ (foreground) and glimpsed through bedroom     │
│                  │ doorway (background)"                         │
├──────────────────┼───────────────────────────────────────────────┤
│ Area Rug         │ "Persian rug edge visible in living room      │
│ (러그)           │ and continuing into kitchen threshold"        │
├──────────────────┼───────────────────────────────────────────────┤
│ Plant            │ "Large fiddle leaf fig in living corner,      │
│ (대형 식물)      │ same plant's leaves peeking into bedroom"     │
├──────────────────┼───────────────────────────────────────────────┤
│ Artwork          │ "Gallery wall visible from living, reflected  │
│ (아트워크)       │ in kitchen window glass"                      │
├──────────────────┼───────────────────────────────────────────────┤
│ Hallway View     │ "Same hallway visible from kitchen and        │
│ (복도 시야)      │ bedroom doorframes"                           │
└──────────────────┴───────────────────────────────────────────────┘

[SECONDARY ANCHORS - 지원]
─────────────────────────────────────────────────────────────────
• CEILING: "Same ceiling height and molding pattern across all"
• FLOORING: "Herringbone oak continues from living to kitchen"
• WALL COLOR: "Same cream #F5F5DC plaster throughout"
• WINDOW TYPE: "Identical French window style in all rooms"

[OCCUPATION-SPECIFIC ANCHOR EXAMPLES]
─────────────────────────────────────────────────────────────────
GALLERY CURATOR:
Primary: Aged brass floor lamp with gallery arm
Secondary: Art books visible in living + bedroom
Prompt: "Distinctive museum-style brass floor lamp in living room 
foreground, same lamp's glow visible through bedroom doorway"

ARCHITECT:
Primary: Scale model on console
Secondary: Drafting tools visible across rooms
Prompt: "Architectural model on living room console, same white 
plaster model visible in background of kitchen view"

CHEF:
Primary: Copper pot collection
Secondary: Herb plants on multiple windowsills
Prompt: "Copper cookware hanging in kitchen, one copper pot 
visible on living room side table with flowers"

[PROMPT TEMPLATE]
─────────────────────────────────────────────────────────────────
"Cross-quadrant anchor: [PRIMARY_ANCHOR] visible in [ROOM_A] 
(foreground) and glimpsed in [ROOM_B] (background through 
doorway/reflection). [SECONDARY_ANCHOR] continues across 
[ROOM_C] and [ROOM_D] threshold. Same architectural details 
throughout confirming single residence."
```

---

# ═══════════════════════════════════════════════════════════════
# 부록: 광학 리얼리즘(요약)
# ═══════════════════════════════════════════════════════════════

```
0.5% Optical Realism은 내부 품질 기준이며 물리적 일관성과 미세 텍스처를 우선한다.
과도한 샤프닝/미세 패턴 강조는 금지한다.
```

---

# ═══════════════════════════════════════════════════════════════
# 버전 히스토리
# ═══════════════════════════════════════════════════════════════

```
STEP 2 v5.9.0 [FINAL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHANGES FROM v5.8:
* 결과 표시용 마크다운 출력 형식 추가 (Exterior/Interior)

STEP 2 v5.8 [FINAL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHANGES FROM v5.7:
* GLOBAL 표기 제거 및 로컬 락 명세로 통합
* camera_meta 단일 필드(default/overrides)로 통합
* MANIFEST 출력 본문 제거 (별도 가이드 유지)
* 토큰 라우팅 주석 + Nano Banana 핸드오프 예시 추가
* GREETING 축약, 외부 락/프롬프트 템플릿 간결화
* 0.5% Optical Realism 본문 제거 → 부록 2줄 요약

STEP 2 v5.7 [FINAL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHANGES FROM v5.6:
* Step 2 JSON에 room_target / single_room_prompt / negative_space_description 추가
* schemas/LG_Step2_Schema_v1.1.json 정합성 반영
* 4-Quadrant 네거티브 프롬프트 TARGET_MODEL 분기
* NANO_BANANA 모드 입력 규칙 추가

STEP 2 v5.6 [FINAL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHANGES FROM v5.5.1:
* Manifest 출력은 LG_Manifest_Output_Guide_v1.0.md로 분리

CHANGES FROM v5.5:
* STEP2_JSON 스키마 준수 요청사항 추가

CHANGES FROM v5.4:
* §0.5 TARGET_MODEL 추가 (플랫폼별 네거티브 문법 분기)
* §6.2 Entropy 숫자 대신 설명문 출력 강제
* schema_version 5.5로 정합성 갱신

CHANGES FROM v5.2.1:
* §12.1 MATERIAL PHYSICS ENGINE 신규 추가
  - Stone/Mineral: 5가지 (Marble, Terrazzo, Concrete)
  - Wood: 5가지 (Oak, Walnut, Herringbone, Whitewash, Reclaimed)
  - Metal: 5가지 (Brass, Steel, Copper)
  - Textiles: 5가지 (Velvet, Linen, Cashmere, Leather, Silk)
  - Glass/Ceramic: 4가지
  - 각 소재별 IOR, Roughness, SSS 물리값 + 프롬프트
* §12.2 ATMOSPHERIC PERSPECTIVE 신규 추가
  - 3-Layer Depth System (Foreground/Midground/Background)
  - Room Size Calibration (Studio → Loft)
  - Lighting Variation별 색상 시프트
* §12.3 ENTROPY LEVEL SYSTEM 신규 추가
  - Level 1-10 상세 정의
  - 오브젝트 수량/커버리지 기준
  - Occupation → Entropy 자동 매핑
  - Room Type × Entropy 적합성 매트릭스
* §12.4 CROSS-PANEL ANCHOR SYSTEM 신규 추가
  - Primary/Secondary Anchor 선택 규칙
  - Occupation별 앵커 예시
  - 프롬프트 템플릿

CHANGES FROM v5.2:
* §2.5 SEAMLESS QUAD COMPOSITION (경계선 없는 4분할)
* §6.2-6.3 경계선 없는 템플릿
* §8, §10, §11 경계선 방지 강화
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 12 Sections + 4 Advanced Physics Systems
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```





