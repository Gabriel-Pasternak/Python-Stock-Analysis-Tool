import yfinance as yf

class FundamentalAnalyzer:
    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)
        
    def get_fundamentals(self):
        try:
            info = self.stock.info
            financials = self.stock.financials
            
            return {
                'PE_Ratio': info.get('forwardPE', 0),
                'PB_Ratio': info.get('priceToBook', 0),
                'Profit_Margin': info.get('profitMargins', 0),
                'ROE': info.get('returnOnEquity', 0),
                'Current_Ratio': info.get('currentRatio', 0),
                'Debt_To_Equity': info.get('debtToEquity', 0),
                'Revenue_Growth': info.get('revenueGrowth', 0),
                'Analyst_Rating': info.get('recommendationMean', 3),
                'Target_Price': info.get('targetMeanPrice', 0),
                'Dividend_Yield': info.get('dividendYield', 0)
            }
        except:
            return None