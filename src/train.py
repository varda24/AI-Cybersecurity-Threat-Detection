from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def train_model(X, y):
    print("\nTraining model...")

    # Reduce dataset size for faster training
    X = X.sample(n=20000, random_state=42)
    y = y.loc[X.index]

    # Stratified split (IMPORTANT FIX)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Model
    model = RandomForestClassifier(n_estimators=50, n_jobs=-1)
    model.fit(X_train, y_train)

    # Predictions
    preds = model.predict(X_test)

    print("\n📊 Classification Report:\n")
    print(classification_report(y_test, preds))

    # =========================
    # 🔥 CONFUSION MATRIX
    # =========================
    cm = confusion_matrix(y_test, preds)

    plt.figure()
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig("outputs/confusion_matrix.png")
    print("✅ Confusion matrix saved!")

    # =========================
    # 🔥 FEATURE IMPORTANCE
    # =========================
    feature_importances = pd.Series(model.feature_importances_, index=X.columns)
    top_features = feature_importances.nlargest(10)

    plt.figure()
    top_features.plot(kind='barh')
    plt.title("Top 10 Important Features")

    plt.savefig("outputs/feature_importance.png")
    print("✅ Feature importance saved!")

    # Save model
    joblib.dump(model, "models/model.pkl")

    return model