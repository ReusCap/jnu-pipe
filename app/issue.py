import os
import logging
import requests

def create_github_issue(title: str, body: str, logger) -> None:
    # 환경 변수에서 저장소와 토큰 정보 가져오기
    repo = os.getenv("GH_REPO")
    token = os.getenv("GH_TOKEN")
    
    # 토큰이나 저장소 설정이 없으면 경고 후 종료
    if not repo or not token:
        logger.warning("GH_REPO/GH_TOKEN not set; skipping GitHub issue creation.")
        return
    
    # GitHub API 엔드포인트 설정
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"title": title, "body": body}
    
    try:
        # POST 요청 보내기
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        
        # 상태 코드가 300 이상(에러)인 경우 기록
        if r.status_code >= 300:
            logger.warning(f"Failed to create issue: {r.status_code} {r.text[:200]}")
        else:
            logger.info(f"Successfully created GitHub issue in {repo}")
            
    except Exception as e:
        # 네트워크 타임아웃 등 예외 발생 시 기록
        logger.error(f"Error during GitHub issue creation: {e}")