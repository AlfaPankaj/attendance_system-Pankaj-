import face_recognition
import pickle
import os
import cv2
import numpy as np


ENCODINGS_PATH = os.path.join("data", "embeddings.pkl")

def load_known_faces():
    """Loads known face encodings from the pickle file."""
    if not os.path.exists(ENCODINGS_PATH):
        return [], []

    with open(ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)
    
    return data["encodings"], data["names"]

def save_known_faces(encodings, names):
    """Saves new encodings to the pickle file."""
    data = {"encodings": encodings, "names": names}
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)

def register_new_user(frame, name):
    """
    Detects a face in the frame and saves it as a new user.
    Returns: (Success Boolean, Message)
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    boxes = face_recognition.face_locations(rgb_frame, model="hog")
    
    if len(boxes) == 0:
        return False, "No face detected. Please look at the camera."
    
    if len(boxes) > 1:
        return False, "Multiple faces detected. Please ensure only you are in frame."
    
    encoding = face_recognition.face_encodings(rgb_frame, boxes)[0]
    

    known_encodings, known_names = load_known_faces()
    
    if len(known_encodings) > 0:
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
        if True in matches:
            return False, "User already registered!"

    known_encodings.append(encoding)
    known_names.append(name)
    save_known_faces(known_encodings, known_names)
    
    return True, f"User {name} registered successfully!"

def recognize_face(frame):
    """
    Identifies a face in the frame.
    Returns: (Name, Confidence) or (None, 0)
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    known_encodings, known_names = load_known_faces()
    
    if not known_encodings:
        return "Unknown", 0.0

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if not face_encodings:
        return None, 0.0

    for encoding in face_encodings:
        face_distances = face_recognition.face_distance(known_encodings, encoding)
        best_match_index = np.argmin(face_distances)
        
        if face_distances[best_match_index] < 0.5:
            name = known_names[best_match_index]
            confidence = 1.0 - face_distances[best_match_index] 
            return name, confidence
            
    return "Unknown", 0.0