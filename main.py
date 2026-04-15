import cv2
import numpy as np
from face_analyzer import FaceAnalyzer
from PIL import Image

def ejecutar_diseno_digital(ruta_foto_paciente, ruta_protesis, salida_resultado):
    # 1. Inicializar el analista facial
    analista = FaceAnalyzer()
    
    print(f"--- Analizando rostro en: {ruta_foto_paciente} ---")
    datos = analista.analizar_paciente(ruta_foto_paciente)
    
    if isinstance(datos, str):
        print(datos)
        return

    print(f"Forma detectada: {datos['forma_rostro']}")
    print(f"Ángulo de inclinación: {datos['angulo_inclinacion']:.2f}°")

    # 2. Abrir imágenes con PIL para manejo de transparencia (Alpha Channel)
    paciente_img = Image.open(ruta_foto_paciente).convert("RGBA")
    protesis_img = Image.open(ruta_protesis).convert("RGBA")

    # 3. Escalar la prótesis al ancho de la boca (con margen estético)
    ancho_boca = datos['ancho_boca']
    factor_escala = (ancho_boca * 0.95) / float(protesis_img.size[0])
    nuevo_ancho = int(protesis_img.size[0] * factor_escala)
    nuevo_alto = int(protesis_img.size[1] * factor_escala)
    
    protesis_res = protesis_img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

    # 4. Rotar la prótesis para que coincida con el plano oclusal
    # Usamos -angulo porque PIL rota en sentido antihorario
    protesis_rot = protesis_res.rotate(-datos['angulo_inclinacion'], expand=True, resample=Image.Resampling.BICUBIC)

    # 5. Calcular posición de pegado (centrado en la boca)
    centro_x = int(datos['centro_boca'][0] - (protesis_rot.size[0] / 2))
    centro_y = int(datos['centro_boca'][1] - (protesis_rot.size[1] / 2))

    # 6. Superposición final
    paciente_img.paste(protesis_rot, (centro_x, centro_y), protesis_rot)

    # Guardar resultado
    resultado_final = paciente_img.convert("RGB")
    resultado_final.save(salida_resultado)
    print(f"✅ ¡Éxito! Diseño guardado en: {salida_resultado}")

# --- BLOQUE DE EJECUCIÓN ---
if __name__ == "__main__":
    # Ajusta estas rutas a tus archivos reales
    FOTO_INPUT = "paciente.jpg" 
    DIENTES_INPUT = "assets/overlays/protesis_estandar.png"
    OUTPUT = "resultado_diseno.jpg"
    
    ejecutar_diseno_digital(FOTO_INPUT, DIENTES_INPUT, OUTPUT)
