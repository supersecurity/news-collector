import os
import sys
import requests

def verify_token():
    token = os.environ.get("NOTION_TOKEN", "")
    
    # 기본 검증
    if not token:
        print("::error::NOTION_TOKEN environment variable is not set")
        sys.exit(1)
    
    # 디버그 정보 (안전하게)
    print(f"Token starts with: {token[:4]}...")  # rtn_만 표시
    print(f"Token length: {len(token)}")
    
    # 토큰 형식 검증
    if not token.startswith("rtn_"):
        print(f"::error::Token prefix invalid. Expected 'rtn_', got '{token[:4]}'")
        sys.exit(1)
    
    # API 요청 테스트
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            "https://api.notion.com/v1/users/me",
            headers=headers
        )
        
        if response.status_code == 200:
            print("Token verification successful!")
            return True
        else:
            print(f"::error::API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"::error::Request failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    verify_token()
