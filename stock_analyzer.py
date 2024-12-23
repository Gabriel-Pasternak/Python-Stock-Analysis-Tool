import yfinance as yf
import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.weekly_data = self.stock.history(period="1y", interval="1wk")
        self.monthly_data = self.stock.history(period="2y", interval="1mo")
        
    def calculate_indicators(self, df):
        # Calculate technical indicators
        df['SMA20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
        df['SMA50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
        
        # MACD
        macd = MACD(close=df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        
        # RSI
        df['RSI'] = RSIIndicator(close=df['Close']).rsi()
        
        # Bollinger Bands
        bb = BollingerBands(close=df['Close'])
        df['BB_upper'] = bb.bollinger_hband()
        df['BB_lower'] = bb.bollinger_lband()
        
        return df
    
    def analyze_trend(self, df):
        current_price = df['Close'].iloc[-1]
        sma20 = df['SMA20'].iloc[-1]
        sma50 = df['SMA50'].iloc[-1]
        rsi = df['RSI'].iloc[-1]
        macd = df['MACD'].iloc[-1]
        macd_signal = df['MACD_Signal'].iloc[-1]
        
        signals = []
        
        # Trend analysis
        if current_price > sma20 and current_price > sma50:
            signals.append(("Bullish", "Price above both SMAs"))
        elif current_price < sma20 and current_price < sma50:
            signals.append(("Bearish", "Price below both SMAs"))
        
        # RSI analysis
        if rsi > 70:
            signals.append(("Bearish", "RSI indicates overbought"))
        elif rsi < 30:
            signals.append(("Bullish", "RSI indicates oversold"))
            
        # MACD analysis
        if macd > macd_signal:
            signals.append(("Bullish", "MACD above signal line"))
        else:
            signals.append(("Bearish", "MACD below signal line"))
            
        return signals
    
    def calculate_options_probability(self, df):
        # Calculate historical volatility
        returns = np.log(df['Close'] / df['Close'].shift(1))
        volatility = returns.std() * np.sqrt(252)  # Annualized volatility
        
        current_price = df['Close'].iloc[-1]
        trend = sum(1 if signal[0] == "Bullish" else -1 for signal in self.analyze_trend(df))
        
        # Simple probability calculation based on trend and volatility
        call_prob = 0.5 + (0.1 * trend) + (0.1 if volatility < 0.3 else -0.1)
        put_prob = 1 - call_prob
        
        return {
            "call_probability": round(max(min(call_prob, 0.9), 0.1), 2),
            "put_probability": round(max(min(put_prob, 0.9), 0.1), 2),
            "volatility": round(volatility, 2)
        }
    
    def get_recommendation(self):
        # Analyze weekly data
        weekly_df = self.calculate_indicators(self.weekly_data)
        weekly_signals = self.analyze_trend(weekly_df)
        weekly_options = self.calculate_options_probability(weekly_df)
        
        # Analyze monthly data
        monthly_df = self.calculate_indicators(self.monthly_data)
        monthly_signals = self.analyze_trend(monthly_df)
        monthly_options = self.calculate_options_probability(monthly_df)
        
        # Determine overall recommendation
        weekly_sentiment = sum(1 if signal[0] == "Bullish" else -1 for signal in weekly_signals)
        monthly_sentiment = sum(1 if signal[0] == "Bullish" else -1 for signal in monthly_signals)
        
        if weekly_sentiment > 1 and monthly_sentiment > 0:
            recommendation = "BUY"
        elif weekly_sentiment < -1 and monthly_sentiment < 0:
            recommendation = "SELL"
        else:
            recommendation = "HOLD"
            
        return {
            "ticker": self.ticker,
            "recommendation": recommendation,
            "weekly_analysis": {
                "signals": weekly_signals,
                "options": weekly_options
            },
            "monthly_analysis": {
                "signals": monthly_signals,
                "options": monthly_options
            }
        }

def main():
    ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
    
    try:
        analyzer = StockAnalyzer(ticker)
        result = analyzer.get_recommendation()
        
        print(f"\nAnalysis for {result['ticker']}:")
        print(f"Overall Recommendation: {result['recommendation']}\n")
        
        print("Weekly Analysis:")
        print("Signals:")
        for signal, reason in result['weekly_analysis']['signals']:
            print(f"- {signal}: {reason}")
        print(f"Options Probability:")
        print(f"- Call: {result['weekly_analysis']['options']['call_probability']:.0%}")
        print(f"- Put: {result['weekly_analysis']['options']['put_probability']:.0%}")
        print(f"- Volatility: {result['weekly_analysis']['options']['volatility']:.1%}\n")
        
        print("Monthly Analysis:")
        print("Signals:")
        for signal, reason in result['monthly_analysis']['signals']:
            print(f"- {signal}: {reason}")
        print(f"Options Probability:")
        print(f"- Call: {result['monthly_analysis']['options']['call_probability']:.0%}")
        print(f"- Put: {result['monthly_analysis']['options']['put_probability']:.0%}")
        print(f"- Volatility: {result['monthly_analysis']['options']['volatility']:.1%}")
        
    except Exception as e:
        print(f"Error analyzing {ticker}: {str(e)}")

if __name__ == "__main__":
    main()