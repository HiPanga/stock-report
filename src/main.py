import os
os.makedirs("dist", exist_ok=True)

html = """<!DOCTYPE html>
<html>
<head><title>A股日报</title></head>
<body>
<h1>A股日报 - 测试版</h1>
<p>脚本运行成功，正在逐步添加功能</p>
</body>
</html>"""

with open("dist/index.html", "w") as f:
    f.write(html)

print("✓ 网站已生成到 dist/index.html")
