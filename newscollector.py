# main.py
import os
from datetime import datetime
import requests
from newspaper import Article
import schedule
from notion_client import Client

# Notion 클라이언트 설정
notion = Client(auth=os.environ["NOTION_TOKEN"])
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

def add_to_notion(content):
    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "제목": {"title": [{"text": {"content": "뉴스 수집 결과"}}]},
                "내용": {"rich_text": [{"text": {"content": content}}]},
                "날짜": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
            }
        )
        print("Notion에 성공적으로 추가되었습니다.")
    except Exception as e:
        print(f"Notion 추가 중 에러 발생: {str(e)}")

def news_collector():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = f"작업 시작: {current_time}\n"
    
    # 여기에 기존의 뉴스 수집 코드 유지
    
    # 결과를 Notion에 추가
    add_to_notion(result)

if __name__ == "__main__":
    news_collector()