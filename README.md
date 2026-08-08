# US Stock Analysis Skill (美股三維財務分析 Skill)

美股上市公司三維財務分析儀表板生成工具，適用於 **Google Antigravity** 與 **Claude** 等 AI Agent 系統。

---

## 📌 專案來源與致謝 (Acknowledge & Credits)

本專案改編自 **[chengwesley/taiwan-stock-analysis](https://github.com/chengwesley/taiwan-stock-analysis)**（台股三維財務分析 Skill）。

感謝原作者開發出極佳的三維財務分析架構（經營分析 / 獲利分析 / 財務健全度）與互動式三分頁 HTML 視覺化樣板。

---

## 🔄 主要改變與改良 (Changes & Improvements)

為了將原本適用於台股的工具擴展至全球最大的美股市場，本專案進行了以下重構與改進：

1. **數據源替換 (yfinance API Integration)**：
   - 將原本針對 Goodinfo.tw 的網頁爬蟲，重構為基於 `yfinance` API 的自動化數據提取引擎。
   - 支援任何美股上市公司的英文 Ticker 符號（例如：`NVDA`, `AAPL`, `TSLA`, `MSFT`, `GOOGL`, `AMZN`, `META` 等）。
   - 免去網頁爬蟲與 Cookie 阻擋風險，資料擷取速度提升數倍且 100% 穩定。

2. **國際財報結構與單位換算 (SEC GAAP Standardization)**：
   - 自動將美股財報 (SEC Filings) 的會計科目映射至標準財務指標。
   - 自動將財務數字轉換為十億美元 ($B USD) 單位，並對齊 Diluted EPS、ROE、ROA、自由現金流 (FCF) 等核心美股指標。

3. **專屬暗色系 (Dark-Mode) 視覺儀表板**：
   - 設計了專為美股/科技股風格打造的深色系 HTML 儀表板。
   - 包含 12 張 Chart.js 動態圖表、KPI 卡片、Insight 亮點分析點評與雙欄對照數據表格。

4. **標準化 Agent 技能架構 (Skill Architecture)**：
   - 封裝為標準 `SKILL.md`，符合 Progressive Disclosure (漸進式載入) 機制。

---

## ✨ 功能特點

- 📊 **自動抓取與計算**：自動下載三大財報（損益表、資產負債表、現金流量表）並計算 15+ 關鍵衍生指標。
- 💰 **三大分析維度**：
  - **經營分析**：營收 (Revenue)、毛利率 (Gross Margin)、研發費用 (R&D)、營業利益率 (Operating Margin)。
  - **獲利分析**：稅後淨利 (Net Income)、每股盈餘 (Diluted EPS)、股東權益報酬率 (ROE)、資產報酬率 (ROA)。
  - **財務健全度**：現金部位 (Cash & Equivalents)、流動比率 (Current Ratio)、負債比率 (Debt Ratio)、自由現金流 (Free Cash Flow FCF)。
- 🎨 **互動式 HTML 視覺化**：生成獨立、可分享、可離線開啟的三分頁 HTML 報告。

---

## 🚀 安裝與使用方式 (Installation & Usage)

### 1. 安裝至 Antigravity / Claude
將本 Repository 複製至您的 Agent 技能目錄：

```bash
# 全域安裝 (所有專案通用)
git clone https://github.com/eefylin/us-stock-analysis.git ~/.gemini/config/skills/us-stock-analysis

# 或 專案級安裝
git clone https://github.com/eefylin/us-stock-analysis.git .agents/skills/us-stock-analysis
```

### 2. 對 Agent 發出指令
安裝完成後，直接在對話框輸入：
- `幫我分析美股 NVDA`
- `幫我看 AAPL 財報`
- `分析美股 TSLA 的獲利能力與財務健全度`

Agent 將自動抓取資料並為您產生與開啟 HTML 分析儀表板！
