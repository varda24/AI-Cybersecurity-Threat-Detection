import pandas as pd

def predict_threats(model, X):
    predictions = model.predict(X)

    results = pd.DataFrame({
        "Prediction": predictions
    })

    results.to_csv("outputs/results.csv", index=False)

    print("Predictions saved to outputs/results.csv")

    # Alert simulation
    threats = results[results['Prediction'] == 1]

    print(f"\n⚠️ Detected {len(threats)} potential threats!")