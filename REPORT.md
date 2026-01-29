                    
                    Technical Report: Face Authentication System
Submitted by: [Pankaj]                    For: Medoc Health AI Intern Assignment



                              Model and Approach Used
To balance real-time performance with high accuracy, this system utilizes a Hybrid Architecture:

Face Detection: Uses HOG (Histogram of Oriented Gradients) for rapid face localization on CPU.

Face Recognition: Utilizes the dlib ResNet-34 model, pre-trained on the Labeled Faces in the Wild (LFW) dataset. This model maps a face to a 128-dimensional hypersphere, where the Euclidean distance between vectors represents face similarity.

Anti-Spoofing (Liveness):

Algorithm: Google MediaPipe Face Mesh.

Logic: Tracks 468 3D facial landmarks to calculate the Eye Aspect Ratio (EAR).

Trigger: A deliberate "Blink" action (EAR < 0.25) is required to prove liveness, effectively filtering out static 2D photos.




                             The Training Process (One-Shot Learning)
Unlike traditional classification models that require thousands of images per class, this system employs One-Shot Learning.

Enrollment Phase: When a user registers, the system computes the 128-d embedding vector of their face immediately.

Storage: This vector is stored in a secure pickle file (embeddings.pkl) alongside the user's metadata.

Inference: During attendance, the live face vector is compared against stored vectors using Euclidean Distance. No retraining is required to add new employees.




                            Accuracy Expectations
Based on the underlying dlib ResNet model benchmarks:

LFW Benchmark Accuracy: 99.38%

False Positive Rate: < 1% when using a distance threshold of 0.5.

Liveness Detection: MediaPipe tracks landmarks with sub-millimeter precision, making the blink detection robust against basic photo attacks.




                             Known Failure Cases & Limitations
In the spirit of engineering transparency, the following limitations are identified:

Extreme Lighting: Strong backlighting (e.g., a window behind the user) silhouettes the face, preventing HOG detection. Mitigation: Added CLAHE preprocessing in code.

Occlusions: Heavy eyewear or face masks block landmark detection, causing the Liveness check to fail.

Extreme Angles: The model performs best on frontal faces. Yaw angles > 30 degrees increase the Euclidian distance, leading to potential "Unknown User" classifications.

Twin Paradox: As with most biometric systems, identical twins may result in False Acceptances due to extremely similar embedding vectors.

                           Final Packaging Instructions
To submit your assignment professionally:

Folder: attendance_system[Pankaj]

data/
src/
app.py
Dockerfile
requirements.txt
README.md
REPORT.md (The text above)
