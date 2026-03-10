# 部署到 GitHub Pages - HiPanga 专用指南

## 第一步：在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名称填：`stock-report`
3. 选择 **Public**
4. 点击 **Create repository**

---

## 第二步：推送代码（直接复制粘贴）

```bash
cd /root/.openclaw/workspace/stock-report

git init
git add .
git commit -m "Initial commit: stock report project"
git remote add origin https://github.com/HiPanga/stock-report.git
git branch -M main
git push -u origin main
```

---

## 第三步：启用 GitHub Pages

1. 打开 https://github.com/HiPanga/stock-report/settings/pages
2. **Build and deployment** 下面：
   - Source 选择 **GitHub Actions**
3. 保存

---

## 第四步：手动运行测试

1. 打开 https://github.com/HiPanga/stock-report/actions
2. 点击 **Daily Stock Report**
3. 点击 **Run workflow** → **Run workflow**
4. 等待 1-2 分钟

---

## 第五步：访问你的网站

部署成功后访问：

**🔗 https://HiPanga.github.io/stock-report**

---

## 定时运行说明

- 每天 **北京时间 8:00** 自动更新
- 只在 **周一到周五** 运行（A股交易日）
- 周末和节假日自动跳过

---

## 想改时间？

编辑 `.github/workflows/daily-report.yml` 第 6 行：

```yaml
# 北京时间 8:00（默认）
cron: '0 0 * * 1-5'

# 北京时间 9:00
cron: '0 1 * * 1-5'

# 北京时间 15:00（收盘后）
cron: '0 7 * * 1-5'
```
