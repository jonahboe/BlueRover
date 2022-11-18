from copy import deepcopy
from playsound import playsound
from fer import FER
import face_recognition
import threading
import cv2

class FacialRecognition(threading.Thread):
    def __init__(self):
        super().__init__()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_detector = FER(mtcnn=True)
        owner_image = face_recognition.load_image_file("images/owner.jpg")
        self.owner_face_encoding = face_recognition.face_encodings(owner_image)[0]
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.render = False
        self.location = None
        self.owner = False

    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def detectID(self, frame, render=False):
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        # check if owner      
        face_names = []
        for face_encoding in face_encodings:
            name = '???'
            # See if the face is a match for the known face
            match = face_recognition.compare_faces([self.owner_face_encoding], face_encoding)[0]
            if match: 
                self.owner = True
                name = 'Owner'
            face_names.append(name)
        if self.owner and render:
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1) 
    
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
        emThread = threading.Thread(target=self.detectEmotion)
        idThread = threading.Thread(target=self.detectID)
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
            # If there is a person
            if len(faces) > 0:
                # Find the center location of the person
                (x,y,w,h) = faces[0]
                self.location = ((x+w/2)-320, (y+h/2)-180)
                # Draw box for rendering people location
                if self.render:
                    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
            # Otherwise set the person location to none
            else:
                self.location = None

            # Render the video feed
            if self.render:
                cv2.imshow("video", image)
            
            # If we are finished reading the last emotion detected, then detect the next emotion
            if not emThread.is_alive():
                myThread = threading.Thread(target=self.detectEmotion, args=(deepcopy(image), self.emotion_detector))
                myThread.start()
            if not idThread.is_alive():
                myThread = threading.Thread(target=self.detectID, args=(deepcopy(image), True))
                myThread.start()

            if cv2.waitKey(1) == 27: 
                cv2.destroyAllWindows()
                break