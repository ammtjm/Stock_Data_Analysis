import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load data
data = pd.read_csv('nikkei2011.csv')
data = data.dropna()
closing_prices = data['close'].values

# SSM functions and parameters here...

# Kalman Filter function
def kalman_filter_v9(y, Z, T, R, Q, a1, P1):
    n = len(y)
    alpha_predicted = np.zeros((n, 2, 1))
    P_predicted = np.zeros((n, 2, 2))
    alpha_filtered = np.zeros((n, 2, 1))
    P_filtered = np.zeros((n, 2, 2))
    alpha_smoothed = np.zeros((n, 2, 1))
    P_smoothed = np.zeros((n, 2, 2))
    P_pair = np.zeros((n, 2, 2))
    v = np.zeros((n, 1, 1))
    F = np.zeros((n, 1, 1))
    K = np.zeros((n, 2, 1))
    
    for t in range(n):
        if t == 0:
            alpha_predicted[t] = a1.reshape(2, 1)
            P_predicted[t] = P1
        else:
            alpha_predicted[t] = np.dot(T, alpha_filtered[t-1])
            P_predicted[t] = np.dot(T, np.dot(P_filtered[t-1], T.T)) + np.dot(R, np.dot(Q, R.T))
        
        v[t] = y[t] - np.dot(Z, alpha_predicted[t])
        F[t] = np.dot(Z, np.dot(P_predicted[t], Z.T))
        K[t] = np.dot(np.dot(P_predicted[t], Z.T), np.linalg.inv(F[t]))
        alpha_filtered[t] = alpha_predicted[t] + K[t] * v[t]
        P_filtered[t] = P_predicted[t] - np.dot(K[t], np.dot(Z, P_predicted[t]))
    
    alpha_smoothed[-1] = alpha_filtered[-1]
    P_smoothed[-1] = P_filtered[-1]
    for t in range(n-2, -1, -1):
        L = np.dot(P_filtered[t], np.dot(T.T, np.linalg.inv(P_predicted[t+1])))
        alpha_smoothed[t] = alpha_filtered[t] + np.dot(L, (alpha_smoothed[t+1] - np.dot(T, alpha_filtered[t])))
        P_smoothed[t] = P_filtered[t] + np.dot(np.dot(L, (P_smoothed[t+1] - P_predicted[t+1])), L.T)
        P_pair[t] = P_filtered[t] + np.dot(L, P_smoothed[t+1])
    
    return alpha_predicted, P_predicted, alpha_filtered, P_filtered, alpha_smoothed, P_smoothed, P_pair

# Prediction function
def ssm_next_day_prediction_v3(y, Z, T, R, Q, a1, P1):
    alpha_predicted, _, _, _, _, _, _ = kalman_filter_v9(y, Z, T, R, Q, a1, P1)
    y_pred = np.dot(Z, alpha_predicted[-1])
    return y_pred

def ssm_rolling_prediction_v3(y, Z, T, R, Q, a1, P1):
    predictions = []
    for i in range(1, 11):
        y_subset = y[:-i]
        prediction = ssm_next_day_prediction_v3(y_subset, Z, T, R, Q, a1, P1)
        predictions.append(prediction)
    return predictions

def ssm_one_day_prediction_v4(y, Z, T, R, Q, a1, P1):
    y_subset = y[-200:]  # Take the last 200 days
    prediction = ssm_next_day_prediction_v3(y_subset, Z, T, R, Q, a1, P1)
    return prediction

# Initialize parameters for State Space Model
Z = np.array([[1.0, 0.0]])
T = np.array([[1, 1], [0, 1]])
R = np.eye(2)
Q = 1.0
a1 = np.array([closing_prices[0], 0.0])
P1 = np.eye(2)


#上記のコードは、状態空間モデル（SSM）を使用して日次の株価を予測するためのものです。SSMは、カルマンフィルターというアルゴリズムを使用して、時系列データの潜在的な状態を推定します。このモデルは、観測されるデータと潜在的な状態の間の関係を表すための複数のパラメータを使用しています。上記の関数とパラメータは、この予測モデルの基礎となるものです。
# RF rolling prediction logic
def rf_rolling_prediction(closing_prices):
    rf_predictions = []
    rf = RandomForestRegressor(n_estimators=10)
    for i in range(-1000, 0):
        X_train_rf = np.array([closing_prices[j] for j in range(i-1200, i-200)]).reshape(-1, 1)
        y_train_rf = np.array([closing_prices[j] for j in range(i-1199, i-199)])
        X_test_rf = np.array(closing_prices[i-199]).reshape(1, -1)
        
        rf.fit(X_train_rf, y_train_rf)
        prediction = rf.predict(X_test_rf)
        rf_predictions.append(prediction[0])
    return rf_predictions

rf_predictions = rf_rolling_prediction(closing_prices)

# Trading simulation logic
def trading_simulation(prices, predictions):
    capital = 1.0
    position = 0.0
    history = [capital]

    for i in range(len(prices) - 1):
        if predictions[i] > prices[i] and capital > 0:  # Buy
            position += capital / prices[i + 1]
            capital = 0.0
        elif predictions[i] < prices[i] and position > 0:  # Sell
            capital += position * prices[i + 1]
            position = 0.0
        
        # Update history with current value
        current_value = capital + position * prices[i + 1]
        history.append(current_value)
    
    return history

ssm_history = trading_simulation(closing_prices[-1000:], ssm_prediction_sample)
rf_history = trading_simulation(closing_prices[-1000:], rf_predictions)

# RSI strategy
def rsi_strategy_with_history(data):
    cash = 1.0
    position = 0
    entry_price = 0
    in_trade = False
    history = [cash]
    
    for i in range(len(data)):
        if not in_trade and data['rsi'].iloc[i] > 30:
            # Buy
            entry_price = data['close'].iloc[i]
            position = cash / entry_price
            cash = 0
            in_trade = True
        elif in_trade and data['rsi'].iloc[i] > 70:
            # Sell
            cash = position * data['close'].iloc[i]
            position = 0
            in_trade = False
        # Update history with current value
        current_value = cash + position * data['close'].iloc[i]
        history.append(current_value)
    
    return history

rsi_history = rsi_strategy_with_history(data.tail(1000))
