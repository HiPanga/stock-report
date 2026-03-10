"""
股票数据采集模块
使用 AKShare 获取 A 股数据
"""
import akshare as ak
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple
import time

def get_stock_quote(stock_code: str) -> Dict:
    """获取单只股票行情"""
    try:
        # 获取个股行情
        if stock_code.startswith('6'):
            full_code = f"sh{stock_code}"
        else:
            full_code = f"sz{stock_code}"
        
        # 使用个股信息接口
        df = ak.stock_individual_info_em(symbol=stock_code)
        if df.empty:
            return None
        
        # 获取实时行情
        spot_df = ak.stock_zh_a_spot_em()
        stock_row = spot_df[spot_df['代码'] == stock_code]
        
        if stock_row.empty:
            return None
        
        row = stock_row.iloc[0]
        
        # 计算涨跌幅
        close = float(row['最新价']) if pd.notna(row['最新价']) else 0
        prev_close = float(row['昨收']) if pd.notna(row['昨收']) else 0
        change_pct = ((close - prev_close) / prev_close * 100) if prev_close else 0
        
        return {
            'code': stock_code,
            'name': row['名称'],
            'price': close,
            'change_pct': change_pct,
            'change_amount': close - prev_close,
            'volume': row['成交量'] if pd.notna(row['成交量']) else 0,
            'amount': row['成交额'] if pd.notna(row['成交额']) else 0,
            'high': row['最高'] if pd.notna(row['最高']) else 0,
            'low': row['最低'] if pd.notna(row['最低']) else 0,
            'open': row['今开'] if pd.notna(row['今开']) else 0,
            'turnover': row['换手率'] if pd.notna(row['换手率']) else 0,
            'pe': row['市盈率-动态'] if pd.notna(row['市盈率-动态']) else None,
            'pb': row['市净率'] if pd.notna(row['市净率']) else None,
            'market_cap': row['总市值'] if pd.notna(row['总市值']) else 0,
        }
    except Exception as e:
        print(f"获取 {stock_code} 数据失败: {e}")
        return None

def get_index_quote(index_code: str) -> Dict:
    """获取大盘指数行情"""
    try:
        # 获取指数行情
        if index_code.startswith('sh'):
            symbol = index_code[2:]
            market = "sh"
        else:
            symbol = index_code[2:]
            market = "sz"
        
        # 使用 AKShare 获取指数实时行情
        df = ak.index_zh_a_hist(symbol=symbol, period="daily", start_date="20990101", end_date="20990101")
        
        # 改用实时行情接口
        spot_df = ak.stock_zh_index_spot()
        idx_row = spot_df[spot_df['代码'] == f"{market}{symbol}"]
        
        if idx_row.empty:
            return None
        
        row = idx_row.iloc[0]
        close = float(row['最新价']) if pd.notna(row['最新价']) else 0
        prev_close = float(row['昨收']) if pd.notna(row['昨收']) else 0
        change_pct = ((close - prev_close) / prev_close * 100) if prev_close else 0
        
        return {
            'code': index_code,
            'name': row['名称'],
            'price': close,
            'change_pct': change_pct,
            'change_amount': close - prev_close,
            'volume': row['成交量'] if pd.notna(row['成交量']) else 0,
            'amount': row['成交额'] if pd.notna(row['成交额']) else 0,
        }
    except Exception as e:
        print(f"获取指数 {index_code} 数据失败: {e}")
        return None

def get_all_stocks_data(stocks: List[Tuple[str, str, str]]) -> List[Dict]:
    """获取所有关注股票的数据"""
    results = []
    
    # 先获取全部实时行情，提高效率
    try:
        spot_df = ak.stock_zh_a_spot_em()
    except Exception as e:
        print(f"获取行情数据失败: {e}")
        spot_df = pd.DataFrame()
    
    for code, name, sector in stocks:
        try:
            if not spot_df.empty:
                stock_row = spot_df[spot_df['代码'] == code]
                if not stock_row.empty:
                    row = stock_row.iloc[0]
                    close = float(row['最新价']) if pd.notna(row['最新价']) else 0
                    prev_close = float(row['昨收']) if pd.notna(row['昨收']) else 0
                    change_pct = ((close - prev_close) / prev_close * 100) if prev_close else 0
                    
                    data = {
                        'code': code,
                        'name': row['名称'],
                        'sector': sector,
                        'price': close,
                        'change_pct': change_pct,
                        'change_amount': close - prev_close,
                        'volume': row['成交量'] if pd.notna(row['成交量']) else 0,
                        'amount': row['成交额'] if pd.notna(row['成交额']) else 0,
                        'high': row['最高'] if pd.notna(row['最高']) else 0,
                        'low': row['最低'] if pd.notna(row['最低']) else 0,
                        'open': row['今开'] if pd.notna(row['今开']) else 0,
                        'turnover': row['换手率'] if pd.notna(row['换手率']) else 0,
                        'pe': row['市盈率-动态'] if pd.notna(row['市盈率-动态']) else None,
                        'pb': row['市净率'] if pd.notna(row['市净率']) else None,
                        'market_cap': row['总市值'] if pd.notna(row['总市值']) else 0,
                    }
                    results.append(data)
                    continue
            
            # 备用：单个获取
            data = get_stock_quote(code)
            if data:
                data['sector'] = sector
                results.append(data)
                
        except Exception as e:
            print(f"处理 {code} 时出错: {e}")
        
        time.sleep(0.1)  # 避免请求过快
    
    return results

def get_all_indices(indices: Dict[str, str]) -> List[Dict]:
    """获取所有大盘指数数据"""
    results = []
    
    try:
        spot_df = ak.stock_zh_index_spot()
    except Exception as e:
        print(f"获取指数数据失败: {e}")
        spot_df = pd.DataFrame()
    
    for code, name in indices.items():
        try:
            if code.startswith('sh'):
                full_code = code
            else:
                full_code = code
            
            if not spot_df.empty:
                idx_row = spot_df[spot_df['代码'] == full_code]
                if not idx_row.empty:
                    row = idx_row.iloc[0]
                    close = float(row['最新价']) if pd.notna(row['最新价']) else 0
                    prev_close = float(row['昨收']) if pd.notna(row['昨收']) else 0
                    change_pct = ((close - prev_close) / prev_close * 100) if prev_close else 0
                    
                    data = {
                        'code': code,
                        'name': name,
                        'price': close,
                        'change_pct': change_pct,
                        'change_amount': close - prev_close,
                        'volume': row['成交量'] if pd.notna(row['成交量']) else 0,
                    }
                    results.append(data)
                    continue
            
            data = get_index_quote(code)
            if data:
                results.append(data)
                
        except Exception as e:
            print(f"获取指数 {code} 失败: {e}")
    
    return results

def format_number(num: float, unit: str = "") -> str:
    """格式化数字显示"""
    if num is None or num == 0:
        return "-"
    
    if unit == "亿":
        return f"{num / 100000000:.2f}亿"
    elif unit == "万":
        return f"{num / 10000:.0f}万"
    elif abs(num) >= 100000000:
        return f"{num / 100000000:.2f}亿"
    elif abs(num) >= 10000:
        return f"{num / 10000:.2f}万"
    else:
        return f"{num:.2f}"
