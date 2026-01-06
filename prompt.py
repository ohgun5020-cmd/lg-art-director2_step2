"""
LG Art Director System STEP 2 v5.9.0 - Prompt Loader
md 파일들을 읽어서 LG_SYSTEM_PROMPT로 조합
"""

import os
import re

# 프롬프트 파일 로드 순서 (INDEX_STEP2.md 기준)
PROMPT_FILES = [
    "00_step2_core_rules.md",
    "10_step2_logic_physics.md",
    "20_step2_output_handoff_qa.md",
]

# 현재 파일 기준 prompts 폴더 경로
PROMPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")

# HTML 코멘트 제거 패턴
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)


def load_prompt_file(filename: str) -> str:
    """단일 프롬프트 파일 로드 및 정리"""
    filepath = os.path.join(PROMPTS_DIR, filename)
    
    if not os.path.exists(filepath):
        return ""
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # HTML 코멘트 제거
    content = HTML_COMMENT_PATTERN.sub("", content)
    
    # 앞뒤 공백 정리
    content = content.strip()
    
    return content


def load_system_prompt() -> str:
    """모든 프롬프트 파일을 순서대로 로드하여 조합"""
    parts = []
    
    for filename in PROMPT_FILES:
        content = load_prompt_file(filename)
        if content:
            parts.append(content)
    
    if not parts:
        return "LG Art Director System STEP 2 v5.9.0 - Prompt files not found"
    
    # 구분자로 연결
    return "\n\n---\n\n".join(parts)


def get_version() -> str:
    """시스템 버전 반환"""
    return "5.9.0"


# 메인 export - app.py에서 import할 변수
LG_SYSTEM_PROMPT = load_system_prompt()
SYSTEM_VERSION = get_version()


if __name__ == "__main__":
    # 테스트용
    print(f"=== LG Art Director System STEP 2 v{SYSTEM_VERSION} ===")
    print(f"Loaded prompt length: {len(LG_SYSTEM_PROMPT)} chars")
    print(f"Prompt files: {PROMPT_FILES}")
    print("\n--- First 500 chars ---")
    print(LG_SYSTEM_PROMPT[:500])
