# 股票日报项目

自动收集 A 股科技股、能源板块行情，每日生成静态网站并通过 GitHub Pages 发布。

## 在线访问

部署后访问：`https://<你的用户名>.github.io/stock-report`

## 功能特性

- 📊 自动采集 A 股科技股、能源板块数据
- 📈 大盘指数实时展示（上证指数、深证成指、创业板指、沪深300）
- 🏆 每日涨幅榜/跌幅榜
- 📅 历史归档，支持回顾过往数据
- 📱 响应式设计，支持手机/平板/电脑
- ⚡ GitHub Actions 自动定时运行

## 技术栈

- **数据采集**: Python + AKShare (东方财富数据)
- **网站生成**: Jinja2 模板引擎
- **样式框架**: Tailwind CSS
- **部署托管**: GitHub Pages
- **自动化**: GitHub Actions

## 快速开始

### 1. Fork 本仓库

点击右上角的 "Fork" 按钮，将项目复制到你的 GitHub 账号下。

### 2. 启用 GitHub Pages

1. 进入仓库的 **Settings** → **Pages**
2. Source 选择 **GitHub Actions**

### 3. 配置定时任务（可选）

编辑 `.github/workflows/daily-report.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 0 * * 1-5'  # 周一到周五 UTC 00:00 (北京时间 8:00)
```

### 4. 手动触发测试

进入仓库的 **Actions** → **Daily Stock Report** → **Run workflow**，手动运行一次测试。

## 本地开发

```bash
# 克隆仓库
git clone https://github.com/<你的用户名>/stock-report.git
cd stock-report

# 安装依赖
pip install -r requirements.txt

# 运行生成脚本
python src/main.py

# 预览生成的网站
python -m http.server 8000 -d dist
# 访问 http://localhost:8000
```

## 自定义配置

编辑 `src/config.py`：

```python
# 添加关注的股票
STOCKS = [
    ("000001", "平安银行", "金融"),
    # ...
]

# 修改网站标题
SITE_TITLE = "我的股票日报"
```

## 目录结构

```
stock-report/
├── .github/workflows/     # GitHub Actions 配置
├── src/                   # 源代码
│   ├── config.py         # 配置信息
│   ├── data_collector.py # 数据采集
│   ├── generator.py      # 网站生成器
│   └── main.py           # 主程序
├── templates/             # HTML 模板
│   ├── daily_report.html # 日报模板
│   └── index.html        # 归档页模板
├── static/               # 静态资源
├── data/                 # 数据存储（自动创建）
├── archive/              # 历史归档（自动创建）
├── dist/                 # 生成的网站（自动创建）
├── requirements.txt      # Python 依赖
└── README.md
```

## 数据来源

本项目使用 [AKShare](https://www.akshare.xyz/) 获取 A 股实时行情数据，数据来源于东方财富网。

**免责声明**: 本报告仅供学习交流使用，不构成任何投资建议。股市有风险，投资需谨慎。

## License

MIT License
