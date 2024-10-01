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


# 스크롤하면서 100개의 기사를 수집하는 함수
def collect_articles():
    collected_count = 0
    scroll_pause_time = 2  # 스크롤 후 대기 시간
    last_height = driver.execute_script("return document.body.scrollHeight")  # 현재 페이지 높이

    while collected_count < 100:
        # 기사 수집
        news_areas = driver.find_elements(By.CLASS_NAME, "news_area")
        for news in news_areas:
            if collected_count >= 100:
                break
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
            collected_count += 1

        # 스크롤을 아래로 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)  # 스크롤 후 대기

        # 새로운 페이지 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # 더 이상 스크롤 할 수 없으면 종료
            break
        last_height = new_height


# 기사 수집 실행
collect_articles()

# DataFrame으로 변환
df = pd.DataFrame(articles, columns=["기사업체", "날짜", "제목", "내용", "링크"])

# Excel 파일로 저장
df.to_excel("news_articles_100.xlsx", index=False, engine='openpyxl')

# 드라이버 종료
driver.quit()

print("100개의 기사 수집 완료 및 Excel 파일 저장.")