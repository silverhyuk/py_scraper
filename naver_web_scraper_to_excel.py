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

# 웹 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 크롬창을 띄우지 않음
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 기사 데이터를 저장할 리스트
articles = []


# 페이지별로 기사를 수집하는 함수
def collect_articles():
    page_number = 1
    collected_count = 0
    max_articles = 100  # 수집할 최대 기사 수

    while collected_count < max_articles:
        start_index = (page_number - 1) * 10 + 1
        url = f"https://search.naver.com/search.naver?nso=so%3Add&page={page_number}&query={encoded_query}&sm=tab_pge&start={start_index}&where=web"

        # 페이지 열기
        driver.get(url)
        time.sleep(2)

        # 기사 수집
        news_areas = driver.find_elements(By.CLASS_NAME, "total_wrap")
        for news in news_areas:
            if collected_count >= max_articles:
                break

            # 기사 링크
            try:
                link_element = news.find_element(By.CLASS_NAME, "link_tit")
                link = link_element.get_attribute("href")
            except Exception:
                link = None

            # 기사 제공 업체
            try:
                press_element = news.find_element(By.CLASS_NAME, "source_box").find_element(By.CLASS_NAME, "name")
                press = press_element.text
            except Exception:
                press = None

            # 기사 제목
            try:
                title_element = news.find_element(By.CLASS_NAME, "link_tit")
                title = title_element.text
            except Exception:
                title = None

            # 기사 요약에서 날짜 정보 제거
            try:
                summary_element = news.find_element(By.CLASS_NAME, "total_dsc")
                summary = summary_element.text
                # 날짜 정보는 sub_txt 클래스에 포함되어 있으므로 이를 제거
                date_element = news.find_element(By.CLASS_NAME, "sub_txt")
                date = date_element.text
                summary = summary.replace(date, "").strip()  # 요약 내용에서 날짜 제거
            except Exception:
                summary = None
                date = None

            # 이미지 소스 추출
            try:
                img_element = news.find_element(By.CLASS_NAME, "thumb_link").find_element(By.TAG_NAME, "img")
                img_src = img_element.get_attribute("src")
            except Exception:
                img_src = None

            # 기사 정보를 리스트에 추가 (날짜 및 이미지 소스 포함)
            articles.append([press, date, title, summary, link, img_src])
            collected_count += 1

        # 다음 페이지로 이동
        page_number += 1


# 기사 수집 실행
collect_articles()

# DataFrame으로 변환 (날짜 및 이미지 소스 정보를 포함)
df = pd.DataFrame(articles, columns=["기사업체", "날짜", "제목", "내용", "링크", "이미지 소스"])

# Excel 파일로 저장
df.to_excel("news_articles_100.xlsx", index=False, engine='openpyxl')

# 드라이버 종료
driver.quit()

print("기사 수집 완료 및 Excel 파일 저장.")