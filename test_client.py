import requests
import json

DEFAULT_MODEL = "gemini-2.5-flash" # Latest Gemini 2.5 model

def test_proxy_native_gemini():
    # Native Gemini Endpoint through Proxy
    model = DEFAULT_MODEL
    url = f"http://127.0.0.1:8000/v1/models/{model}:generateContent"
    
    # Create a long, realistic text (Software Engineering / API Documentation context)
    base_text = "The new version of the API introduces several breaking changes. Endpoint /v1/users now requires a Bearer token in the Authorization header. The payload must be a JSON object containing 'user_id' and 'email'. Additionally, the rate limit has been reduced from 1000 to 500 requests per minute to ensure server stability during peak hours. Failure to comply will result in a 429 Too Many Requests response. Developers must migrate their code before the deprecation date next month. "
    long_prompt = base_text * 15
    long_prompt += "\n\nQuestion: What are the two main breaking changes introduced in the new API version? Please summarize in Korean."
    
    # Gemini Native Request Body
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": "너는 시니어 백엔드 AI 엔지니어야. 아래 영문 API 명세서를 읽고 질문에 정확하게 답해줘."},
                    {"text": long_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500
        }
    }
    
    print(f"--- [Native Gemini] 최적화 프록시({model})로 요청을 보내는 중... ---")
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print("성공적으로 답변을 받았습니다!")
            # Extract content from Gemini response structure
            if "candidates" in data and len(data["candidates"]) > 0:
                answer = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"답변 내용 요약: {answer[:100]}...")
            else:
                print("답변 구조가 예상과 다릅니다:", data)
            
            print("\n대시보드(http://localhost:8000/dashboard)에서 절감 내역을 확인하세요.")
        else:
            print(f"에러 발생: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"연결 실패: {e}\n서버(uvicorn)가 실행 중인지 확인하세요.")

if __name__ == "__main__":
    test_proxy_native_gemini()
