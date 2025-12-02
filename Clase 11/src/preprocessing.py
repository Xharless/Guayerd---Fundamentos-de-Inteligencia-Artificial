import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    # Example preprocessing steps
    data = data.dropna()  # Remove missing values
    # Add more preprocessing steps as needed
    return data

def split_data(data, target_column, test_size=0.2, random_state=42):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def main():
    # Example usage
    data = load_data('data/ventas_limpio.csv')
    processed_data = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_data(processed_data, target_column='target_column_name')

if __name__ == "__main__":
    main()