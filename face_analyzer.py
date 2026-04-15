import cv2
import mediapipe as mp
import numpy as np

class FaceAnalyzer:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        # Activamos refine_landmarks para máxima precisión en labios
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True
        )

    def analizar_paciente(self, image_path):
        # 1. Cargar y validar imagen
        image = cv2.imread(image_path)
        if image is None: 
            return "Error: No se pudo leer la imagen"
        
        h, w, _ = image.shape
        results = self.face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if not results.multi_face_landmarks:
            return "Error: No se detectó rostro"

        coords = results.multi_face_landmarks[0].landmark
        
        # Función interna para convertir puntos a píxeles reales
        def get_p(i):
            return np.array([coords[i].x * w, coords[i].y * h])

        # --- EXTRACCIÓN DE PUNTOS CLAVE ---
        # Línea Media (Nasion a Mentón)
        nasion = get_p(168)
        pogonion = get_p(152)
        
        # Plano Oclusal (Comisuras de los labios)
        izq_labio = get_p(61)
        der_labio = get_p(291)
        
        # Puntos para forma de rostro
        frente_w = np.linalg.norm(get_p(103) - get_p(332))
        pomulo_w = np.linalg.norm(get_p(234) - get_p(454))
        mandibula_w = np.linalg.norm(get_p(58) - get_p(288))
        cara_l = np.linalg.norm(get_p(10) - get_p(152))

        # --- LÓGICA DE CLASIFICACIÓN ESTÉTICA ---
        # Determinación de la forma del rostro
        forma = "Ovalado"
        if cara_l > pomulo_w * 1.3:
            forma = "Alargado"
        elif abs(pomulo_w - mandibula_w) < (pomulo_w * 0.1):
            forma = "Cuadrado"
        elif frente_w > mandibula_w * 1.1:
            forma = "Corazón/Triangular"

        # --- RESULTADO FINAL ---
        return {
            "forma_rostro": forma,
            "linea_media": (nasion.tolist(), pogonion.tolist()),
            "plano_oclusal": (izq_labio.tolist(), der_labio.tolist()),
            "ancho_boca": np.linalg.norm(der_labio - izq_labio),
            "centro_boca": ((izq_labio + der_labio) / 2).tolist(),
            "angulo_inclinacion": np.degrees(np.arctan2(der_labio[1] - izq_labio[1], der_labio[0] - izq_labio[0]))
        }

