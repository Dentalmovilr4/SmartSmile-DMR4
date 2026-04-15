import cv2
import numpy as np
from PIL import Image, ImageDraw

def crear_mascara_labios(puntos_faciales, shape_imagen):
    # Crear una máscara negra del tamaño de la foto
    mask = Image.new("L", (shape_imagen[1], shape_imagen[0]), 0)
    draw = ImageDraw.Draw(mask)
    
    # Índices de Mediapipe para el contorno INTERNO de los labios
    # Estos puntos definen el "hueco" de la boca
    indices_labio_interno = [
        13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 
        14, 87, 178, 88, 95, 78, 191, 80, 81, 82
    ]
    
    puntos_boca = []
    for idx in indices_labio_interno:
        # Usamos los puntos que ya detectó nuestro FaceAnalyzer
        p = puntos_faciales['coords_crude'][idx]
        puntos_boca.append((p[0], p[1]))
    
    # Dibujar el polígono de la boca en blanco sobre la máscara negra
    draw.polygon(puntos_boca, fill=255)
    return mask

def integrar_protesis_profesional(foto_fondo, ruta_protesis, datos_faciales):
    # 1. Cargar imágenes
    paciente = Image.open(foto_fondo).convert("RGBA")
    dientes = Image.open(ruta_protesis).convert("RGBA")
    
    # 2. Escalar y Rotar (como ya hacíamos)
    ancho_objetivo = int(datos_faciales["ancho_boca"] * 1.1) # Un poco más ancho para cubrir bien
    ratio = ancho_objetivo / float(dientes.size[0])
    alto_objetivo = int(float(dientes.size[1]) * ratio)
    dientes = dientes.resize((ancho_objetivo, alto_objetivo), Image.Resampling.LANCZOS)
    dientes = dientes.rotate(-datos_faciales["angulo_inclinacion"], expand=True)

    # 3. Crear lienzo transparente para los dientes
    canvas_dientes = Image.new("RGBA", paciente.size, (0, 0, 0, 0))
    pos_x = int(datos_faciales["centro_boca"][0] - (dientes.size[0] / 2))
    pos_y = int(datos_faciales["centro_boca"][1] - (dientes.size[1] / 2))
    canvas_dientes.paste(dientes, (pos_x, pos_y), dientes)

    # 4. APLICAR MÁSCARA (El secreto del realismo)
    # Solo los dientes que coincidan con la apertura de la boca serán visibles
    mask_boca = crear_mascara_labios(datos_faciales, np.array(paciente).shape)
    
    # Combinar: Paciente + (Dientes recortados por la máscara de la boca)
    paciente.paste(canvas_dientes, (0, 0), mask=mask_boca)
    
    return paciente.convert("RGB")
