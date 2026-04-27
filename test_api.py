import requests # URL 요청 처리 위함 
from dotenv import load_dotenv # .env 파일을 불러오기 위함 
import os # 운영체제 소통용 
import re # 정규표현식 사용을 위함
import html # 특수문자 제거를 위함 

load_dotenv() # .env 파일 불러오기 

client_id=os.getenv("NAVER_CLIENT_ID") 
client_secret=os.getenv("NAVER_CLIENT_SECRET")

url = "https://openapi.naver.com/v1/search/news.json"
headers = {"X-Naver-Client-Id" : client_id,"X-Naver-Client-Secret" : client_secret}
params={"query":"삼성전자", "display":5, "start":1, "sort":"date"}

response=requests.get(url,headers=headers,params=params)

data=response.json()

def clean_text(text):
    text = html.unescape(re.sub('<[^>]+>',"",text))
    return text

for item in data['items']:
    title = clean_text(item['title'])
    link = item['link']
    print("제목:",title,"url:",link)