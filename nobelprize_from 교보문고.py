from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 브라우저 꺼짐 방지 옵션
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

kyobo_url = 'https://www.kyobobook.co.kr/'
driver.get(kyobo_url)

# 노벨 상 작품, 저자 읽기
df = pd.read_csv('nobel.csv', encoding='CP949')
year_list = df["year"].to_list()
book_list = df["book_name"].to_list()
author_list = df["author"].to_list()

content_list = []


# 교보문고 대문에서 책 + 저자이용해 검색
for i in range(len(book_list)):
    element = driver.find_element(By.CSS_SELECTOR, "#searchKeyword")
    element.clear()
    element.send_keys(book_list[i]+author_list[i])
    element.send_keys("\n")

    # page_source = driver.page_source
    try:
        # 대기 시간을 5초로 설정하고, EC.presence_of_element_located로 요소가 나타날 때까지 대기
        wait = WebDriverWait(driver, 5)
        title_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id^="cmdtName_"]')))
        
        # 성공적으로 요소를 찾았을 때 수행할 코드
        print("Title found:", title_element.text)

        # WebElement의 부모를 찾음
        parent_element = title_element.find_element(By.XPATH, '..')

        # 부모에서 href 속성을 가져옴
        title_url = parent_element.get_attribute('href')

        # 얻은 url을 갖고 셀레니움을 한번 더 돌려서 책 설명을 얻는다.
        driver.get(title_url)
        try:
            wait = WebDriverWait(driver, 5)
            content_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollSpyProdInfo > div.product_detail_area.book_intro > div.intro_bottom")))
            print(content_element.text)
            content_list.append(content_element.text)
        except TimeoutException:
            print("TimeoutException: Content not found within 10 seconds. Moving to the next loop.")
            content_list.append('')
            continue
        

    except TimeoutException:
        # TimeoutException이 발생하면 에러 메시지 출력 후 다음 루프로 진행
        print("TimeoutException: Title not found within 10 seconds. Moving to the next loop.")
        content_list.append('')
        continue


raw_data = {'year' : year_list, 'book_name' : book_list, 'author' : author_list, 'content' : content_list}
raw_data = pd.DataFrame(raw_data)
raw_data.to_excel(excel_writer='nobelprize.xlsx')
