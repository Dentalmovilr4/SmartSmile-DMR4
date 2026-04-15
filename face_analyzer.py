import cv2
import mediapipe as mp
import numpy as np

class FaceAnalyzer:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True
        )

    def obtener_medidas(self, imagen_path):
        image = cv2.imread(imagen_path)
        if image is None: return None
        
        results = self.face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.multi_face_landmarks:
            return None

        coords = results.multi_face_landmarks[0].landmark
        h, w, _ = image.shape

        # Convertir puntos normalizados a píxeles
        p = lambda i: np.array([coords[i].x * w, coords[i].y * h])

        # 1. Parámetros de Simetría
        nasion = p(168)
        pogonion = p(152)
        comisura_izq = p(61)
        comisura_der = p(291)

        # 2. Medidas para Forma de Rostro
        frente_izq, frente_der = p(103), p(332)
        pomulo_izq, pomulo_der = p(234), p(454)
        mandibula_izq, mandibula_der = p(58), p(288)
        top_cabeza, menton = p(10), p(152)

        dist = lambda a, b: np.linalg.norm(a - b)

        frente_w = dist(frente_izq, frente_der)
        pomulo_w = dist(pomulo_izq, pomulo_der)
        mandibula_w = dist(mandibula_izq, mandibula_der)
        cara_l = dist(top_cabeza, menton)

        # Lógica de clasificación de forma
        forma = "Ovalado"
        if cara_l > pomulo_w * 1.3:
            forma = "Alargado"
        elif abs(pomulo_w - mandibula_w) < (pomulo_w * 0.1):
            forma = "Cuadrado"
        elif frente_w > mandibula_w * 1.2:
            forma = "Corazón"

        return {
            "forma_rostro": forma,
            "linea_media": (nasion, pogonion),
            "plano_oclusal": (comisura_izq, comisura_der),
            "ancho_boca": dist(comisura_izq, comisura_der),
            "centro_boca": (comisura_izq + comisura_der) / 2
        }
