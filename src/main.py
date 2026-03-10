import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.config import STOCKS, INDEX_CODES
from src.data_collector import get_all_stocks_data, get_all_indices
from src.generator import SiteGenerator
from datetime import datetime
import json

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"=== A股日报 {today} ===")
    
    os.makedirs("dist/archive", exist_ok=True)
    
    print("[1/3] 获取股票数据...")
    stocks = get_all_stocks_data(STOCKS)
    print(f"✓ {len(stocks)} 只股票")
    
    print("[2/3] 获取大盘指数...")
    indices = get_all_indices(INDEX_CODES)
    print(f"✓ {len(indices)} 个指数")
    
    print("[3/3] 生成网站...")
    gen = SiteGenerator("templates", "dist")
    html = gen.generate_daily_report(stocks, indices, today)
    gen.save_html("index.html", html)
    gen.save_html(f"archive/{today}.html", html)
    gen.save_data_json(stocks, indices, today)
    print("✓ 完成")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
