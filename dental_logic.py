import cv2
import numpy as np
from PIL import Image

def integrar_protesis(foto_fondo, ruta_protesis, datos_faciales):
    # Cargar imágenes
    background = Image.open(foto_fondo).convert("RGBA")
    overlay = Image.open(ruta_protesis).convert("RGBA")

    # 1. Calcular rotación según el plano oclusal
    p1, p2 = datos_faciales["plano_oclusal"]
    angulo = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))

    # 2. Escalar prótesis según el ancho de la boca (dejando corredor bucal)
    ancho_objetivo = int(datos_faciales["ancho_boca"] * 0.9)
    ratio = ancho_objetivo / float(overlay.size[0])
    alto_objetivo = int(float(overlay.size[1]) * float(ratio))
    
    overlay = overlay.resize((ancho_objetivo, alto_objetivo), Image.Resampling.LANCZOS)
    overlay = overlay.rotate(-angulo, expand=True)

    # 3. Posicionar en el centro de la boca
    pos_x = int(datos_faciales["centro_boca"][0] - (overlay.size[0] / 2))
    pos_y = int(datos_faciales["centro_boca"][1] - (overlay.size[1] / 2))

    # Superponer
    background.paste(overlay, (pos_x, pos_y), overlay)
    
    return background.convert("RGB")
