import os
from PIL import Image
from face_analyzer import FaceAnalyzer


def cargar_imagen(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró la imagen: {ruta}")
    return Image.open(ruta).convert("RGBA")


def procesar_protesis(protesis_img, datos):
    ancho_boca = datos['ancho_boca']

    factor_escala = (ancho_boca * 0.95) / float(protesis_img.size[0])
    nuevo_size = (
        int(protesis_img.size[0] * factor_escala),
        int(protesis_img.size[1] * factor_escala)
    )

    protesis = protesis_img.resize(nuevo_size, Image.Resampling.LANCZOS)

    protesis = protesis.rotate(
        -datos['angulo_inclinacion'],
        expand=True,
        resample=Image.Resampling.BICUBIC
    )

    return protesis


def calcular_posicion(protesis, datos):
    x = int(datos['centro_boca'][0] - protesis.size[0] / 2)
    y = int(datos['centro_boca'][1] - protesis.size[1] / 2)
    return x, y


def ejecutar_diseno_digital(ruta_foto, ruta_protesis, salida):
    analista = FaceAnalyzer()

    print(f"Analizando: {ruta_foto}")
    datos = analista.analizar_paciente(ruta_foto)

    if not isinstance(datos, dict):
        raise ValueError(datos)

    paciente = cargar_imagen(ruta_foto)
    protesis = cargar_imagen(ruta_protesis)

    protesis = procesar_protesis(protesis, datos)
    posicion = calcular_posicion(protesis, datos)

    paciente.paste(protesis, posicion, protesis)

    resultado = paciente.convert("RGB")
    resultado.save(salida)

    print(f"✅ Resultado guardado en: {salida}")


if __name__ == "__main__":
    ejecutar_diseno_digital(
        "paciente.jpg.jpeg",
        "assets/overlays/protesis_estandar.png",
        "resultado_diseno.jpg"
    )