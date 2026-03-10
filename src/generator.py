"""
HTML 网站生成器
使用 Jinja2 模板引擎
"""
import os
import json
from datetime import datetime
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader
from .config import SITE_TITLE, SITE_DESCRIPTION, SECTOR_COLORS, COLOR_UP, COLOR_DOWN

class SiteGenerator:
    def __init__(self, template_dir: str = "templates", output_dir: str = "dist"):
        self.template_dir = template_dir
        self.output_dir = output_dir
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "archive"), exist_ok=True)
        
        # 初始化 Jinja2
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
    def render_template(self, template_name: str, context: Dict) -> str:
        """渲染模板"""
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def save_html(self, filename: str, content: str):
        """保存 HTML 文件"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已生成: {filepath}")
    
    def generate_daily_report(self, 
                             stocks: List[Dict], 
                             indices: List[Dict],
                             report_date: str = None) -> str:
        """生成日报页面"""
        if report_date is None:
            report_date = datetime.now().strftime("%Y-%m-%d")
        
        # 按板块分组
        tech_stocks = [s for s in stocks if s['sector'] == '科技']
        energy_stocks = [s for s in stocks if s['sector'] == '能源']
        
        # 计算统计数据
        all_change = [s['change_pct'] for s in stocks if s.get('change_pct') is not None]
        avg_change = sum(all_change) / len(all_change) if all_change else 0
        up_count = sum(1 for x in all_change if x > 0)
        down_count = sum(1 for x in all_change if x < 0)
        
        # 涨跌幅排序
        top_gainers = sorted(stocks, key=lambda x: x.get('change_pct', 0), reverse=True)[:5]
        top_losers = sorted(stocks, key=lambda x: x.get('change_pct', 0))[:5]
        
        context = {
            'site_title': SITE_TITLE,
            'site_description': SITE_DESCRIPTION,
            'report_date': report_date,
            'indices': indices,
            'tech_stocks': tech_stocks,
            'energy_stocks': energy_stocks,
            'avg_change': avg_change,
            'up_count': up_count,
            'down_count': down_count,
            'top_gainers': top_gainers,
            'top_losers': top_losers,
            'sector_colors': SECTOR_COLORS,
            'color_up': COLOR_UP,
            'color_down': COLOR_DOWN,
            'now': datetime.now(),
        }
        
        return self.render_template("daily_report.html", context)
    
    def generate_index_page(self, archives: List[str]) -> str:
        """生成首页/归档页面"""
        context = {
            'site_title': SITE_TITLE,
            'site_description': SITE_DESCRIPTION,
            'archives': sorted(archives, reverse=True),
            'now': datetime.now(),
        }
        return self.render_template("index.html", context)
    
    def copy_static_files(self, static_dir: str = "static"):
        """复制静态资源"""
        import shutil
        
        if os.path.exists(static_dir):
            dst = os.path.join(self.output_dir, "static")
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(static_dir, dst)
            print(f"已复制静态资源: {static_dir} → {dst}")
    
    def save_data_json(self, stocks: List[Dict], indices: List[Dict], date: str):
        """保存原始数据为 JSON"""
        data = {
            'date': date,
            'stocks': stocks,
            'indices': indices,
            'generated_at': datetime.now().isoformat(),
        }
        filepath = os.path.join(self.output_dir, "archive", f"{date}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已保存数据: {filepath}")
