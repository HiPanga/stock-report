import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from config import STOCKS, INDEX_CODES, SITE_TITLE

# 尝试导入数据获取模块
try:
    from data_collector import get_all_stocks_data, get_all_indices
    HAS_DATA_MODULE = True
except ImportError as e:
    print(f"数据模块导入失败: {e}")
    HAS_DATA_MODULE = False

os.makedirs("dist/archive", exist_ok=True)

# 获取数据
if HAS_DATA_MODULE:
    print("正在获取实时数据...")
    try:
        stocks = get_all_stocks_data(STOCKS)
        indices = get_all_indices(INDEX_CODES)
        print(f"✓ 获取 {len(stocks)} 只股票, {len(indices)} 个指数")
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
        stocks = []
        indices = []
else:
    stocks = []
    indices = []

# 生成HTML
if stocks:
    # 有数据，显示详细表格
    stocks_html = "".join([
        f"<tr><td>{s['code']}</td><td>{s['name']}</td><td>{s['price']:.2f}</td><td>{s['change_pct']:+.2f}%</td></tr>"
        for s in stocks[:10]  # 只显示前10只
    ])
    html = f"""<!DOCTYPE html>
<html>
<head><title>{SITE_TITLE}</title><style>
body {{ font-family: sans-serif; padding: 20px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f2f2f2; }}
.up {{ color: red; }}
.down {{ color: green; }}
</style></head>
<body>
<h1>{SITE_TITLE}</h1>
<p>更新时间: 实时</p>
<h2>股票行情 (前10只)</h2>
<table>
<tr><th>代码</th><th>名称</th><th>价格</th><th>涨跌幅</th></tr>
{stocks_html}
</table>
<p>共 {len(stocks)} 只股票</p>
</body>
</html>"""
else:
    # 无数据，显示配置
    stocks_html = "".join([f"<li>{s[0]} - {s[1]} ({s[2]})</li>" for s in STOCKS])
    html = f"""<!DOCTYPE html>
<html>
<head><title>{SITE_TITLE}</title></head>
<body>
<h1>{SITE_TITLE}</h1>
<h2>关注股票 ({len(STOCKS)}只)</h2>
<ul>{stocks_html}</ul>
<p>数据获取功能调试中...</p>
</body>
</html>"""

with open("dist/index.html", "w") as f:
    f.write(html)

print("✓ 网站生成完成")
