import cv2
import threading
import time

class ThreadedCamera:
    def __init__(self, source=0):
        self.capture = cv2.VideoCapture(source)
        self.is_running = True
        self.current_frame = None
        
        success, frame = self.capture.read()
        if success:
            self.current_frame = frame
            
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        """Constantly reads the camera in the background."""
        while self.is_running:
            if self.capture.isOpened():
                success, frame = self.capture.read()
                if success:
                    self.current_frame = cv2.flip(frame, 1)
                else:
                    time.sleep(0.01)

    def get_frame(self):
        """Returns the latest available frame instantly."""
        return self.current_frame

    def stop(self):
        self.is_running = False
        self.capture.release()