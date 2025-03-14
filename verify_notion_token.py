import os
import sys
import requests

def debug_token(token):
    print(f"Token prefix: '{token[:4]}'")
    print(f"Token length: {len(token)}")
    print(f"Token contains whitespace: {any(c.isspace() for c in token)}")

token = os.environ.get("NOTION_TOKEN", "")

# 디버깅 정보 출력
print("=== Debug Information ===")
if not token:
    print("Token is empty or not set")
else:
    debug_token(token)
print("========================")

if not token:
    print("::error::Notion token is not set")
    sys.exit(1)

# 토큰 앞뒤 공백 제거
token = token.strip()
    
if not token.startswith("ntn_"):
    print(f"::error::Token must start with 'ntn_' (current prefix: '{token[:4]}')")
    sys.exit(1)
    
if len(token) < 40 or len(token) > 50:
    print(f"::error::Token length ({len(token)}) is invalid (should be between 40 and 50)")
    sys.exit(1)

try:
    response = requests.get(
        "https://api.notion.com/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28"
        }
    )
    
    if response.status_code != 200:
        print(f"::error::API request failed with status {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)
        
except Exception as e:
    print(f"::error::Request failed: {str(e)}")
    sys.exit(1)

print("Notion token is valid")
