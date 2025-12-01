from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

def create_model():
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    return model

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)

def make_predictions(model, X_test):
    predictions = model.predict(X_test)
    return predictions

def evaluate_model(y_test, predictions):
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return mse, r2