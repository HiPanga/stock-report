import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# 先只用配置文件，不获取实时数据
from config import STOCKS, INDEX_CODES, SITE_TITLE

os.makedirs("dist/archive", exist_ok=True)

# 生成简单页面，显示股票列表
stocks_html = "".join([f"<li>{s[0]} - {s[1]} ({s[2]})</li>" for s in STOCKS])

html = f"""<!DOCTYPE html>
<html>
<head><title>{SITE_TITLE}</title></head>
<body>
<h1>{SITE_TITLE}</h1>
<h2>关注股票 ({len(STOCKS)}只)</h2>
<ul>{stocks_html}</ul>
<h2>大盘指数</h2>
<ul>{"".join([f"<li>{v}</li>" for v in INDEX_CODES.values()])}</ul>
</body>
</html>"""

with open("dist/index.html", "w") as f:
    f.write(html)

print(f"✓ 生成成功，包含 {len(STOCKS)} 只股票")
