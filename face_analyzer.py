import cv2
import numpy as np
import mediapipe as mp

# Forzamos la carga de las soluciones de forma robusta
import mediapipe.solutions.face_mesh as mp_face_mesh

class FaceAnalyzer:
    def __init__(self):
        # Configuramos el motor con los parámetros de alta precisión
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True, # Indispensable para detectar el borde de los labios
            min_detection_confidence=0.5
        )

    def analizar_paciente(self, image_path):
        # 1. Cargar y validar imagen
        image = cv2.imread(image_path)
        if image is None: 
            return f"Error: No se encontró la imagen en {image_path}"

        h, w, _ = image.shape
        # Convertir a RGB para Mediapipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            return "Error: No se detectó rostro en la foto"

        # Obtenemos los puntos detectados
        puntos = results.multi_face_landmarks[0].landmark

        # Función para convertir coordenadas normalizadas a píxeles
        def get_p(i):
            return np.array([puntos[i].x * w, puntos[i].y * h])

        # --- EXTRACCIÓN DE BIOMETRÍA DENTAL ---
        
        # 1. Línea Media (Referencia vertical para centrar la prótesis)
        nasion = get_p(168)
        pogonion = get_p(152)

        # 2. Comisuras Labiales (Definen el ancho de la sonrisa)
        izq_labio = get_p(61)
        der_labio = get_p(291)

        # 3. Puntos para segmentación de labios (Pilar del Realismo)
        # Guardamos los puntos crudos para que dental_logic.py pueda crear la máscara
        coords_crude = [[p.x * w, p.y * h] for p in puntos]

        # 4. Mediciones de Forma Facial
        frente_w = np.linalg.norm(get_p(103) - get_p(332))
        pomulo_w = np.linalg.norm(get_p(234) - get_p(454))
        mandibula_w = np.linalg.norm(get_p(58) - get_p(288))
        cara_l = np.linalg.norm(get_p(10) - get_p(152))

        # --- CLASIFICACIÓN MORFOLÓGICA ---
        forma = "Ovalado"
        if cara_l > pomulo_w * 1.3:
            forma = "Alargado"
        elif abs(pomulo_w - mandibula_w) < (pomulo_w * 0.12):
            forma = "Cuadrado"
        elif frente_w > mandibula_w * 1.15:
            forma = "Corazón/Triangular"

        # --- RETORNO DE DATOS ---
        return {
            "forma_rostro": forma,
            "linea_media": (nasion.tolist(), pogonion.tolist()),
            "plano_oclusal": (izq_labio.tolist(), der_labio.tolist()),
            "ancho_boca": np.linalg.norm(der_labio - izq_labio),
            "centro_boca": ((izq_labio + der_labio) / 2).tolist(),
            "angulo_inclinacion": np.degrees(np.arctan2(der_labio[1] - izq_labio[1], der_labio[0] - izq_labio[0])),
            "coords_crude": coords_crude # Estos datos van para la máscara de labios
        }

