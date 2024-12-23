import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

class MLPredictor:
    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=100)
        self.gb_model = GradientBoostingClassifier()
        self.scaler = StandardScaler()
        
    def prepare_features(self, df):
        features = ['SMA20', 'SMA50', 'SMA200', 'RSI', 'MACD', 'Stoch_K', 'ATR', 'OBV']
        X = df[features].fillna(0)
        
        # Create target variable (1 if price goes up in next period, 0 otherwise)
        y = (df['Close'].shift(-1) > df['Close']).astype(int)
        
        return X[:-1], y[:-1]  # Remove last row since we don't have next day's price
        
    def train_models(self, df):
        X, y = self.prepare_features(df)
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest
        self.rf_model.fit(X_scaled, y)
        
        # Train Gradient Boosting
        self.gb_model.fit(X_scaled, y)
        
    def predict(self, df):
        X, _ = self.prepare_features(df)
        X_scaled = self.scaler.transform(X)
        
        rf_pred = self.rf_model.predict_proba(X_scaled)[-1]
        gb_pred = self.gb_model.predict_proba(X_scaled)[-1]
        
        # Ensemble prediction
        final_prob = (rf_pred + gb_pred) / 2
        
        return {
            'up_probability': round(final_prob[1], 2),
            'down_probability': round(final_prob[0], 2)
        }