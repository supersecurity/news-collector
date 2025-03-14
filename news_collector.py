import os
import requests
import feedparser
import time
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import html

# Google News RSS URL for security news (Korean)
GOOGLE_NEWS_URL = "https://news.google.com/rss/search?q=security+OR+보안+OR+취약점&hl=ko&gl=KR&ceid=KR:ko"

def fetch_news():
    """Fetch security news from Google News"""
    feed = feedparser.parse(GOOGLE_NEWS_URL)
    news_items = []
    
    for entry in feed.entries[:10]:  # Get top 10 news
        try:
            # Clean up the title and remove HTML entities
            title = html.unescape(entry.title)
            
            # Get summary and clean it up
            summary = entry.description
            soup = BeautifulSoup(summary, 'html.parser')
            summary = html.unescape(soup.get_text())
            
            # Limit summary length to 2000 characters (Notion limit)
            if len(summary) > 2000:
                summary = summary[:1997] + "..."
            
            news_items.append({
                "title": title,
                "url": entry.link,
                "summary": summary,
                "category": "Security"  # Default category
            })
            
        except Exception as e:
            print(f"Error processing news item: {str(e)}")
            continue
            
    return news_items

def create_notion_page(title, url, summary, category):
    """Create a new page in Notion database"""
    token = os.environ.get("NOTION_TOKEN")
    database_id = "1b5c077d6a0c802d8595d152ff4bb6d0"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Set current time in KST
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
                    "start": current_time.split()[0]
                }
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
        # Fetch news from Google News
        news_items = fetch_news()
        print(f"Fetched {len(news_items)} news items")
        
        # Add each news item to Notion
        for item in news_items:
            success = create_notion_page(
                item["title"],
                item["url"],
                item["summary"],
                item["category"]
            )
            
            if not success:
                print(f"Failed to add news: {item['title']}")
            
            # Wait a bit between requests to avoid rate limiting
            time.sleep(1)
            
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
