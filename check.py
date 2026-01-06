import os
import google.generativeai as genai

MY_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not MY_API_KEY:
    raise SystemExit("GOOGLE_API_KEY 환경변수가 필요합니다.")

genai.configure(api_key=MY_API_KEY)

print("--- 사용 가능한 모델 목록 ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"에러 발생: {e}")
print("---------------------------")
