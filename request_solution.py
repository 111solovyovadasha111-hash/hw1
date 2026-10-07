import re
import sys

import requests
from bs4 import BeautifulSoup

# *Адрес/Ссылка (обязат)
# *GET/POST/перейти по ссылке/загрузить файлы
# * для GET - ничего, куки, параметры, заголовки, данные формы
# * для POST - заголовки, данные формы, куки, параметры
# * для файлов - содержимое
# * для перехода по ссылке - тот же get
# примеры ссылок  <a href='/FJehlwlPSN'>  <code>/yv7cW4Tl6pBz</code

class Query:
    def __init__(self, type, address):
        self.type = type
        self.address = address
        self.cookie = None
        self.headers = None
        self.forms = None
        self.params = None
        self.file_content = None


def parse_html_1(html):
    soup = BeautifulSoup(html, "html.parser")
    address = None

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/'):
            address = href
            break

    if not address:
        for code_tag in soup.find_all('code'):
            text = code_tag.get_text(strip=True)
            if text.startswith('/'):
                address = text
                break
    if not address:
        print(html)
        sys.exit(1)

    instruction = str(soup.find_all('h1')[-1].next_sibling)
    if "GET" in instruction or "Перейдите" in instruction:
        type = "get"
    elif "POST" in instruction:
        type = "post"
    elif "файлы" in instruction:
        type = "files"
    else:
        print(html)
        sys.exit(1)

    query = Query(type=type, address=address)
    tables = soup.find_all('table')

    for table in tables:
        prev_text = "" # текст перед таблицей

        for sibling in table.previous_siblings:
            if sibling:
                text = sibling.get_text(strip=True) if hasattr(sibling, 'get_text') else str(sibling).strip()
                if text:
                    prev_text = text
                    break

        table_data = {}
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                key = cols[0].get_text(strip=True)
                val = cols[1].get_text(strip=True)
                table_data[key] = val

        if "cookie" in prev_text:
            query.cookie = table_data
        elif "формы" in prev_text :
            query.forms = table_data
        elif query.type == "files":
                query.file_content = table_data
        elif "заголовки" in prev_text :
            query.headers = table_data
        elif "параметры" in prev_text :
            query.params = table_data

    return query

def main():
    with requests.Session() as session:
        session.trust_env = False
        url = "http://hw1.alexbers.com"
        token = "67777a5609f9778299777f23da96993f"
        session.cookies.set("user", token)
        response = session.get(url)
        task_1 = response.text

        while True:
            query = parse_html_1(task_1)
            address = url + query.address
            print(address, response.elapsed.total_seconds())
            method = "GET" if query.type == "get" else "POST"
            if query.type == "files":
                response = session.post(address, files=query.file_content)
            else:
                response = session.request(
                    method, address,
                    headers=query.headers,
                    cookies=query.cookie,
                    params=query.params,
                    data=query.forms,
                )
            task_1 = response.text

if __name__ == "__main__":
    main()