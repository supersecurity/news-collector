import os
import requests
import feedparser
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import html
import time

GOOGLE_NEWS_URL = "https://news.google.com/rss/search?q=security+OR+보안+OR+취약점&hl=ko&gl=KR&ceid=KR:ko"

def fetch_news():
    feed = feedparser.parse(GOOGLE_NEWS_URL)
    news_items = []
    
    for entry in feed.entries[:10]:
        try:
            title = html.unescape(entry.title)
            summary = entry.description
            soup = BeautifulSoup(summary, 'html.parser')
            summary = html.unescape(soup.get_text())
            
            if len(summary) > 2000:
                summary = summary[:1997] + "..."
            
            news_items.append({
                "title": title,
                "url": entry.link,
                "summary": summary
            })
            
        except Exception as e:
            print(f"Error processing news item: {str(e)}")
            continue
            
    return news_items

def create_notion_page(title, url, summary):
    token = os.environ.get("NOTION_TOKEN")
    database_id = "1b5c077d6a0c802d8595d152ff4bb6d0"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Notion 데이터베이스의 실제 속성 이름에 맞게 수정
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "제목": {  # "Name" 대신 "제목" 사용
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "링크": {  # "URL" 대신 "링크" 사용
                "url": url
            },
            "요약": {  # "Summary" 대신 "요약" 사용
                "rich_text": [
                    {
                        "text": {
                            "content": summary
                        }
                    }
                ]
            }
        }
    }

    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
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
    print("Starting news collection...")
    
    try:
        news_items = fetch_news()
        print(f"Fetched {len(news_items)} news items")
        
        for item in news_items:
            success = create_notion_page(
                item["title"],
                item["url"],
                item["summary"]
            )
            
            if not success:
                print(f"Failed to add news: {item['title']}")
            
            time.sleep(1)
            
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
