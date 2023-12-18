# Crawling

# Description
작품 크롤링

past
- 책 제목, 저자만 존재
- 외국문학 43권, 한국문학 43권만 존재
  - BeautifulSoup 사용



# 12.02 Update

외국문학 책 내용 추가 (content) 
  - 책 제목에서 책 상세 url 파싱 -> 책 소개 파싱 (최대 17줄)
  - BeautifulSoup 사용



노벨문학상 책 추가
  - 노벨문학상은 나무위키에서 크롤링 -> 책 제목과 저자 담긴 csv 파일 생성 (nobel.csv)
    - BeautifulSoup 사용

  - 노벨문학상 책 내용 추가 -> csv 파일 읽어서 책 제목이랑 저자 이용해 검색 크롤링
    - Options() 이용해서 브라우저 꺼짐 방지, 검색 후 5초 대기 시간 둬 요소 찾을 시간 확보
    - 검색 결과 존재하지 않는 도서라면 쓰여지는 것 없게 Exception 처리
    - Selenium 사용


# 12.15 Updata

휴고상 책 추가
  - csv파일 생성 (hugo.csv)
  - 책 내용 존재하는 책들만 교보문고 크롤링 -> Selenium 이용

*foreign_literary.xlsx 내용 변경
*nobelprize.xlsx 생성
*hugoprize.xlsx 생성
