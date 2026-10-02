import re

import requests
from bs4 import BeautifulSoup

# *Адрес/Ссылка (обязат)
# *GET/POST/перейти по ссылке/загрузить файлы
# * для GET - куки, параметры
# * для POST - заголовки, данные формы
# * для файлов - содержимое
# * для перехода по ссылке - ничего, куки, параметры
# ссылка  <a href='/FJehlwlPSN'>  по адресу <code>/yv7cW4Tl6pBz</code

class Query:
    def __init__(self, type, address):
        self.type = type #+
        self.address = address #+
        self.cookie = None #+
        self.headers = None #+
        self.forms = None #+
        self.params = None
        self.file_content = None #+


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

    print(address)


    if "GET" in html:
        type = "get"
    elif "POST" in html:
        type = "post"
    elif "ссылке" in html:
        type = "link"
    elif "файлы" in html:
        type = "files"
    else:
        raise ValueError("передан некорректный или необработанный тип запроса1")

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
        elif "файлы" in prev_text :
            query.file_content = table_data
        elif "заголовки" in prev_text :
            query.headers = table_data
        elif "параметры" in prev_text :
            query.params = table_data
        # else:
        #     raise ValueError("передан некорректный или необработанный тип запроса2")

    return query


url = "http://hw1.alexbers.com/"
token = "67777a5609f9778299777f23da96993f"
cookie_0 = {"user": token}
response = requests.get(url, cookies=cookie_0)
task_1 = response.text
print(task_1)
query = parse_html_1(task_1)
for key, value in vars(query).items():
    print(f"{key} = {value}")


