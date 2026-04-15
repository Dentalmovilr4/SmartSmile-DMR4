import numpy as np
from PIL import Image, ImageEnhance


def ajustar_color(overlay, background, posicion):
    # Tomar zona de referencia del fondo
    x, y = posicion
    region = background.crop((x, y, x + overlay.size[0], y + overlay.size[1]))

    if region.size != overlay.size:
        return overlay

    # Promedio de brillo
    overlay_gray = np.array(overlay.convert("L")).mean()
    bg_gray = np.array(region.convert("L")).mean()

    if overlay_gray == 0:
        return overlay

    factor = bg_gray / overlay_gray

    enhancer = ImageEnhance.Brightness(overlay)
    overlay = enhancer.enhance(factor)

    return overlay


def integrar_protesis(foto_fondo, ruta_protesis, datos_faciales):
    background = Image.open(foto_fondo).convert("RGBA")
    overlay = Image.open(ruta_protesis).convert("RGBA")

    # 🔹 Rotación más estable
    p1, p2 = datos_faciales["plano_oclusal"]
    angulo = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))

    # 🔹 Escalado más natural
    ancho_boca = datos_faciales["ancho_boca"]
    ancho_objetivo = int(ancho_boca * 0.92)

    ratio = ancho_objetivo / overlay.size[0]
    nuevo_size = (
        ancho_objetivo,
        int(overlay.size[1] * ratio)
    )

    overlay = overlay.resize(nuevo_size, Image.Resampling.LANCZOS)
    overlay = overlay.rotate(-angulo, expand=True, resample=Image.Resampling.BICUBIC)

    # 🔹 Posición
    pos_x = int(datos_faciales["centro_boca"][0] - overlay.size[0] / 2)
    pos_y = int(datos_faciales["centro_boca"][1] - overlay.size[1] / 2)

    # 🔥 Ajuste de color (CLAVE)
    overlay = ajustar_color(overlay, background, (pos_x, pos_y))

    # 🔥 Suavizado de bordes (anti “pegado”)
    alpha = overlay.split()[3]
    alpha = alpha.point(lambda p: p * 0.85)
    overlay.putalpha(alpha)

    background.paste(overlay, (pos_x, pos_y), overlay)

    return background.convert("RGB")
