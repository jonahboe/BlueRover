import copy
from playsound import playsound
from fer import FER
import threading
import cv2

class Emotion(threading.Thread):
    def __init__(self):
        super().__init__()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_detector = FER(mtcnn=True)
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.render = False

    def __del__(self):
        cv2.destroyAllWindows()
    
    def detectEmotion(self, image, emotion_detector):
        captured_emotions = emotion_detector.detect_emotions(image)
        if len(captured_emotions) > 0:
            # Determine the emotion and play the apropriate sound
            emotions = captured_emotions[0]['emotions']
            print(emotions)
            dominant = max(emotions, key=emotions.get)
            if dominant == 'happy':
                playsound('audio/happy.wav')
            elif dominant == 'sad':
                playsound('audio/whimper.wav')
        
    def run(self):
        myThread = threading.Thread(target=self.detectEmotion)
        success, image = self.cam.read()
        while True:
            # Grab the next image
            success, image = self.cam.read()
            if not success:
                print("!!! Failed vid.read()")
                break

            # Find person location
            gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
            faces = self.face_cascade.detectMultiScale(gray_img, 1.25, 4)
            if len(faces) > 0:
                print(faces[0])
                if self.render:
                    (x,y,w,h) = faces[0]
                    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
            if self.render:
                cv2.imshow("video", image)
            
            # If we are finished reading the last emotion detected, then detect the next emotion
            if not myThread.is_alive():
                myThread = threading.Thread(target=self.detectEmotion, args=(copy.deepcopy(image), self.emotion_detector))
                myThread.start()

            if cv2.waitKey(1) == 27: 
                cv2.destroyAllWindows()
                break
