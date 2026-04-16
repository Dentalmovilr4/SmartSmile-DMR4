import cv2
import numpy as np
import mediapipe as mp

# 🔹 CORRECCIÓN CRÍTICA: Importación compatible con servidores y versiones nuevas
try:
    import mediapipe.solutions.face_mesh as mp_face_mesh
except (ImportError, AttributeError):
    from mediapipe.python.solutions import face_mesh as mp_face_mesh

class FaceAnalyzer:
    def __init__(self):
        # Mantenemos tu configuración de alta precisión
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True, # Indispensable para estética dental
            min_detection_confidence=0.6
        )

    def _validar_landmarks(self, puntos):
        # Verificamos que los puntos de referencia dental existan
        indices_clave = [61, 291, 168, 152]
        for i in indices_clave:
            if i >= len(puntos):
                raise ValueError("Landmarks incompletos: El rostro está muy lejos o mal iluminado")

    def analizar_paciente(self, image_path):
        # 1. Cargar y validar imagen
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"No se encontró la imagen en: {image_path}")

        h, w, _ = image.shape
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 2. Procesar con IA
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            raise ValueError("Error: No se detectó rostro en la foto")

        puntos = results.multi_face_landmarks[0].landmark
        self._validar_landmarks(puntos)

        # Función para convertir coordenadas a píxeles
        def get_p(i):
            return np.array([puntos[i].x * w, puntos[i].y * h])

        # --- BIOMETRÍA DENTAL ---
        nasion = get_p(168)
        pogonion = get_p(152)
        izq_labio = get_p(61)
        der_labio = get_p(291)

        # 🔹 Estabilización del ángulo oclusal
        delta = der_labio - izq_labio
        angulo = np.degrees(np.arctan2(delta[1], delta[0]))
        angulo = np.clip(angulo, -25, 25) 

        # 🔹 Medidas de estructura facial
        frente_w = np.linalg.norm(get_p(103) - get_p(332))
        pomulo_w = np.linalg.norm(get_p(234) - get_p(454))
        mandibula_w = np.linalg.norm(get_p(58) - get_p(288))
        cara_l = np.linalg.norm(get_p(10) - get_p(152))

        # 🔹 Clasificación Morfológica para Diseño de Sonrisa
        ratio = cara_l / pomulo_w

        if ratio > 1.35:
            forma = "Alargado"
        elif abs(pomulo_w - mandibula_w) / pomulo_w < 0.1:
            forma = "Cuadrado"
        elif frente_w > mandibula_w * 1.2:
            forma = "Triangular"
        else:
            forma = "Ovalado"

        # Coordenadas completas para la máscara de labios en dental_logic.py
        coords_crude = [[p.x * w, p.y * h] for p in puntos]

        return {
            "forma_rostro": forma,
            "linea_media": (nasion.tolist(), pogonion.tolist()),
            "plano_oclusal": (izq_labio.tolist(), der_labio.tolist()),
            "ancho_boca": float(np.linalg.norm(der_labio - izq_labio)),
            "centro_boca": ((izq_labio + der_labio) / 2).tolist(),
            "angulo_inclinacion": float(angulo),
            "coords_crude": coords_crude
        }
