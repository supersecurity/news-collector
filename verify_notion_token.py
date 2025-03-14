import os
import sys
import requests

token = os.environ.get("NOTION_TOKEN", "")

if not token:
    print("::error::Notion token is not set")
    sys.exit(1)
    
if not token.startswith("rtn_"):
    print("::error::Notion token must start with rtn_")
    sys.exit(1)
    
if len(token) < 40 or len(token) > 50:
    print("::error::Notion token has an invalid length")
    sys.exit(1)
    
response = requests.get("https://api.notion.com/v1/users", 
                        headers={"Authorization": f"Bearer {token}",
                                 "Notion-Version": "2022-06-28"})

if response.status_code != 200:
    print(f"::error::Notion API request failed with status code {response.status_code}")
    sys.exit(1)

print("Notion token is valid")
