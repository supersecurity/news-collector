import os
import sys

# 디버깅 정보 출력
print("=== Debug Information ===")
token = os.environ.get("NOTION_TOKEN", "")

if not token:
    print("Token is completely empty")
    sys.exit(1)

print(f"Token length: {len(token)}")
print(f"First 4 characters: '{token[:4]}'")
print(f"Contains whitespace at start/end: {token != token.strip()}")
print(f"Raw character values: {[ord(c) for c in token[:4]]}")
print("========================")

# 실제 검증
if not token.startswith("rtn_"):
    print(f"::error::Token must start with 'rtn_' (got: '{token[:4]}')")
    sys.exit(1)

print("Token prefix verification passed")
