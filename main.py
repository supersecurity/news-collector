import os
from datetime import datetime
from notion_client import Client

def validate_database_id(database_id):
    # 하이픈 제거
    clean_id = database_id.replace('-', '')
    if len(clean_id) != 32:
        raise ValueError(f"Invalid database ID length: {len(clean_id)}")
    return clean_id

def verify_notion_access(notion_client, database_id):
    try:
        # 데이터베이스 접근 테스트
        notion_client.databases.retrieve(database_id)
        print("데이터베이스 연결 성공")
        return True
    except Exception as e:
        print(f"데이터베이스 연결 실패: {str(e)}")
        print("다음 사항을 확인해주세요:")
        print("1. Integration이 데이터베이스에 연결되어 있는지")
        print("2. 데이터베이스 ID가 올바른지")
        print("3. NOTION_TOKEN이 올바른지")
        return False

def main():
    try:
        # Notion 토큰 확인
        token = os.environ["NOTION_TOKEN"]
        if not token.startswith('rtn_'):
            raise ValueError("Invalid Notion token format")

        # 데이터베이스 ID 정리
        database_id = os.environ["NOTION_DATABASE_ID"]
        clean_database_id = validate_database_id(database_id)
        
        # Notion 클라이언트 설정
        notion = Client(auth=token)
        
        print("Notion 연결 테스트 시작...")
        
        # 데이터베이스 연결 확인
        if not verify_notion_access(notion, clean_database_id):
            raise Exception("데이터베이스 연결 실패")

        # 테스트 데이터 추가
        test_title = "테스트 실행"
        test_content = f"GitHub Actions 테스트 실행 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        notion.pages.create(
            parent={"database_id": clean_database_id},
            properties={
                "제목": {"title": [{"text": {"content": test_title}}]},
                "내용": {"rich_text": [{"text": {"content": test_content}}]},
                "날짜": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
            }
        )
        print("테스트 데이터 추가 성공")
        
    except Exception as e:
        print(f"실행 중 오류 발생: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
