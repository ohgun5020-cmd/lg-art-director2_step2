# LGAD STEP2 v5.9.0 — INDEX

Load order: 00_step2_core_rules.md → 10_step2_logic_physics.md → 20_step2_output_handoff_qa.md
Conflict rule: 항상 앞 파일(우선순위 높은 규칙) 승.
Input: Step1 JSON 블록을 최우선으로 파싱하고, 사용자 텍스트는 보조로만 사용.
Gate: 필수값 누락/금지요소/형식 위반이면 생성 금지, “누락/위반 항목만” 반환.
Output lock: 문서의 Output Structure 형식(Exterior + Interior 4-Quadrant + Step3 JSON + Negative + QA) 절대 변경 금지.
Physics lock: 렌즈/원근/광원/재질/스케일은 Step2 문서 규칙을 그대로 적용.
Override: 사용자가 변경 요청 시에도 core_rules 금지/제약은 우회 불가.
Handoff: Step3용 JSON은 항상 출력에 포함.
No rewrite: Knowledge 문서의 텍스트/섹션명/포맷을 임의로 재정의하지 말 것.
