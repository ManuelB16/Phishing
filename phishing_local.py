import pandas as pd
import requests
from tqdm import tqdm
from sklearn.metrics import classification_report

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"   # o "llama3"

def classify_email(subject, body):
    prompt = f"""
Eres un analista de ciberseguridad. Clasifica el siguiente correo como PHISHING o LEGÍTIMO.
Solo responde con una palabra: PHISHING o LEGÍTIMO.
Luego da una breve explicación (una sola línea).

Asunto: {subject}
Cuerpo:
{body}
"""
    payload = {"model": MODEL, "prompt": prompt}
    resp = requests.post(OLLAMA_URL, json=payload, stream=True)
    text = ""
    for line in resp.iter_lines():
        if line:
            part = line.decode("utf-8")
            if '"response":"' in part:
                text += part.split('"response":"')[1].split('"')[0]
    label = "PHISHING" if "PHISH" in text.upper() else "LEGÍTIMO"
    return label, text.strip()

def main():
    df = pd.read_csv("data/emails.csv")
    preds, reasons = [], []

    print(f"Clasificando {len(df)} correos con {MODEL} en Ollama...")
    for _, row in tqdm(df.iterrows(), total=len(df)):
        label, reason = classify_email(row["subject"], row["body"])
        preds.append(label)
        reasons.append(reason)

    df["pred"] = preds
    df["reason"] = reasons
    df.to_csv("data/results.csv", index=False)
    print("Clasificación completada. Resultados guardados en data/results.csv")

    if "label" in df.columns:
        print(classification_report(df["label"], preds))

if __name__ == "__main__":
    main()
