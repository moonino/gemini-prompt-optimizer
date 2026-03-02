# Lightweight Prompt Optimizer 🔥 (Gemini Native Edition)

[![Python Support](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker Support](https://img.shields.io/badge/Docker-Supported-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"API 요금을 반토막 내는 가장 쉬운 방법"**
>
> 기존 Gemini API 호출 코드에서 URL 단 **한 줄만 변경**하세요. 로컬 프록시가 무거운 딥러닝 없이 초경량 NLP 엔진으로 프롬프트를 압축하여 전달합니다.

---

## 📖 목차
1. [왜 이 프로젝트가 필요한가요? (Why)](#-왜-이-프로젝트가-필요한가요)
2. [어떻게 작동하나요? (How it works)](#-어떻게-작동하나요)
3. [주요 기능 (Features)](#-주요-기능)
4. [빠른 시작 (Quick Start)](#-빠른-시작)
5. [사용 방법 (Usage)](#-사용-방법)
6. [대시보드 (Dashboard)](#-대시보드)

---

## ❓ 왜 이 프로젝트가 필요한가요?

AI 서비스를 기획하거나 RAG(Retrieval-Augmented Generation) 시스템을 만들 때, 방대한 문서를 AI 모델의 컨텍스트 창에 우겨넣으면 **막대한 API 비용**이 발생합니다.

**Lightweight Prompt Optimizer**는 무거운 ML 모델 연산을 없애고 오직 파이썬 네이티브 종속성(`re`, `NLTK`, `NetworkX`)만으로 0.1초 만에 텍스트의 핵심만 추출합니다. 

* 📉 **비용 절감**: 평균 **15% ~ 50%**의 API 비용(토큰)을 즉각적으로 절약합니다.
* 🚀 **응답 시간 향상**: 가벼워진 프롬프트 덕분에 Gemini 모델의 답변 속도 가 획기적으로 향상됩니다.
* 🔌 **Zero Code Change**: 여러분의 비즈니스 로직(Node.js, Spring, Python)을 고칠 필요가 전혀 없습니다.

---

## ⚙️ 어떻게 작동하나요?

1. **Client**가 로컬 프록시로 Native Gemini API 포맷의 요청을 보냅니다.
2. 프록시 내부의 **Lightweight NLP 논리망**을 거칩니다:
   * **1단계 (Regex)**: 의미 없는 HTML/Markdown 태그, 다중 공백 및 불필요한 줄바꿈 제거
   * **2단계 (TextRank)**: `NetworkX` 페이지랭크 알고리즘으로 문서 내 핵심 문장(키워드)만 추출
   * **3단계 (NLTK)**: 의미를 해치지 않는 선에서 불용어(Stopwords, 조사/접속사) 제거
3. **50% 압축된 텍스트**가 진짜 Gemini API로 전송되고, Google의 응답이 Client에게 릴레이됩니다.

---

## 🌟 주요 기능

* **100% 안정성**: 기존 LLMLingua 같은 딥러닝 종속성이 없어서 `500 Server Error`나 `CUDA OOM` 같은 메모리 충돌이 절대 발생하지 않습니다.
* **Gemini Native API 지원**: `gemini-2.5-flash`, `gemini-2.5-pro` 등 최신 모델 라인업의 공식 GenerateContent 규격을 완벽 지원합니다.
* **시각화 대시보드 내장**: 이번 달 내가 얼마나 API 비용을 아꼈는지 SQLite 기반의 멋진 차트로 조회할 수 있습니다.

---

## 🚀 빠른 시작

### 1단계: API 키 설정
`.env.example`을 복사하여 `.env` 파일을 만들고 Gemini API 키를 넣습니다.
```bash
cp .env.example .env

# .env 파일 내부
GEMINI_API_KEY="AI Studio에서 발급받은 실제 API 키 입력"
COMPRESSION_ENABLED=True
COMPRESSION_RATE=0.5 # 50% 압축
```

### 2단계: 서버 실행 (Docker 추천 🐳)
파이썬 환경 충돌 스트레스 없이 딱 한 줄로 실행하세요.
```bash
docker-compose up -d
```
*(백그라운드에서 조용히 실행되며 `localhost:8000`을 점유합니다.)*

---

## 💻 사용 방법 (Drop-in Replacement)

서버가 켜졌다면, 여러분의 기존 코드에서 **엔드포인트(URL)만** 바꿔주시면 됩니다!

### � Python (Google GenAI SDK)
```python
import google.generativeai as genai
from google.api_core.client_options import ClientOptions

# 단 한줄의 설정 변경으로 프록시 우회
genai.configure(
    api_key="유효한_제미나이_키", 
    client_options=ClientOptions(api_endpoint="http://localhost:8000/v1")
)

model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content("여기 매우 긴 PDF나 책 내용을 붙여넣어보세요...")
print(response.text)
```

### 🌐 cURL (Native REST API 호환)
```bash
curl "http://localhost:8000/v1/models/gemini-2.5-flash:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: 내_API_키" \
  -d '{
    "contents": [{
      "parts": [{"text": "매우 긴 텍스트..."}]
    }]
  }'
```

---

## 📊 대시보드 (Dashboard)

서버 파이프라인의 절감 효과를 눈으로 직접 확인하세요.
웹 브라우저를 열고 👉 [http://localhost:8000/dashboard](http://localhost:8000/dashboard) 로 접속합니다.

* **실시간 누적 절감액(USD)** 및 토큰(Tokens) 카운터
* 모델별 사용 점유율 차트 (Chart.js)
* 최근 20건의 요청/압축 비교 트렌드 그래프

