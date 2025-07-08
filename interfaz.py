import tkinter as tk
from tkinter import filedialog, messagebox
from logica import procesar_pdf
import os

def iniciar_interfaz():
    
    ventana = tk.Tk()
    ventana.title("ESCANEADOR")
    ventana.geometry("420x250")

    ruta_pdf = tk.StringVar()
    ruta_salida = tk.StringVar()
    ruta_salida.set("salida")  

    def seleccionar_pdf():
        archivo = filedialog.askopenfilename(title="Selecciona PDF", filetypes=[("PDF", "*.pdf")])
        if archivo:
            ruta_pdf.set(archivo)
            nombre_archivo = os.path.basename(archivo)
            mensaje.config(text=f"📄 PDF: {nombre_archivo}")

    def seleccionar_directorio():
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de guardado")
        if carpeta:
            ruta_salida.set(carpeta)
            mensaje_destino.config(text=f"📁 Guardar en: {carpeta}")

    def separar_pdf():
        if ruta_pdf.get() == "":
            messagebox.showwarning("Sin PDF", "Primero selecciona un PDF.")
            return

        messagebox.showinfo("Procesando", "Iniciando OCR y separación...")

        cantidad, detalles = procesar_pdf(ruta_pdf.get(), ruta_salida.get())

        if cantidad > 0:
            resumen = f"Títulos separados: {cantidad}\n\n"
            for titulo, paginas in detalles.items():
                resumen += f"{titulo} ➜ {paginas // 2} hojas\n"
            messagebox.showinfo("Finalizado", resumen)
        else:
            messagebox.showwarning("Sin resultados", "No se encontró ningún título válido.")

    # UI
    tk.Label(ventana, text="ESCANEADOR", font=("Helvetica", 14, "bold")).pack(pady=10)

    tk.Button(ventana, text="📁 Cargar PDF", command=seleccionar_pdf).pack(pady=5)
    mensaje = tk.Label(ventana, text="Ningún archivo.", fg="gray")
    mensaje.pack(pady=5)

    tk.Button(ventana, text="📂 Seleccionar carpeta de destino", command=seleccionar_directorio).pack(pady=5)
    mensaje_destino = tk.Label(ventana, text="Destino: carpeta 'salida'", fg="gray")
    mensaje_destino.pack(pady=5)

    tk.Button(ventana, text="🪄 SEPARAR", bg="green", fg="white", command=separar_pdf).pack(pady=10)

    ventana.mainloop()
