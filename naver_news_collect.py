# ! pip3 install newspaper3k
from newspaper import Article
import urllib
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

class Naver_news_collect:
    def __init__(self, search_term, date_from, date_to, store_path):
        ''' 검색어, 검색 기간("20200321", "20200402" 방식), 저장할 경로(파일 이름 포함)'''
        self.search_term = search_term
        self.date_from = date_from
        self.date_to = date_to
        self.store_path = store_path
    def count(self):
        ''' 검색 건수 보여주기 '''
        word = urllib.parse.quote(self.search_term)
        url_base = "https://search.naver.com/search.naver?where=news&query={}&sort=0&photo=0&field=1&nso=so:r,p:from{}to{},a:t&start=1"
        target_url = url_base.format(word, self.date_from, self.date_to)
        req = requests.get(target_url)
        soup =BeautifulSoup(req.text, "html.parser")
        cases = soup.select_one("#main_pack > div.news.mynews.section._prs_nws > div.section_head > div.title_desc.all_my > span")
        n_cases=int(cases.text.split("/")[1][:-1].replace(",","").strip())
        return print("검색 결과, 총 {}건입니다".format(n_cases))
    def collect1(self):
        ''' 본문 제외 기사 수집 '''
        word = urllib.parse.quote(self.search_term)
        url_base = "https://search.naver.com/search.naver?where=news&query={}&sort=0&photo=0&field=1&nso=so:r,p:from{}to{},a:t&start=1"
        target_url = url_base.format(word, self.date_from, self.date_to)
        req = requests.get(target_url)
        soup =BeautifulSoup(req.text, "html.parser")
        cases = soup.select_one("#main_pack > div.news.mynews.section._prs_nws > div.section_head > div.title_desc.all_my > span")
        n_cases=int(cases.text.split("/")[1][:-1].replace(",","").strip())
        ii = [target_url]
        i = 1
        while n_cases > i+9:
            i += 10
            ii.append(target_url[:-1]+"{}".format(i))

        sources = []
        dates = []
        titles = []
        urls = []
        texts = []
        for i in ii:
            try:
                req = requests.get(target_url[:-1]+"{}".format(i))
                soup =BeautifulSoup(req.text, "html.parser")

                a = soup.select("dd.txt_inline")
                a_list = [ai.text for ai in a]
                a1 = [ai.split()[0] for ai in a_list]   # 출처
                a2 = []   # 날짜
                for ai in a_list:
                    try:
                        a2.append(re.findall(r'\d{4}.\d{2}.\d{2}.', ai)[0])
                    except:
                        a2.append(re.findall(r'\d+\w+\s+전', ai)[0])

                bbb = soup.select("dl > dt > a")
                bbb.remove(soup.select("dl > dt > a.link_help")[0])
                b1 = [b.text for b in bbb]       # 제목
                b2 = [b["href"] for b in bbb]    # URL

                sources.append(a1)
                dates.append(a2)
                titles.append(b1)
                urls.append(b2)
            except:
                sources.append("")
                dates.append("")
                titles.append("")
                urls.append("")
        sources = sum(sources, [])
        dates = sum(dates, [])
        titles = sum(titles, [])
        urls = sum(urls, [])
        news_all= pd.DataFrame({"source": sources, "date": dates, "title":titles,  "url": urls})
        news_all.to_csv(self.store_path, encoding="utf_8_sig")
        return news_all

    def collect2(self):
        ''' 본문 포함 기사 수집 '''
        word = urllib.parse.quote(self.search_term)
        url_base = "https://search.naver.com/search.naver?where=news&query={}&sort=0&photo=0&field=1&nso=so:r,p:from{}to{},a:t&start=1"
        target_url = url_base.format(word, self.date_from, self.date_to)
        req = requests.get(target_url)
        soup =BeautifulSoup(req.text, "html.parser")
        cases = soup.select_one("#main_pack > div.news.mynews.section._prs_nws > div.section_head > div.title_desc.all_my > span")
        n_cases=int(cases.text.split("/")[1][:-1].replace(",","").strip())
        ii = [target_url]
        i = 1
        while n_cases > i+9:
            i += 10
            ii.append(target_url[:-1]+"{}".format(i))

        sources = []
        dates = []
        titles = []
        urls = []
        texts = []
        for i in ii:
            try:
                req = requests.get(target_url[:-1]+"{}".format(i))
                soup =BeautifulSoup(req.text, "html.parser")

                a = soup.select("dd.txt_inline")
                a_list = [ai.text for ai in a]
                a1 = [ai.split()[0] for ai in a_list]   # 출처
                a2 = []   # 날짜
                for ai in a_list:
                    try:
                        a2.append(re.findall(r'\d{4}.\d{2}.\d{2}.', ai)[0])
                    except:
                        a2.append(re.findall(r'\d+\w+\s+전', ai)[0])

                bbb = soup.select("dl > dt > a")
                bbb.remove(soup.select("dl > dt > a.link_help")[0])
                b1 = [b.text for b in bbb]       # 제목
                b2 = [b["href"] for b in bbb]    # URL

                b3 = []   # 본문
                for b2i in b2:
                    try:
                        b22 = Article(b2i, language='ko')
                        b22.download()
                        b22.parse()
                        b3.append(b22.text)
                    except:
                        b3.append("다운로드 실패")
                sources.append(a1)
                dates.append(a2)
                titles.append(b1)
                urls.append(b2)
                texts.append(b3)
            except:
                sources.append("")
                dates.append("")
                titles.append("")
                urls.append("")
                texts.append("")
        sources = sum(sources, [])
        dates = sum(dates, [])
        titles = sum(titles, [])
        urls = sum(urls, [])
        texts = sum(texts, [])
        news_all= pd.DataFrame({"source": sources, "date": dates, "title":titles,  "url": urls, "text": texts,})
        news_all.to_csv(self.store_path, encoding="utf_8_sig")
        return news_all
