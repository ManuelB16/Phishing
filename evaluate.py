# evaluate.py
import pandas as pd
import sys
import json
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

CSV_PATH = "data/results.csv"

def main():
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo: {CSV_PATH}")
        sys.exit(1)

    # Comprobar columnas
    if "label" not in df.columns or "pred" not in df.columns:
        print("[ERROR] El CSV debe contener al menos las columnas 'label' y 'pred'.")
        print("Columnas encontradas:", list(df.columns))
        sys.exit(1)

    # Normalizar mayúsculas y espacios
    y_true = df["label"].astype(str).str.strip().str.upper()
    y_pred = df["pred"].astype(str).str.strip().str.upper()

    print("=== Clasification report ===")
    print(classification_report(y_true, y_pred, digits=4))

    print("=== Confusion matrix (rows: true / cols: pred) ===")
    cm = confusion_matrix(y_true, y_pred, labels=["PHISHING", "LEGÍTIMO", "LEGIT"] )
    # Si tus labels son diferentes a PHISHING/LEGIT, ajusta las etiquetas anteriores.
    print(cm)

    acc = accuracy_score(y_true, y_pred)
    print(f"\nAccuracy: {acc:.4f}")

    # Guardar métricas simples
    metrics = {
        "accuracy": float(acc),
        "classification_report": classification_report(y_true, y_pred, output_dict=True)
    }
    with open("data/metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print("\nMétricas guardadas en data/metrics.json")

if __name__ == "__main__":
    main()
