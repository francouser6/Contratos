import streamlit as st
import fitz
import pandas as pd

st.set_page_config(page_title="Radar Regulatorio FRM", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS14bSWA3akUYXe-VV04Nw2K0QnQCwCV9SG8g&s")
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS14bSWA3akUYXe-VV04Nw2K0QnQCwCV9SG8g&s", width=250)
st.title("Buscador de palabras FRM")

def buscar_palabras_clave_pdf(pdf_file, palabras_clave):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    resultados = {palabra: [] for palabra in palabras_clave}
    contexto = {palabra: [] for palabra in palabras_clave}
    
    for num_pagina in range(len(doc)):
        pagina = doc[num_pagina]
        texto = pagina.get_text("text")
        lineas = texto.split("\n")
        
        for palabra in palabras_clave:
            for linea in lineas:
                if palabra.lower() in linea.lower():
                    resultados[palabra].append(num_pagina + 1)
                    contexto[palabra].append(f'Página {num_pagina + 1}: "{linea.strip()}"')
    
    return resultados, contexto

def buscar_palabras_clave_excel(excel_file, palabras_clave):
    df = pd.read_excel(excel_file, sheet_name=None)
    resultados = {palabra: [] for palabra in palabras_clave}
    contexto = {palabra: [] for palabra in palabras_clave}
    
    for sheet_name, sheet in df.items():
        for index, row in sheet.iterrows():
            for col in sheet.columns:
                cell_value = str(row[col])
                for palabra in palabras_clave:
                    if palabra.lower() in cell_value.lower():
                        resultados[palabra].append(f'Hoja: {sheet_name}, Fila: {index + 1}')
                        contexto[palabra].append(f'Hoja: {sheet_name}, Fila: {index + 1}, Texto: "{cell_value.strip()}"')
    
    return resultados, contexto

archivo = st.file_uploader("Sube un archivo PDF o Excel", type=["pdf", "xls", "xlsx"])
palabra_input = st.text_input("Ingresa una o más palabras clave (separadas por comas)")

if archivo and palabra_input:
    palabras_clave = [p.strip() for p in palabra_input.split(",")]
    
    if archivo.type == "application/pdf":
        resultados, contexto = buscar_palabras_clave_pdf(archivo, palabras_clave)
    else:
        resultados, contexto = buscar_palabras_clave_excel(archivo, palabras_clave)
    
    st.subheader("Resultados de la búsqueda:")
    for palabra, paginas in resultados.items():
        if paginas:
            st.write(f'**{palabra}** se encontró en: {paginas}')
        else:
            st.write(f'**{palabra}** no se encontró en el documento.')
    
    st.subheader("Contexto de las palabras encontradas:")
    for palabra, frases in contexto.items():
        if frases:
            for frase in frases:
                st.write(f'🔹 {frase}')
        else:
            st.write(f'No se encontró contexto para **{palabra}**.')

st.markdown("---")
st.markdown("### Financial Risk Management - Franco Olivares")
