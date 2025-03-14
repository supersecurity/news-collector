import os
import requests
from datetime import datetime
import pytz

def create_notion_page(title, url, summary, category):
    token = os.environ.get("NOTION_TOKEN")
    database_id = "1b5c077d6a0c802d8595d152ff4bb6d0"  # 데이터베이스 ID

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # 한국 시간대로 현재 시간 설정
    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "URL": {
                "url": url
            },
            "Summary": {
                "rich_text": [
                    {
                        "text": {
                            "content": summary
                        }
                    }
                ]
            },
            "Category": {
                "select": {
                    "name": category
                }
            },
            "Date": {
                "date": {
                    "start": current_time.split()[0]  # YYYY-MM-DD 형식
                }
            }
        }
    }

    try:
        response = requests.post(
            f"https://api.notion.com/v1/pages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            print(f"Successfully added news: {title}")
            return True
        else:
            print(f"Failed to add news: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error creating page: {str(e)}")
        return False

def main():
    # 테스트용 뉴스 데이터
    test_news = {
        "title": "테스트 뉴스 제목",
        "url": "https://example.com",
        "summary": "이것은 테스트 뉴스 요약입니다.",
        "category": "Tech"
    }
    
    # 노션 페이지 생성 테스트
    success = create_notion_page(
        test_news["title"],
        test_news["url"],
        test_news["summary"],
        test_news["category"]
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
