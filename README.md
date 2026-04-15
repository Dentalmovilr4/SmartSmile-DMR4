# 🦷 SmartSmile-DMR4
### Diseño Digital de Sonrisa Prototipo con IA

**SmartSmile-DMR4** es una herramienta avanzada desarrollada para odontólogos que permite realizar simulaciones estéticas dentales de forma automática utilizando Inteligencia Artificial. El proyecto está optimizado para funcionar en entornos móviles y entornos de desarrollo en la nube como GitHub Codespaces.

## 🚀 Características Principales
* **Detección Facial:** Identificación automática de la línea media y el plano oclusal.
* **Análisis Biométrico:** Clasificación de la forma del rostro (Ovalado, Cuadrado, Corazón) para sugerir la mejor morfología dental.
* **Máscara de Labios:** Los dientes se integran de forma realista detrás de los labios del paciente.
* **Procesamiento Móvil:** Diseñado para ser gestionado desde dispositivos Android (Oppo A57) mediante Termux y Acode.

## 📁 Estructura del Proyecto
- `src/face_analyzer.py`: Motor de IA para detección de puntos anatómicos.
- `src/dental_logic.py`: Lógica de superposición y segmentación de labios.
- `assets/overlays/`: Biblioteca de prótesis dentales en formato PNG transparente.
- `app.py`: Interfaz de usuario para uso clínico.

## 🛠️ Instalación y Uso
1. Clonar el repositorio:
   `git clone https://github.com/Dentalmovilr4/SmartSmile-DMR4.git`
   2. Instalar dependencias:
      `pip install -r requirements.txt`
      3. Ejecutar la App:
         `streamlit run app.py`

         ## 👨‍💻 Desarrollador
         Proyecto gestionado por **Dentalmovilr4** - Creador Digital y Desarrollador de soluciones Agro-Tech y Dental-Tech.
         