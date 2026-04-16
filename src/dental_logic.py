import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance


# --------------------------------------------------
# 🔹 MÁSCARA DE LABIOS (SUAVE Y PRECISA)
# --------------------------------------------------
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

    # 🔥 suavizado progresivo (clave realismo)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=6))

    return mask


# --------------------------------------------------
# 🔹 AJUSTE DE COLOR MÁS ESTABLE
# --------------------------------------------------
def ajustar_color(dientes, paciente, mask):
    dientes_np = np.array(dientes.convert("L"), dtype=np.float32)
    paciente_np = np.array(paciente.convert("L"), dtype=np.float32)
    mask_np = np.array(mask, dtype=np.float32) / 255.0

    if mask_np.sum() < 10:
        return dientes

    brillo_dientes = (dientes_np * mask_np).sum() / mask_np.sum()
    brillo_paciente = (paciente_np * mask_np).sum() / mask_np.sum()

    if brillo_dientes < 1:
        return dientes

    factor = np.clip(brillo_paciente / brillo_dientes, 0.7, 1.3)

    enhancer = ImageEnhance.Brightness(dientes)
    dientes = enhancer.enhance(factor)

    return dientes


# --------------------------------------------------
# 🔥 WARP DENTAL (CURVATURA DE SONRISA)
# --------------------------------------------------
def warp_dental_imagen(pil_img, datos):
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)

    h, w = img.shape[:2]

    # puntos origen (rectángulo)
    src = np.float32([
        [0, 0],
        [w, 0],
        [0, h]
    ])

    p_izq = np.array(datos["plano_oclusal"][0])
    p_der = np.array(datos["plano_oclusal"][1])
    centro = np.array(datos["centro_boca"])

    # 🔥 control de curvatura
    ancho = np.linalg.norm(p_der - p_izq)
    curvatura = 0.12 * ancho

    dst = np.float32([
        p_izq,
        p_der,
        centro + [0, curvatura]
    ])

    M = cv2.getAffineTransform(src, dst)

    warped = cv2.warpAffine(
        img,
        M,
        (int(centro[0] * 2), int(centro[1] * 2)),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_TRANSPARENT
    )

    return Image.fromarray(cv2.cvtColor(warped, cv2.COLOR_BGRA2RGBA))


# --------------------------------------------------
# 🚀 FUNCIÓN PRINCIPAL FINAL
# --------------------------------------------------
def integrar_protesis_profesional(foto_fondo, ruta_protesis, datos_faciales):

    # --- CARGA ---
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

    # 🔥 WARP (AQUÍ ESTÁ LA MAGIA)
    dientes = warp_dental_imagen(dientes, datos_faciales)

    # --- LIENZO ---
    canvas = Image.new("RGBA", paciente.size, (0, 0, 0, 0))

    # colocar directamente (ya deformado)
    canvas.paste(dientes, (0, 0), dientes)

    # --- MÁSCARA LABIOS ---
    mask = crear_mascara_labios(datos_faciales, np.array(paciente).shape)

    # --- AJUSTE DE COLOR ---
    canvas = ajustar_color(canvas, paciente, mask)

    # --- SUAVIZAR TRANSPARENCIA ---
    alpha = canvas.split()[3]
    alpha = alpha.point(lambda p: p * 0.85)
    canvas.putalpha(alpha)

    # --- FUSIÓN FINAL ---
    paciente.paste(canvas, (0, 0), mask)

    return paciente.convert("RGB")
