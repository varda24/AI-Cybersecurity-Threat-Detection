from src.preprocess import load_data, preprocess_data
from src.train import train_model
from src.predict import predict_threats
from src.visualize import plot_distribution
from src.anomaly import detect_anomalies

def main():
    print("Loading dataset...")
    df = load_data("data/kddcup.data_10_percent_corrected")

    print("Preprocessing data...")
    X, y = preprocess_data(df)

    print("Plotting data distribution...")
    plot_distribution(y)

    print("Training model...")
    model = train_model(X, y)

    print("Running predictions...")
    predict_threats(model, X)

    print("Running anomaly detection...")
    detect_anomalies(X)

if __name__ == "__main__":
    main()