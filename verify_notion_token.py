import os
import sys
import requests

def verify_token():
    token = os.environ.get("NOTION_TOKEN", "")
    
    if not token:
        print("::error::Notion token is not set")
        sys.exit(1)
        
    if not token.startswith("ntn_"):
        print("::error::Notion token must start with ntn_")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(
            "https://api.notion.com/v1/users/me",
            headers=headers
        )
        if response.status_code != 200:
            print(f"::error::API verification failed: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"::error::Request failed: {str(e)}")
        sys.exit(1)

    print("Notion token verified successfully")

if __name__ == "__main__":
    verify_token()
