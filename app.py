import streamlit as st
from src.face_analyzer import FaceAnalyzer
from src.dental_logic import integrar_protesis_profesional
import os

st.set_page_config(page_title="SmartSmile-DMR4", layout="centered")

st.title("🦷 SmartSmile-DMR4")
st.subheader("Diseño Digital de Sonrisa Prototipo")

# Subir foto del paciente
archivo_paciente = st.file_uploader("Subir foto del paciente", type=["jpg", "png", "jpeg"])

if archivo_paciente:
    # Guardar temporalmente
    with open("temp_paciente.jpg", "wb") as f:
        f.write(archivo_paciente.getbuffer())
    
    st.image("temp_paciente.jpg", caption="Paciente Original", use_column_width=True)
    
    if st.button("Generar Diseño Automático"):
        analista = FaceAnalyzer()
        datos = analista.analizar_paciente("temp_paciente.jpg")
        
        if isinstance(datos, dict):
            # Aquí la app elegiría según la forma del rostro
            # Por ahora usamos la estándar
            protesis_ruta = "assets/overlays/protesis_estandar.png"
            
            resultado = integrar_protesis_profesional("temp_paciente.jpg", protesis_ruta, datos)
            st.image(resultado, caption="Resultado Estético", use_column_width=True)
            
            # Botón para descargar
            resultado.save("resultado.jpg")
            with open("resultado.jpg", "rb") as file:
                st.download_button("Descargar Imagen", file, "diseno_dmr4.jpg", "image/jpeg")
