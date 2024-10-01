import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from urllib.parse import quote

# 검색어를 URL 인코딩
search_query = "와이어바알리"
encoded_query = quote(search_query)

# 네이버 뉴스 검색 URL
url = f"https://search.naver.com/search.naver?where=news&query={encoded_query}&sm=tab_opt&sort=1"

# 웹 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 크롬창을 띄우지 않음
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 페이지 열기
driver.get(url)
time.sleep(2)

# 기사 데이터를 저장할 리스트
articles = []

# 기사 수집 로직
news_areas = driver.find_elements(By.CLASS_NAME, "news_area")
for news in news_areas:
    # 기사 제목, 링크
    title_element = news.find_element(By.CLASS_NAME, "news_tit")
    title = title_element.text
    link = title_element.get_attribute("href")

    # 기사 요약
    summary_element = news.find_element(By.CLASS_NAME, "dsc_txt_wrap")
    summary = summary_element.text

    # 기사 제공 업체
    press_element = news.find_element(By.CLASS_NAME, "press")
    press = press_element.text

    # 날짜
    date_element = news.find_element(By.CLASS_NAME, "info_group").find_elements(By.TAG_NAME, "span")[1]
    date = date_element.text

    # 기사 정보를 리스트에 추가
    articles.append([press, date, title, summary, link])

# DataFrame으로 변환
df = pd.DataFrame(articles, columns=["기사업체", "날짜", "제목", "내용", "링크"])

# CSV 파일로 저장
df.to_csv("news_articles.csv", index=False, encoding='utf-8-sig')

# 드라이버 종료
driver.quit()

print("기사 수집 완료 및 CSV 파일 저장.")