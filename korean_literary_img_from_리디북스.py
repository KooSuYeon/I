from bs4 import BeautifulSoup
from io import BytesIO
import urllib.request
import requests
import pandas as pd
from PIL import Image

name_list = []
author_list = []
book_content_list = []
img_list = []

book_url = "https://ridibooks.com"

for i in range(1,5):
    r = requests.get(f"https://ridibooks.com/category/bestsellers/101?page={i}&period=steady")
    soup = BeautifulSoup(r.text, 'html.parser')
    for j in range(1, 12):
        name = soup.select_one(f"#__next > main > div > section > ul.fig-1rl9mz1 > li:nth-child({j}) > div > div.fig-1s05j40 > div > div:nth-child(1) > a")
        author = soup.select_one(f"#__next > main > div > section > ul.fig-1rl9mz1 > li:nth-child({j}) > div > div.fig-1s05j40 > div > div.fig-18cjgl > div > p.fig-b6nxu7 > a").text
        name_link = name.get('href')
        name_url = book_url + name_link
        book_r = requests.get(name_url)

        # 이미지 찾기
        html_source = book_r.text
        soup_img = BeautifulSoup(html_source, 'html.parser')
        div_ = soup_img.find("img", class_="thumbnail")
        img_url = div_.get("src")

        # 이미지 png 타입 변환 후 저장
        img_url = "https:" + img_url
        img_response = BytesIO(requests.get(img_url + 'png').content)
        img_pil = Image.open(img_response)
        img_pil.save(f"{name.text}.png")