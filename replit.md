# SmartSmile-DMR4

## Overview
A digital dental design prototype that uses AI to perform aesthetic dental simulations. It analyzes a patient's face, detects anatomical landmarks, classifies facial shapes, and superimposes dental prostheses behind the lips using lip masking and biometric analysis.

## Tech Stack
- **Language:** Python 3.12
- **Web Framework:** Streamlit (runs on port 5000)
- **AI/Computer Vision:** MediaPipe (face mesh detection), OpenCV
- **Image Processing:** Pillow (PIL), NumPy

## Project Structure
```
app.py                  # Main Streamlit entry point
face_analyzer.py        # Root-level face analyzer (copied to src/)
dental_logic.py         # Root-level dental logic
src/
  face_analyzer.py      # AI engine for anatomical point detection (used by app.py)
  dental_logic.py       # Lip masking, warping, segmentation logic
assets/
  overlays/
    protesis_estandar.png  # Standard dental prosthesis overlay image
  paciente.jpg.jpeg     # Sample patient image
.streamlit/
  config.toml           # Streamlit server config (port 5000, host 0.0.0.0)
requirements.txt        # Python dependencies
```

## Running the App
The app runs via the "Start application" workflow:
```
streamlit run app.py
```

## Key Features
1. Upload a patient photo (jpg/png)
2. AI face analysis using MediaPipe (468+ facial landmarks)
3. Facial shape classification (Alargado, Cuadrado, Triangular, Ovalado)
4. Dental prosthesis overlay with lip masking and perspective warping
5. Download the resulting composite image

## Notes
- `src/face_analyzer.py` is the version used by `app.py` (copied from root `face_analyzer.py`)
- `assets/overlays/protesis_estandar.png` must exist for the design generation to work
- Streamlit config disables CORS and XSRF protection for Replit proxy compatibility
