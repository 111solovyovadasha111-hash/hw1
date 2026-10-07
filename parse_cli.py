import os
import sys
from urllib.parse import urlencode
from request_solution import parse_html_1, Query

real_stdout = sys.stdout
sys.stdout = sys.stderr


base, tmp = sys.argv[1], sys.argv[2]
html = sys.stdin.read()
print(html)
q = parse_html_1(html)

url = base + q.address
if q.params:
    url += "?" + urlencode(q.params) # замена невалидных символов на формат, который можно передать внутри url
out = [url]

if q.type == "files":
    for i, (k, v) in enumerate((q.file_content ).items()):
        path = os.path.join(tmp, f"f{i}") # путь к файлу - временная папка/f_i
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(v)
        out += ["-F", f"{k}=@/{path};filename={k}"]   # -F флаг пост запроса
else:
    out += ["-X", "GET" if q.type == "get" else "POST"]
    for k, v in (q.forms or {}).items():
        out += ["--data-urlencode", f"{k}={v}"]

for k, v in (q.headers or {}).items():
    out += ["-H", f"{k}: {v}"]
for k, v in (q.cookie or {}).items():
    out += ["-b", f"{k}={v}"]

real_stdout.buffer.write("\0".join(out).encode("utf-8"))