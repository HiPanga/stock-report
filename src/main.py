#!/usr/bin/env python3
"""
股票日报主程序
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 修复导入路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

# 确保目录存在
os.makedirs("dist", exist_ok=True)
os.makedirs("dist

try:
    from config import STOCKS, INDEX_CODES
    from data_collector import get_all_stocks_data, get_all_indices
    from generator import SiteGenerator
except ImportError as e:
    print(f"导入错误: {e}")
    sys.exit(1)

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"=== A股日报 {today} ===\n")
    
    # 获取股票数据
    print("[1/3] 获取股票数据...")
    try:
        stocks = get_all_stocks_data(STOCKS)
        print(f"✓ 获取 {len(stocks)} 只股票")
    except Exception as e:
        print(f"✗ 失败: {e}")
        stocks = []
    
    # 获取指数
    print("[2/3] 获取大盘指数...")
    try:
        indices = get_all_indices(INDEX_CODES)
        print(f"✓ 获取 {len(indices)} 个指数")
    except Exception as e:
        print(f"✗ 失败: {e}")
        indices = []
    
    # 生成网站
    print("[3/3] 生成网站...")
    try:
        gen = SiteGenerator("templates", "dist")
        html = gen.generate_daily_report(stocks, indices, today)
        gen.save_html("index.html", html)
        gen.save_html(f"archive/{today}.html", html)
        gen.save_data_json(stocks, indices, today)
        print("✓ 完成")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print(f"\n=== 网站已生成 ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
