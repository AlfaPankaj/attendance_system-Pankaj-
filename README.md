
"""🔴 Live Demo prototype: [a8xpdpndypepwkxmqzhcdd.streamlit.app]"""


# Medoc Health AI - Face Authentication Attendance System


**Internship Assignment: AI/ML Engineering (2026 Batch)** *Developed by: Pankaj Yadav*


## Overview
This is a production-ready **Biometric Attendance System** designed for Medoc Health. It utilizes computer vision and deep learning to authenticate users via facial recognition while ensuring security through **active liveness detection** (anti-spoofing).

The system is built with a **Hybrid Authentication Engine** that supports both fully automated "Walk-through" attendance and manual "Button-trigger" modes, making it adaptable for different hospital workflows.



### Key Features
* **Real-time Face Recognition:** Uses 128-d facial embeddings (ResNet) for high-accuracy identification.
* **Anti-Spoofing (Liveness):** Active blink detection using **MediaPipe Face Mesh** to prevent photo-based attacks.
* **Hybrid Operation Modes:**
    * **Auto Mode:** Automatically logs attendance the moment a verified face is detected (Zero-touch).
    * **Manual Mode:** Requires the user to click "Punch In/Out" after verification (Human-in-the-loop).
* **High Performance:** Implements **Multi-threaded Video Processing** to separate UI rendering from frame ingestion, ensuring zero lag.
* **Admin Dashboard:** secure SQLite database with CSV export for HR audits.
* **Dockerized:** Fully containerized for "Write Once, Run Anywhere" deployment.


graph TD
    User[User / Employee] -->|Webcam Feed| Camera[Threaded Camera Module]
    Camera -->|Frame Stream| Liveness[Liveness Detector \n(MediaPipe Mesh)]
    
    Liveness -- "If Blink Detected" --> FaceRec[Face Recognition \n(ResNet-34)]
    Liveness -- "No Blink" --> UI[User Interface \n(Streamlit)]
    
    FaceRec -- "Match Found" --> DB[(SQLite Database)]
    FaceRec -- "Unknown" --> Alert[Alert: Unknown User]
    
    DB -->|Logs & History| Admin[Admin Dashboard]
    
    subgraph "Core Engine"
    Camera
    Liveness
    FaceRec
    end



## Technical Architecture

### Tech Stack
* **Language:** Python 3.9+
* **Core CV:** OpenCV, MediaPipe (Google), Dlib
* **ML Model:** `face_recognition` (HOG + Linear SVM / CNN)
* **Interface:** Streamlit (Reactive Web UI)
* **Database:** SQLite3 (Embedded Relational DB)
* **Concurrency:** Python `threading` module for non-blocking camera I/O.



### Folder Structure
```text
medoc_attendance/
│
├── src/
│   ├── camera.py          # Multi-threaded camera class (Performance optimized)
│   ├── database.py        # SQLite handler with cooldown logic
│   ├── face_utils.py      # Face detection & encoding logic
│   └── liveness.py        # MediaPipe blink detection algorithm
│
├── data/
│   ├── attendance_v.db    # Persistent storage for logs
│   └── embeddings.pkl     # Encrypted biometric signatures
│
├── app.py                 # Main application controller (Streamlit)
├── Dockerfile             # Container configuration
└── requirements.txt       # Dependency manifest



🚀 Future Roadmap (Production Scaling)
--Cloud Storage: Migrate SQLite to PostgreSQL (AWS RDS) for concurrent write access across multiple hospital wings.

--Edge Computing: Move the dlib inference to an edge device (like NVIDIA Jetson Nano) to reduce server latency.

--Security: Encrypt the embeddings.pkl file using AES-256 to comply with HIPAA (Health Data Privacy) regulations.

--Multi-Camera Support - Multiple entry points monitoring

--Cloud Integration - Google Drive/AWS backup and sync

--Mobile App - React Native app with QR code backup

--Advanced Analytics - Attendance trends, heat maps, insights

--Geofencing - GPS/WiFi location verification

--Voice Recognition - Multi-factor authentication (Face + Voice)

--Smart Shift Management - Automatic shift recognition, break tracking

--AI Anomaly Detection - ML-powered fraud detection and wellness monitoring
