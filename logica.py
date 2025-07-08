import os
import re
import numpy as np
import easyocr
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import ssl
import urllib.request

#ssl._create_default_https_context = ssl._create_unverified_context




def procesar_pdf(ruta_pdf, ruta_salida="salida"):
    print(f"📄 Procesando PDF: {ruta_pdf}")

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    reader_ocr = easyocr.Reader(
        ['es'],
        gpu=False,
        model_storage_directory='C:\\Users\mpure\Documents\ProyectoSSADE\SSADE_SUNARP\models',
        download_enabled=False
    )

    #reader_ocr = easyocr.Reader(['es'], gpu=False)

    imagenes = convert_from_path(ruta_pdf, dpi=300)
    lector_pdf = PdfReader(ruta_pdf)

    total_titulos = 0
    ultimo_titulo = None
    num_doc = 1
    i = 0
    hojas_por_titulo = {}

    while i < len(imagenes):
        if i % 2 != 0:
            i += 1
            continue

        imagen = imagenes[i]
        ancho, alto = imagen.size
        region = imagen.crop((0, 0, ancho, int(alto * 0.3)))
        region_np = np.array(region)

        resultado = reader_ocr.readtext(region_np)
        texto = " ".join([r[1] for r in resultado]).upper()

        print(f"\n--- Página {i+1} ---")
        print(texto)

        def guardar(tipo):
            nonlocal num_doc
            nombre_archivo = f"{ultimo_titulo}_000{num_doc:02d}.pdf"
            guardar_pdf(nombre_archivo, lector_pdf, i, ruta_salida)
            print(f"✅ Guardado {tipo}: {nombre_archivo}")
            hojas_por_titulo[ultimo_titulo] = hojas_por_titulo.get(ultimo_titulo, 0) + 2
            num_doc += 1

        match = re.search(r'2025[-–]\d{6,7}', texto)
        if match:
            numero_titulo = match.group(0).replace(" ", "").replace("–", "-")
            ultimo_titulo = numero_titulo
            num_doc = 1
            nombre_archivo = f"{ultimo_titulo}_000{num_doc:02d}.pdf"
            guardar_pdf(nombre_archivo, lector_pdf, i, ruta_salida)
            print(f"✅ Guardado: {nombre_archivo}")
            hojas_por_titulo[ultimo_titulo] = 2
            total_titulos += 1
            num_doc += 1
            i += 2
            continue

        if "IDENTIFICACIÓN BIOMÉTRICA" in texto and ultimo_titulo:
            guardar("biométrico")
            i += 2
            continue

        if ("OFICIO" in texto or "EXP. NRO" in texto) and ultimo_titulo:
            guardar("oficio")
            i += 2
            continue

        if "SOLICITO: DESIS" in texto and ultimo_titulo:
            guardar("desistimiento")
            i += 2
            continue





        


        i += 2

    print("✅ Finalizado correctamente.")
    print("✅ Títulos separados correctamente.")
    return total_titulos, hojas_por_titulo

def guardar_pdf(nombre_archivo, lector_pdf, pagina_inicio, salida_dir):
    writer = PdfWriter()
    writer.add_page(lector_pdf.pages[pagina_inicio])
    if pagina_inicio + 1 < len(lector_pdf.pages):
        writer.add_page(lector_pdf.pages[pagina_inicio + 1])
    ruta_salida = os.path.join(salida_dir, nombre_archivo)
    with open(ruta_salida, "wb") as f:
        writer.write(f)
