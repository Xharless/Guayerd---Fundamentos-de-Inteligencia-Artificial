import pandas as pd
from preprocessing import load_data, preprocess_data, split_data
from model import create_model, train_model, make_predictions
from evaluation import evaluate_model
from visualization import plot_metrics

def main():
    # Load and preprocess the data
    data = load_data('data/ventas_limpio.csv')
    processed_data = preprocess_data(data)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(processed_data)
    
    # Create and train the model
    model = create_model()
    train_model(model, X_train, y_train)
    
    # Generate predictions
    predictions = make_predictions(model, X_test)
    
    # Evaluate the model
    metrics = evaluate_model(y_test, predictions)
    
    # Save metrics to a file
    with open('results/metrics.txt', 'w') as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    
    # Visualize the results
    plot_metrics(metrics)

if __name__ == "__main__":
    main()