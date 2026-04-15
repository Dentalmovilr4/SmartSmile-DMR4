import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance


# 🔥 MÁSCARA DE LABIOS MEJORADA
def crear_mascara_labios(puntos_faciales, shape_imagen):
    mask = Image.new("L", (shape_imagen[1], shape_imagen[0]), 0)
    draw = ImageDraw.Draw(mask)

    indices_labio_interno = [
        13, 312, 311, 310, 415, 308, 324, 318, 402, 317,
        14, 87, 178, 88, 95, 78, 191, 80, 81, 82
    ]

    puntos = [
        tuple(puntos_faciales['coords_crude'][i])
        for i in indices_labio_interno
    ]

    draw.polygon(puntos, fill=255)

    # 🔥 SUAVIZADO (esto elimina efecto recorte)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=5))

    return mask


# 🔥 AJUSTE DE COLOR AUTOMÁTICO
def ajustar_color(dientes, paciente, mask):
    # Convertir a escala de grises
    dientes_gray = np.array(dientes.convert("L"))
    paciente_gray = np.array(paciente.convert("L"))

    # Aplicar máscara para analizar solo la boca
    mask_np = np.array(mask) / 255.0

    if mask_np.sum() == 0:
        return dientes

    brillo_dientes = (dientes_gray * mask_np).sum() / mask_np.sum()
    brillo_paciente = (paciente_gray * mask_np).sum() / mask_np.sum()

    if brillo_dientes == 0:
        return dientes

    factor = brillo_paciente / brillo_dientes

    enhancer = ImageEnhance.Brightness(dientes)
    dientes = enhancer.enhance(factor * 0.9)  # ligero ajuste estético

    return dientes


# 🚀 FUNCIÓN PRINCIPAL PRO
def integrar_protesis_profesional(foto_fondo, ruta_protesis, datos_faciales):
    paciente = Image.open(foto_fondo).convert("RGBA")
    dientes = Image.open(ruta_protesis).convert("RGBA")

    # --- ESCALADO ---
    ancho_objetivo = int(datos_faciales["ancho_boca"] * 1.05)
    ratio = ancho_objetivo / dientes.size[0]

    dientes = dientes.resize(
        (ancho_objetivo, int(dientes.size[1] * ratio)),
        Image.Resampling.LANCZOS
    )

    # --- ROTACIÓN ---
    dientes = dientes.rotate(
        -datos_faciales["angulo_inclinacion"],
        expand=True,
        resample=Image.Resampling.BICUBIC
    )

    # --- POSICIÓN ---
    pos_x = int(datos_faciales["centro_boca"][0] - dientes.size[0] / 2)
    pos_y = int(datos_faciales["centro_boca"][1] - dientes.size[1] / 2)

    # --- LIENZO ---
    canvas = Image.new("RGBA", paciente.size, (0, 0, 0, 0))
    canvas.paste(dientes, (pos_x, pos_y), dientes)

    # --- MÁSCARA ---
    mask = crear_mascara_labios(datos_faciales, np.array(paciente).shape)

    # 🔥 AJUSTE DE COLOR
    canvas = ajustar_color(canvas, paciente, mask)

    # 🔥 TRANSPARENCIA SUAVE (más natural)
    alpha = canvas.split()[3]
    alpha = alpha.point(lambda p: p * 0.85)
    canvas.putalpha(alpha)

    # --- FUSIÓN FINAL ---
    paciente.paste(canvas, (0, 0), mask)

    return paciente.convert("RGB")
