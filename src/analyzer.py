from indicators.technical import calculate_technical_indicators
from indicators.fundamental import FundamentalAnalyzer
from ml.predictor import MLPredictor
import yfinance as yf
import pandas as pd

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.weekly_data = self.stock.history(period="1y", interval="1wk")
        self.monthly_data = self.stock.history(period="2y", interval="1mo")
        self.ml_predictor = MLPredictor()
        self.fundamental_analyzer = FundamentalAnalyzer(ticker)
        
    def analyze_technicals(self, df):
        df = calculate_technical_indicators(df)
        current_price = df['Close'].iloc[-1]
        
        signals = []
        
        # Trend Analysis
        if current_price > df['SMA200'].iloc[-1]:
            signals.append(("Bullish", "Price above 200 SMA (Long-term uptrend)"))
        if df['MACD'].iloc[-1] > df['MACD_Signal'].iloc[-1]:
            signals.append(("Bullish", "MACD bullish crossover"))
            
        # Momentum Analysis
        rsi = df['RSI'].iloc[-1]
        if rsi > 70:
            signals.append(("Bearish", "RSI overbought"))
        elif rsi < 30:
            signals.append(("Bullish", "RSI oversold"))
            
        # Volatility Analysis
        if current_price > df['BB_upper'].iloc[-1]:
            signals.append(("Bearish", "Price above upper Bollinger Band"))
        elif current_price < df['BB_lower'].iloc[-1]:
            signals.append(("Bullish", "Price below lower Bollinger Band"))
            
        return signals
        
    def get_recommendation(self):
        # Analyze technical indicators
        weekly_df = calculate_technical_indicators(self.weekly_data)
        monthly_df = calculate_technical_indicators(self.monthly_data)
        
        # Train ML models
        self.ml_predictor.train_models(weekly_df)
        
        # Get predictions
        weekly_pred = self.ml_predictor.predict(weekly_df)
        monthly_pred = self.ml_predictor.predict(monthly_df)
        
        # Get technical signals
        weekly_signals = self.analyze_technicals(weekly_df)
        monthly_signals = self.analyze_technicals(monthly_df)
        
        # Get fundamental data
        fundamentals = self.fundamental_analyzer.get_fundamentals()
        
        # Determine recommendation
        weekly_sentiment = sum(1 if signal[0] == "Bullish" else -1 for signal in weekly_signals)
        monthly_sentiment = sum(1 if signal[0] == "Bullish" else -1 for signal in monthly_signals)
        ml_sentiment = 1 if weekly_pred['up_probability'] > 0.6 else (-1 if weekly_pred['down_probability'] > 0.6 else 0)
        
        # Combined analysis
        total_sentiment = weekly_sentiment + monthly_sentiment + ml_sentiment
        if total_sentiment > 2:
            recommendation = "STRONG BUY"
        elif total_sentiment > 0:
            recommendation = "BUY"
        elif total_sentiment < -2:
            recommendation = "STRONG SELL"
        elif total_sentiment < 0:
            recommendation = "SELL"
        else:
            recommendation = "HOLD"
            
        return {
            "ticker": self.ticker,
            "recommendation": recommendation,
            "weekly_analysis": {
                "signals": weekly_signals,
                "ml_prediction": weekly_pred
            },
            "monthly_analysis": {
                "signals": monthly_signals,
                "ml_prediction": monthly_pred
            },
            "fundamentals": fundamentals
        }