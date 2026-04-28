import requests # URL 요청 처리 위함 
from dotenv import load_dotenv # .env 파일을 불러오기 위함 
import os # 운영체제 소통용 
import re # 정규표현식 사용을 위함
import html # 특수문자 제거를 위함 
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv() # .env 파일 불러오기 

client_id=os.getenv("NAVER_CLIENT_ID") 
client_secret=os.getenv("NAVER_CLIENT_SECRET")

url = "https://openapi.naver.com/v1/search/news.json"
headers = {"X-Naver-Client-Id" : client_id,"X-Naver-Client-Secret" : client_secret}
params={"query":"삼성전자", "display":20, "start":1, "sort":"date"}

response=requests.get(url,headers=headers,params=params)

data=response.json()

def clean_text(text):
    text = html.unescape(re.sub('<[^>]+>',"",text))
    return text

okt = Okt()

title_nouns=[]
for item in data['items']:
    title = clean_text(item['title'])
    link = item['link']
    get_nouns= " ".join(okt.nouns(title))
    title_nouns.append(get_nouns)

query_nouns = " ".join(okt.nouns(params['query']))
corpus=[query_nouns]+title_nouns

vectorizer = TfidfVectorizer()
tfidf_matrix=vectorizer.fit_transform(corpus)

scores= cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])
scores = scores[0]

threshold=0.1

for item,score in zip(data['items'],scores):
    if score>=threshold:
        title = clean_text(item['title'])
        link = item['link']
        print("제목:",title,"url:",link)




