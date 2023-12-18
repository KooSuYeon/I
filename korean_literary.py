from bs4 import BeautifulSoup
import requests
import pandas as pd

book_url = "https://ridibooks.com"

name_list = []
author_list = []
book_content_list = []

for i in range(1,5):

    r = requests.get(f"https://ridibooks.com/category/bestsellers/101?page={i}&period=steady")
    soup = BeautifulSoup(r.text, 'html.parser')
    for j in range(1, 12):
        name = soup.select_one(f"#__next > main > div > section > ul.fig-1rl9mz1 > li:nth-child({j}) > div > div.fig-1s05j40 > div > div:nth-child(1) > a")
        author = soup.select_one(f"#__next > main > div > section > ul.fig-1rl9mz1 > li:nth-child({j}) > div > div.fig-1s05j40 > div > div.fig-18cjgl > div > p.fig-b6nxu7 > a").text
        name_link = name.get('href')
        name_url = book_url + name_link
        book_r = requests.get(name_url)
        soup2 = BeautifulSoup(book_r.text, 'html.parser')
        content_lines = soup2.select_one('div#introduce_book.introduce_section.js_introduce_section').text.splitlines()
        filtered_content_lines = [line for line in content_lines if '펼쳐보기' not in line]
        content = "\n".join(filtered_content_lines[:17])
        
        book_name = name.text
        name_list.append(book_name)
        author_list.append(author)
        book_content_list.append(content)

raw_data = {'book_name' : name_list, 'author' : author_list, 'content' : book_content_list}
raw_data = pd.DataFrame(raw_data)
raw_data.to_excel(excel_writer='korean_literary.xlsx')