import streamlit as st
from src.face_analyzer import FaceAnalyzer
from src.dental_logic import integrar_protesis_profesional
from PIL import Image
import tempfile

st.set_page_config(page_title="SmartSmile-DMR4", layout="centered")

st.title("🦷 SmartSmile-DMR4")
st.subheader("Diseño Digital de Sonrisa Prototipo")

archivo = st.file_uploader("Subir foto del paciente", type=["jpg", "png", "jpeg"])

if archivo:
    # Guardado seguro en archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        temp.write(archivo.read())
        ruta_temp = temp.name

    imagen = Image.open(ruta_temp)
    st.image(imagen, caption="Paciente Original", use_column_width=True)

    if st.button("Generar Diseño Automático"):
        with st.spinner("Analizando rostro..."):
            analista = FaceAnalyzer()
            datos = analista.analizar_paciente(ruta_temp)

        if not isinstance(datos, dict):
            st.error("Error en el análisis facial")
        else:
            st.success(f"Forma detectada: {datos['forma_rostro']}")

            # 🔥 Aquí puedes mejorar lógica luego
            protesis_ruta = "assets/overlays/protesis_estandar.png"

            with st.spinner("Generando diseño..."):
                resultado = integrar_protesis_profesional(
                    ruta_temp,
                    protesis_ruta,
                    datos
                )

            st.image(resultado, caption="Resultado Estético", use_column_width=True)

            # Descargar sin guardar en disco fijo
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_out:
                resultado.save(temp_out.name)

                with open(temp_out.name, "rb") as f:
                    st.download_button(
                        "Descargar Imagen",
                        f,
                        file_name="diseno_dmr4.jpg",
                        mime="image/jpeg"
                    )
