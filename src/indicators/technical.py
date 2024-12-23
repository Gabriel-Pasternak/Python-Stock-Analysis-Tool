from ta.trend import SMAIndicator, MACD, IchimokuIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator, AccDistIndexIndicator

def calculate_technical_indicators(df):
    # Trend Indicators
    df['SMA20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
    df['SMA50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
    df['SMA200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()
    
    macd = MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    
    ichimoku = IchimokuIndicator(high=df['High'], low=df['Low'])
    df['Ichimoku_Conversion'] = ichimoku.ichimoku_conversion_line()
    df['Ichimoku_Base'] = ichimoku.ichimoku_base_line()
    
    # Momentum Indicators
    df['RSI'] = RSIIndicator(close=df['Close']).rsi()
    stoch = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'])
    df['Stoch_K'] = stoch.stoch()
    df['Stoch_D'] = stoch.stoch_signal()
    
    # Volatility Indicators
    bb = BollingerBands(close=df['Close'])
    df['BB_upper'] = bb.bollinger_hband()
    df['BB_lower'] = bb.bollinger_lband()
    df['ATR'] = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close']).average_true_range()
    
    # Volume Indicators
    df['OBV'] = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
    df['ADI'] = AccDistIndexIndicator(high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume']).acc_dist_index()
    
    return df