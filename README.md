# Prompt Optimizer Proxy 🚀

비용 절감을 위해 LLM 프롬프트를 실시간으로 압축하는 오픈소스 미들웨어 프록시 서버입니다. 
Microsoft의 **LLMLingua**를 내장하여 OpenAI API 호출 전 텍스트의 의미를 유지하며 길이를 40~50% 줄여줍니다.

## 주요 기능
- **자동 프롬프트 압축**: OpenAI API 요청을 중간에서 가로채 의미론적 압축을 수행합니다.
- **Drop-in 교체**: 기존 코드에서 `Base URL`만 변경하여 즉시 적용 가능합니다.
- **실시간 대시보드**: 절감된 토큰 수와 예상 절약 비용을 시각화하여 확인합니다.
- **B2B 특화**: 기업 내부 서버에 설치하여 API 비용을 획기적으로 줄일 수 있습니다.

## 시작하기

### 1. 환경 설정
`.env` 파일을 생성하고 OpenAI API 키를 입력하세요.
```env
OPENAI_API_KEY=your_api_key_here
COMPRESSION_ENABLED=True
COMPRESSION_RATE=0.5
```

### 2. 서버 실행
```bash
# 가상환경 활성화 후
uvicorn app.main:app --reload --port 8000
```

### 3. 클라이언트 연결
OpenAI SDK 사용 시 `base_url`을 다음과 같이 변경합니다.
```python
client = OpenAI(
    api_key="your_key",
    base_url="http://localhost:8000/v1"  # 미들웨어 주소로 변경
)
```

## 모니터링
서버 실행 후 브라우저에서 `http://localhost:8000/dashboard`에 접속하여 실시간 절감 현황을 확인하세요.

## 기술 스택
- **Framework**: FastAPI
- **Compression**: Microsoft LLMLingua
- **Database**: SQLite / SQLAlchemy
- **UI**: Jinja2 / Pure CSS
