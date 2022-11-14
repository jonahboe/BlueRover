from fer import FER
import threading
import cv2

class Emotion(threading.Thread):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_detector = FER(mtcnn=True)
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.render = False

    def __del__(self):
        cv2.destroyAllWindows()
        
    def run(self, args):    
        success, image = self.cam.read()
        while True:
            success, image = self.cam.read()
            if not success:
                print("!!! Failed vid.read()")
                break
            image = cv2.flip(image, 1)

            gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
            faces = self.face_cascade.detectMultiScale(gray_img, 1.25, 4)
            for i in range(len(faces)): 
                (x,y,w,h) = faces[i]
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)  
                rec_gray = gray_img[y:y+h, x:x+w] 
                rec_color = image[y:y+h, x:x+w] 

                captured_emotions = self.emotion_detector.detect_emotions(image)
                if len(captured_emotions) == len(faces):
                    emotions = captured_emotions[i]['emotions']
                    offset = 20
                    for key in emotions.keys():
                        cv2.putText(img=image, text=(str(key) + ": " + str(emotions[key])), org=(x, y+h+offset), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=.5, color=(0, 255, 0),thickness=1)
                        offset += 20
            if self.render:
                cv2.imshow("video", image)

            if cv2.waitKey(1) == 27: 
                self.delete()
                break
