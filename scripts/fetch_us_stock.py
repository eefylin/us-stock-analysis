#!/usr/bin/env python3
"""
fetch_us_stock.py
美股財務數據抓取與分析腳本 (支援 yfinance)
用法：python3 fetch_us_stock.py <美股代碼> (例如: NVDA, AAPL, TSLA, MSFT)
"""

import sys
import json
import time
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance module not found. Installing yfinance...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance as yf

def safe_val(df, row_names, col):
    if df is None or df.empty:
        return None
    for name in row_names:
        if name in df.index:
            val = df.loc[name, col]
            if pd.notna(val):
                try:
                    return float(val)
                except Exception:
                    pass
    return None

def fetch_us_stock_data(symbol):
    symbol = symbol.upper().strip()
    print(f"正在抓取美股 {symbol} 財務數據...")
    ticker = yf.Ticker(symbol)
    
    info = ticker.info or {}
    company_name = info.get('longName') or info.get('shortName') or symbol
    sector = info.get('sector') or '美股上市公司'
    currency = info.get('currency') or 'USD'
    
    inc = ticker.financials
    bs = ticker.balance_sheet
    cf = ticker.cashflow
    
    if inc is None or inc.empty:
        raise ValueError(f"無法取得 {symbol} 的損益表數據，請確認代碼是否正確。")
        
    cols = [c for c in inc.columns][:3]
    years = [str(c.year) if hasattr(c, 'year') else str(c)[:4] for c in cols]
    
    data_by_year = {}
    
    for i, col in enumerate(cols):
        yr = years[i]
        
        # 損益表項 (以美元原值)
        rev = safe_val(inc, ['Total Revenue', 'Operating Revenue'], col)
        cogs = safe_val(inc, ['Cost Of Revenue', 'Reconciled Cost Of Revenue'], col)
        gp = safe_val(inc, ['Gross Profit'], col)
        rd = safe_val(inc, ['Research And Development'], col)
        sga = safe_val(inc, ['Selling General And Administration', 'Selling General Administrative'], col)
        opex = safe_val(inc, ['Operating Expense', 'Total Operating Expenses'], col)
        op_inc = safe_val(inc, ['Operating Income', 'Total Operating Income As Reported', 'EBIT'], col)
        ni = safe_val(inc, ['Net Income Common Stockholders', 'Net Income', 'Net Income Continuous Operations'], col)
        eps = safe_val(inc, ['Diluted EPS', 'Basic EPS'], col)
        
        # 資產負債表項
        cash = safe_val(bs, ['Cash Cash Equivalents And Short Term Investments', 'Cash And Cash Equivalents'], col)
        ar = safe_val(bs, ['Receivables', 'Accounts Receivable'], col)
        inv = safe_val(bs, ['Inventory'], col)
        ca = safe_val(bs, ['Current Assets', 'Total Current Assets'], col)
        nca = safe_val(bs, ['Total Non Current Assets'], col)
        ppe = safe_val(bs, ['Net PPE', 'Properties', 'Gross PPE'], col)
        ta = safe_val(bs, ['Total Assets'], col)
        
        cl = safe_val(bs, ['Current Liabilities', 'Total Current Liabilities'], col)
        ncl = safe_val(bs, ['Total Non Current Liabilities Net Minority Interest', 'Total Non Current Liabilities'], col)
        tl = safe_val(bs, ['Total Liabilities Net Minority Interest', 'Total Debt', 'Total Liabilities'], col)
        eq = safe_val(bs, ['Stockholders Equity', 'Total Equity Gross Minority Interest', 'Common Stock Equity'], col)
        
        # 現金流量表項
        op_cf = safe_val(cf, ['Operating Cash Flow', 'Cash Flow From Continuing Operating Activities'], col)
        capex = safe_val(cf, ['Capital Expenditure', 'Net PPE Purchase And Sale'], col)
        div = safe_val(cf, ['Common Stock Dividend Paid', 'Cash Dividends Paid'], col)
        repurchase = safe_val(cf, ['Repurchase Of Capital Stock', 'Common Stock Payments'], col)
        
        # 單位換算：金額轉換為十億美元 ($B)
        scale = 1e9
        def b(v): return round(v / scale, 2) if v is not None else None
        def pct(a, b_val): return round((a / b_val) * 100, 2) if (a is not None and b_val) else None
        
        rev_b = b(rev)
        gp_b = b(gp)
        op_inc_b = b(op_inc)
        ni_b = b(ni)
        rd_b = b(rd)
        sga_b = b(sga)
        opex_b = b(opex)
        cash_b = b(cash)
        ca_b = b(ca)
        ta_b = b(ta)
        cl_b = b(cl)
        tl_b = b(tl)
        eq_b = b(eq)
        op_cf_b = b(op_cf)
        capex_b = b(capex)
        div_b = b(div)
        
        fcf_b = round(op_cf_b + capex_b, 2) if (op_cf_b is not None and capex_b is not None) else None
        
        data_by_year[yr] = {
            'revenue': rev_b,
            'cost_of_revenue': b(cogs),
            'gross_profit': gp_b,
            'gross_margin': pct(gp, rev),
            'rd_expense': rd_b,
            'sga_expense': sga_b,
            'operating_expenses': opex_b,
            'opex_ratio': pct(opex, rev),
            'rd_ratio': pct(rd, rev),
            'operating_income': op_inc_b,
            'operating_margin': pct(op_inc, rev),
            'net_income': ni_b,
            'net_margin': pct(ni, rev),
            'eps': round(eps, 2) if eps is not None else None,
            'roe': pct(ni, eq),
            'roa': pct(ni, ta),
            'cash_and_equivalents': cash_b,
            'current_assets': ca_b,
            'current_liabilities': cl_b,
            'current_ratio': pct(ca, cl),
            'total_assets': ta_b,
            'total_liabilities': tl_b,
            'debt_ratio': pct(tl, ta),
            'stockholders_equity': eq_b,
            'operating_cf': op_cf_b,
            'capex': capex_b,
            'free_cash_flow': fcf_b,
            'dividends_paid': div_b,
        }
        
    result = {
        'symbol': symbol,
        'company_name': company_name,
        'sector': sector,
        'currency': currency,
        'years': years,
        'data_by_year': data_by_year,
        'metadata': {
            'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
            'source': 'Yahoo Finance (yfinance API)',
            'sec_edgar_url': f'https://www.sec.gov/edgar/searchedgar/companysearch',
            'years_covered': years,
            'unit': f'{currency} Billions ($B)'
        }
    }
    
    return result

if __name__ == '__main__':
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'NVDA'
    res = fetch_us_stock_data(symbol)
    print(f"✅ 成功抓取美股 {res['company_name']} ({res['symbol']}) 財報數據：")
    print(json.dumps(res, ensure_ascii=False, indent=2))
    
    out_file = f"{res['symbol']}_raw_data.json"
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"\n原始數據已存至 {out_file}")
