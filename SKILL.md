---
name: us-stock-analysis
description: |
  美股上市公司三維財務分析儀表板。從 Yahoo Finance (yfinance API) 抓取真實美股財報數據（損益表 Income Statement、資產負債表 Balance Sheet、現金流量表 Cash Flow Statement），計算關鍵財務指標，生成互動式三分頁 HTML 儀表板（經營分析 / 獲利分析 / 財務健全度）並匯出為可分享的 HTML 檔案。

  當使用者提到以下情境時，一定要使用這個 skill：
  - 「幫我分析 NVDA / AAPL / TSLA / MSFT / GOOGL...」或美股 Ticker 股票代碼
  - 「美股財報分析」、「美股三維分析」、「幫我看 NVDA 財報」
  - 提到美股股票代碼（如 NVDA, AAPL, TSLA, MSFT, GOOGL, AMZN, META 等）並要求財報/財務分析
---

# 美股三維財務分析 Skill

## 概述

本 skill 從 Yahoo Finance 抓取美股上市公司的真實財報數據，計算三大維度的財務指標，並生成一份美觀的互動式 HTML 儀表板及下載檔案。

**三大分析維度：**
- 📊 **經營分析**：營收成長 (Revenue)、毛利率 (Gross Margin)、研發費用 (R&D)、營業利益 (Operating Income)
- 💰 **獲利分析**：淨利 (Net Income)、每股盈餘 (Diluted EPS)、股東權益報酬率 (ROE)、資產報酬率 (ROA)
- 🏦 **財務健全度**：現金與約當現金 (Cash & Equivalents)、流動比率 (Current Ratio)、負債比率 (Debt Ratio)、自由現金流 (Free Cash Flow)

---

## 步驟一：抓取財報數據

使用 Skill 內建的 Python 腳本抓取數據：

```bash
python3 ~/.gemini/config/skills/us-stock-analysis/scripts/fetch_us_stock.py <TICKER>
```
例如：
```bash
python3 ~/.gemini/config/skills/us-stock-analysis/scripts/fetch_us_stock.py NVDA
```

腳本會自動輸出包含最近三年財報明細的 JSON 檔案（例如 `NVDA_raw_data.json`）。

---

## 步驟二：建立 HTML 儀表板

由 Agent 手寫完整 HTML 檔案，檔名格式為：`{Symbol}_us_stock_analysis.html`（例如 `NVDA_us_stock_analysis.html`）。

### 儀表板架構
- **Header**：公司名稱 + 股票 Ticker + 產業類別 + 單位 ($B 十億美元)
- **Verify Bar**：資料抓取時間戳記 + SEC EDGAR 連結 + Yahoo Finance 來源連結
- **Tab 1：經營分析 (Operations)**
  - 5 張 KPI 卡片 (含有具體數字與背景說明)
  - 1 個 🔍 經營亮點 Insight Box
  - 4 張 Chart.js 圖表 (雙Y軸營收/毛利率、研發與費用結構、費用率、營業利益)
  - 損益表 Data Table (含趨勢評估欄)
- **Tab 2：獲利分析 (Profitability)**
  - 5 張 KPI 卡片 (淨利、EPS、淨利率、ROE、ROA/股利)
  - 1 個 🔍 獲利亮點 Insight Box
  - 4 張 Chart.js 圖表 (淨利/淨利率、EPS 趨勢、三層利潤率、ROE/ROA)
  - 獲利能力 Data Table
- **Tab 3：財務健全度 (Health)**
  - 5 張 KPI 卡片 (現金部位、流動比率、負債比率、營業現金流、自由現金流)
  - 1 個 🔍 財務健全度亮點 Insight Box
  - 4 張 Chart.js 圖表 (流動/負債比率、現金流三表、資產負債結構、現金部位)
  - 左右並排表格：資產負債表摘要 + 現金流量表摘要

---

## 步驟三：輸出與說明

1. 將產出的 HTML 儲存於工作目錄。
2. 告知使用者檔案已完成建立。
3. 摘要 3 點核心財務發現（含具體數字）。
4. 提醒使用者如欲在系統瀏覽器直接開啟，只需跟我說**「幫我打開報告」**。
