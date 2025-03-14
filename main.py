import os
from datetime import datetime
from notion_client import Client
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_notion_token(token):
    """Notion 토큰 검증"""
    if not token:
        raise ValueError("NOTION_TOKEN environment variable is not set")
    
    if not token.startswith('secret_'):
        raise ValueError(
            "Invalid token format. Token must start with 'secret_'. "
            "Please check your token in the Notion settings."
        )
    return token

def validate_database_id(database_id):
    """데이터베이스 ID 검증"""
    clean_id = database_id.replace('-', '')
    if len(clean_id) != 32:
        raise ValueError(f"Invalid database ID length: {len(clean_id)}")
    return clean_id

def create_notion_client(token):
    """Notion 클라이언트 생성"""
    try:
        return Client(auth=token)
    except Exception as e:
        logger.error(f"Failed to create Notion client: {e}")
        raise

def verify_database_access(client, database_id):
    """데이터베이스 접근 권한 확인"""
    try:
        client.databases.retrieve(database_id)
        return True
    except Exception as e:
        logger.error(f"Database access verification failed: {e}")
        return False

def create_test_entry(client, database_id):
    """테스트 데이터 생성"""
    try:
        response = client.pages.create(
            parent={"database_id": database_id},
            properties={
                "제목": {"title": [{"text": {"content": "Connection Test"}}]},
                "내용": {"rich_text": [{"text": {"content": f"Test run - {datetime.now()}"}}]},
                "날짜": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
            }
        )
        return response
    except Exception as e:
        logger.error(f"Failed to create test entry: {e}")
        raise

def main():
    try:
        # 환경 변수 검증
        token = os.environ.get("NOTION_TOKEN")
        database_id = os.environ.get("NOTION_DATABASE_ID")

        logger.info("Validating credentials...")
        
        # 토큰 및 데이터베이스 ID 검증
        validated_token = validate_notion_token(token)
        clean_database_id = validate_database_id(database_id)

        # Notion 클라이언트 생성
        notion = create_notion_client(validated_token)
        
        logger.info("Verifying database access...")
        if not verify_database_access(notion, clean_database_id):
            raise Exception("Unable to access the specified database")

        # 테스트 데이터 생성
        logger.info("Creating test entry...")
        create_test_entry(notion, clean_database_id)
        
        logger.info("Operation completed successfully")

    except Exception as e:
        logger.error(f"실행 중 오류 발생: {str(e)}")
        raise

if __name__ == "__main__":
    main()
