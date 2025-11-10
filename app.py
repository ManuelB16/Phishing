import tkinter as tk
from tkinter import messagebox, ttk
import csv
import ollama

def analizar_correos():
    try:
        with open("data/emails.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            correos = list(reader)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró data/emails.csv")
        return

    resultados = []
    for correo in correos:
        subject = correo["subject"]
        body = correo["body"]

        prompt = f"""
        Analiza el siguiente correo y responde SOLO con 'PHISHING' o 'LEGÍTIMO'.
        Asunto: {subject}
        Cuerpo: {body}
        """

        try:
            response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
            result = response["message"]["content"].strip().upper()

            if "PHISHING" in result:
                label = "PHISHING"
            elif "LEGÍTIMO" in result or "LEGITIMO" in result:
                label = "LEGÍTIMO"
            else:
                label = "DESCONOCIDO"

            resultados.append([subject, body, label])
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error con un correo:\n{e}")
            return

    # Guardar resultados
    with open("data/results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["subject", "body", "label"])
        writer.writerows(resultados)

    # Mostrar resultados en la interfaz
    for row in tree.get_children():
        tree.delete(row)
    for r in resultados:
        tree.insert("", "end", values=r)

    messagebox.showinfo("Completado", "Clasificación terminada. Resultados guardados en data/results.csv")


# --- INTERFAZ ---
ventana = tk.Tk()
ventana.title("Detector de Phishing - LLM")
ventana.geometry("800x500")
ventana.config(bg="#f4f4f4")

tk.Label(ventana, text="Detector de correos desde emails.csv", font=("Arial", 14, "bold"), bg="#f4f4f4").pack(pady=10)

btn = tk.Button(ventana, text="Analizar correos", command=analizar_correos, bg="#4CAF50", fg="white", width=20)
btn.pack(pady=10)

# Tabla de resultados
columns = ("Asunto", "Cuerpo", "Clasificación")
tree = ttk.Treeview(ventana, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=250)
tree.pack(pady=10)

ventana.mainloop()
