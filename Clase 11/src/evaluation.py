def calculate_metrics(y_true, y_pred):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, mean_squared_error
    import numpy as np

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'rmse': rmse
    }

def save_metrics(metrics, filepath='results/metrics.txt'):
    with open(filepath, 'w') as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")