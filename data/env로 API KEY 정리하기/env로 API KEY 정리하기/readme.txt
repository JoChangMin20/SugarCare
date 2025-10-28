
==========================================================================
1.env 파일은 맨 앞의 1을 지우고 fastapi-scraper 폴더에 넣으면 됩니다.

map.py 파일에서 
from dotenv import load_dotenv를 import 쪽에 추가하고
KAKAO_API_KEY = os.getenv('KAKAO_API_KEY') 
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET') 로 교체하면 됩니다.

market.py와 파일에서
from dotenv import load_dotenv를 import 쪽에 추가하고
CLIENT_ID = os.getenv('NAVER_CLIENT_ID') 
CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET') 로 교체하면 됩니다.

==========================================================================
2.env 파일은 맨 앞의 2를 지우고 frontend 폴더에 넣으면 됩니다.

==========================================================================
.gitignore 파일은 .git 폴더가 있는 곳에 넣으면 됩니다. (git 폴더 안이 아닙니다.)