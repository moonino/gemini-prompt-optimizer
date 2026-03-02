import requests
import json

def test_proxy():
    url = "http://localhost:8000/v1/chat/completions"
    
    # 꽤 긴 예시 텍스트 (RAG 상황을 가정한 배경지식 포함)
    long_prompt = """
    다음은 프랑스 축구 클럽 RC 랑스(Racing Club de Lens)에 대한 상세 정보입니다. 
    이 팀은 프랑스 북부 랑스를 연고로 하며, 1906년에 창단되었습니다. 
    홈 경기장은 스타드 볼라르트 델렐리스로, 도시 인구보다 경기장 수용 인원이 더 많은 것으로 유명합니다.
    최근 프랑크 에즈 감독 체제에서 3-4-3 또는 3-5-2 전술을 활용하여 리그 1에서 돌풍을 일으켰습니다.
    압박축구와 빠른 공수 전환이 특징이며, 서포터들의 열기가 매우 뜨겁기로 소문나 있습니다.
    ... (중략) ...
    질문: RC 랑스의 주요 전술적 특징과 연고지의 특징을 요약해줘.
    """
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "너는 유능한 축구 전문가야."},
            {"role": "user", "content": long_prompt}
        ]
    }
    
    print("--- 최적화 프록시로 요청을 보내는 중... ---")
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("성공적으로 답변을 받았습니다!")
            print(f"답변 내용 요약: {response.json()['choices'][0]['message']['content'][:100]}...")
            print("\n대시보드(http://localhost:8000/dashboard)에서 절감 내역을 확인하세요.")
        else:
            print(f"에러 발생: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"연결 실패: {e}\n서버(uvicorn)가 실행 중인지 확인하세요.")

if __name__ == "__main__":
    test_proxy()
