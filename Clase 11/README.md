# Machine Learning Project

This project implements a machine learning model using a dataset related to sales analysis. The goal is to build a model that can predict outcomes based on the provided data.

## Project Structure

```
ml-project
├── src
│   ├── main.py            # Entry point of the application
│   ├── model.py           # Machine learning model definition
│   ├── preprocessing.py    # Data preprocessing tasks
│   ├── evaluation.py       # Model evaluation metrics
│   └── visualization.py     # Graphs and visualizations
├── data
│   ├── analisis_ventas_completo.csv  # Complete sales analysis dataset
│   ├── clientes_limpio.csv           # Cleaned customer data
│   ├── productos_limpio.csv          # Cleaned product data
│   └── ventas_limpio.csv             # Cleaned sales data
├── results
│   └── metrics.txt                   # Evaluation metrics
├── requirements.txt                  # Project dependencies
└── README.md                         # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ml-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the project, execute the following command:
```
python src/main.py
```

This will load the data, preprocess it, train the model, generate predictions, and evaluate the results.

## File Descriptions

- **src/main.py**: Orchestrates the workflow of loading data, preprocessing, training the model, generating predictions, and evaluating results.
- **src/model.py**: Contains functions for creating, training, and predicting with the machine learning model.
- **src/preprocessing.py**: Handles data loading, cleaning, and splitting into training and testing sets.
- **src/evaluation.py**: Provides functions to calculate evaluation metrics such as accuracy, precision, recall, and RMSE.
- **src/visualization.py**: Generates visualizations like confusion matrices and ROC curves to represent model performance.
- **data/**: Contains the datasets used for training and evaluation.
- **results/metrics.txt**: Stores the evaluation metrics after model evaluation.
- **requirements.txt**: Lists the necessary Python packages for the project.
- **README.md**: Provides an overview of the project, setup instructions, and file descriptions.