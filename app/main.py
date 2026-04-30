from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.spam import check_spam
from pydantic import BaseModel
import logging
from app.issue import *
import traceback

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | %(levelname)s | "
        "%(filename)s:%(lineno)d (%(funcName)s) | "
        "%(message)s"
    )
)
logger = logging.getLogger("spamcheck")

# FastAPI 기반 웹앱 생성
# /docs (Swagger UI)에 표기되는 이름
app = FastAPI(title="SpamCheck Web")

# 정적 HTML 서빙: static 안에 파일들을 URL로 접근 가능하게 해라
# {URL}/static/... 으로 접근 가능하게
app.mount("/static", StaticFiles(directory="static"), name="static")


# 메인 페이지(/) 처리: "/"로 접속 시 처리할 작업
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

class ClassifyRequest(BaseModel):
    text: str

# classify 요청이 올 때 할 일
# async: 비동기 처리 (서버가 요청 기다리는 동안 다른 요청도 처리 가능)
@app.post("/classify")
# async def classify(request: Request):
#     payload = await request.json()
@app.post("/classify")
async def classify(payload: ClassifyRequest):
    text = payload.text
    
    # (A) 요청 기록: 언제(로그시간) / 무엇(endpoint) / 어떤입력
    logger.info(f"CALL /classify | text='{text}' | len={len(text)}")
    
    try:
        if text == "crash":
            raise RuntimeError("의도적 장애 추가")
            
        label, score = check_spam(text)
        
        # (B) 정상 처리 결과 기록
        logger.info(f"OK /classify | label={label} score={score}")
        
        # 정상 반환 (try 블록 안에서 결과가 있을 때 실행)
        return {
            "label": label, 
            "score": score
        }

    except Exception as e:
        # (C) 디버깅 핵심: 에러 종류/메시지 + 스택트레이스 기록
        # logger.exception은 현재 예외의 traceback을 자동으로 로그에 포함합니다.
        logger.exception(
            f"FAIL /classify | text='{text}' | error={type(e).__name__}: {e}"
        )

        # (D) GitHub Issue 자동 생성 로직
        # 전체 스택트레이스 내용을 문자열로 가져옵니다.
        tb = traceback.format_exc()
        title = f"[Prod Error] /classify failed: {type(e).__name__}"
        body = (
            f"## Summary\n"
            f"- endpoint: /classify\n"
            f"- input(text, short): `{text}`\n"
            f"- input length: {len(text)}\n\n"
            f"## Exception\n"
            f"- type: {type(e).__name__}\n"
            f"- message: {str(e)}\n\n"
            f"## Traceback (line info)\n"
            f"```text\n{tb}\n```"
        )
        
        # 앞서 정의한 GitHub Issue 생성 함수 호출
        create_github_issue(title, body, logger)

        # (E) 사용자 응답은 상세한 에러 대신 심플하게 반환
        return {"label": "Internal Server Error", "score": -1}


# 실행은 운영환경의 책임으로 남기기 위해 만들지 X
# http://127.0.0.1:8000 접속
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
