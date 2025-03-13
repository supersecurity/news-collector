import os
from datetime import datetime
from notion_client import Client

# Notion 클라이언트 설정
notion = Client(auth=os.environ["NOTION_TOKEN"])
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

def add_to_notion(title, content):
    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "제목": {"title": [{"text": {"content": title}}]},
                "내용": {"rich_text": [{"text": {"content": content}}]},
                "날짜": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
            }
        )
        print("Notion에 성공적으로 추가되었습니다.")
        return True
    except Exception as e:
        print(f"Notion 추가 중 에러 발생: {str(e)}")
        return False

def main():
    try:
        # 테스트용 데이터
        test_title = "테스트 실행"
        test_content = f"GitHub Actions 테스트 실행 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Notion 연결 테스트
        print("Notion 연결 테스트 시작...")
        
        # 데이터베이스 접근 테스트
        notion.databases.retrieve(DATABASE_ID)
        print("데이터베이스 연결 성공")
        
        # 데이터 추가 테스트
        if add_to_notion(test_title, test_content):
            print("테스트 완료: 성공")
        else:
            print("테스트 실패")
            raise Exception("데이터 추가 실패")
            
    except Exception as e:
        print(f"실행 중 오류 발생: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
