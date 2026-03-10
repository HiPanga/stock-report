"""
股票日报主程序
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 确保能正确导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import STOCKS, INDEX_CODES
    from data_collector import get_all_stocks_data, get_all_indices
    from generator import SiteGenerator
except ImportError:
    # GitHub Actions 中运行时的备用导入
    from src.config import STOCKS, INDEX_CODES
    from src.data_collector import get_all_stocks_data, get_all_indices
    from src.generator import SiteGenerator

def main():
    print(f"=== A股日报生成器 ===")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建工作目录
    os.makedirs("dist", exist_ok=True)
    os.makedirs("dist/archive", exist_ok=True)
    
    # 获取数据
    print("\n[1/4] 正在获取股票数据...")
    try:
        stocks = get_all_stocks_data(STOCKS)
        print(f"成功获取 {len(stocks)} 只股票数据")
    except Exception as e:
        print(f"获取股票数据失败: {e}")
        stocks = []
    
    print("\n[2/4] 正在获取大盘指数...")
    try:
        indices = get_all_indices(INDEX_CODES)
        print(f"成功获取 {len(indices)} 个指数数据")
    except Exception as e:
        print(f"获取指数失败: {e}")
        indices = []
    
    # 准备生成器
    print("\n[3/4] 正在生成网站...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    generator = SiteGenerator(
        template_dir="templates",
        output_dir="dist"
    )
    
    # 生成日报
    daily_html = generator.generate_daily_report(stocks, indices, today)
    
    # 保存为今天的日期和 index.html
    generator.save_html(f"archive/{today}.html", daily_html)
    generator.save_html("index.html", daily_html)
    
    # 保存数据
    generator.save_data_json(stocks, indices, today)
    
    # 复制静态文件
    generator.copy_static_files("static")
    
    # 更新归档列表
    print("\n[4/4] 正在更新归档...")
    archive_dir = Path("dist/archive")
    archives = []
    if archive_dir.exists():
        archives = [f.stem for f in archive_dir.glob("*.html") if f.stem != today]
    archives.append(today)
    
    # 生成归档页面
    index_html = generator.generate_index_page(archives)
    generator.save_html("archive/index.html", index_html)
    
    # 保存归档列表供下次使用
    with open("dist/archives.json", "w", encoding="utf-8") as f:
        json.dump(sorted(archives, reverse=True), f, ensure_ascii=False)
    
    print("\n=== 生成完成 ===")
    print(f"输出目录: dist/")
    print(f"今日报告: dist/archive/{today}.html")
    print(f"首页: dist/index.html")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
