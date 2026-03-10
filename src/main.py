#!/usr/bin/env python3
"""
股票日报主程序 - GitHub Actions 兼容版
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 打印调试信息
print(f"Python: {sys.executable}")
print(f"Working dir: {os.getcwd()}")
print(f"Files: {os.listdir('.')}")

# 创建输出目录
os.makedirs("dist", exist_ok=True)
os.makedirs("dist/archive", exist_ok=True)

# 尝试导入
try:
    # 本地运行
    from src.config import STOCKS, INDEX_CODES
    from src.data_collector import get_all_stocks_data, get_all_indices
    from src.generator import SiteGenerator
except ImportError:
    # GitHub Actions
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config import STOCKS, INDEX_CODES
    from data_collector import get_all_stocks_data, get_all_indices
    from generator import SiteGenerator

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n=== A股日报 {today} ===\n")
    
    # 获取股票数据
    print("[1/3] 获取股票数据...")
    try:
        stocks = get_all_stocks_data(STOCKS)
        print(f"✓ 获取 {len(stocks)} 只股票")
    except Exception as e:
        print(f"✗ 股票数据失败: {e}")
        stocks = []
    
    # 获取指数
    print("[2/3] 获取大盘指数...")
    try:
        indices = get_all_indices(INDEX_CODES)
        print(f"✓ 获取 {len(indices)} 个指数")
    except Exception as e:
        print(f"✗ 指数失败: {e}")
        indices = []
    
    # 生成网站
    print("[3/3] 生成网站...")
    try:
        gen = SiteGenerator("templates", "dist")
        html = gen.generate_daily_report(stocks, indices, today)
        gen.save_html("index.html", html)
        gen.save_html(f"archive/{today}.html", html)
        gen.save_data_json(stocks, indices, today)
        print("✓ 网站生成完成")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print(f"\n=== 完成 ===")
    print(f"https://HiPanga.github.io/stock-report")
    return 0

if __name__ == "__main__":
    sys.exit(main())
