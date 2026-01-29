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




Installation & Setup
Option 1: Quick Start (Local)
Clone the repository: 
Install Dependencies: Note: Requires C++ Build Tools for Dlib (Windows): pip install -r requirements.txt
Run the App: streamlit run app.py