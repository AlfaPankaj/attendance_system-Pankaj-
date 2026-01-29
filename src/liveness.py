import cv2
import mediapipe as mp
import numpy as np

class LivenessDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        
        self.blink_count = 0
        self.eye_closed = False

    def calculate_ear(self, landmarks, indices):
        A = np.linalg.norm(landmarks[indices[1]] - landmarks[indices[5]])
        B = np.linalg.norm(landmarks[indices[2]] - landmarks[indices[4]])
        C = np.linalg.norm(landmarks[indices[0]] - landmarks[indices[3]])
        return (A + B) / (2.0 * C)

    def check_liveness(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w, _ = frame.shape
                landmarks = np.array([(p.x * w, p.y * h) for p in face_landmarks.landmark])

                left_ear = self.calculate_ear(landmarks, self.LEFT_EYE)
                right_ear = self.calculate_ear(landmarks, self.RIGHT_EYE)
                avg_ear = (left_ear + right_ear) / 2.0
                
                if avg_ear < 0.25:
                    self.eye_closed = True
                elif self.eye_closed: 
                    self.blink_count += 1
                    self.eye_closed = False
                    
                for i in self.LEFT_EYE + self.RIGHT_EYE:
                    cv2.circle(frame, (int(landmarks[i][0]), int(landmarks[i][1])), 1, (0, 255, 0), -1)

        return self.blink_count > 0, frame