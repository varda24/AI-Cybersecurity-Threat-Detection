from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(X):
    print("\nRunning Anomaly Detection (Isolation Forest)...")

    # Use small sample for speed
    X_sample = X.sample(n=10000, random_state=42)

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X_sample)

    preds = model.predict(X_sample)

    # Convert output
    # -1 = anomaly, 1 = normal
    results = pd.DataFrame({
        "Anomaly": preds
    })

    anomaly_count = (results['Anomaly'] == -1).sum()

    results.to_csv("outputs/anomaly_results.csv", index=False)

    print(f"🚨 Anomalies detected: {anomaly_count}")
    print("✅ Anomaly results saved!")

    return anomaly_count