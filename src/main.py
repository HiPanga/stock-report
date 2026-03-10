import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# 创建目录
os.makedirs("dist/archive", exist_ok=True)

# 简单数据
stocks = [{"code": "000001", "name": "测试", "price": 10, "change_pct": 1.5, "sector": "科技"}]
indices = [{"code": "sh000001", "name": "上证指数", "price": 3000, "change_pct": 0.5}]

# 生成简单HTML
html = f"""<!DOCTYPE html>
<html>
<head><title>A股日报</title></head>
<body>
<h1>A股日报 - 测试</h1>
<p>数据获取功能暂时关闭，网站部署测试成功</p>
<p>上证指数: {indices[0]['price']}</p>
</body>
</html>"""

with open("dist/index.html", "w") as f:
    f.write(html)

print("✓ 网站生成成功")
