# This script is just a for testing the functionality of face recognition and emotion detection.
#
# Last edit: 30 Nov, 2022 
# By: Colton Hill
#

from fer import FER
import face_recognition
import cv2
import numpy as np
import sys

# Emotions
emotion_detector = FER(mtcnn=True)

# FACE ID
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

names = [i.lower() for i in sys.argv[1:]]
if len(names)==0: names = ['colton']
print(names)
# names = ['colton','jonah','ela']
images = [face_recognition.load_image_file(f"images/{i}.jpg") for i in names]
known_face_encodings = [face_recognition.face_encodings(i)[0] for i in images]

known_face_names = [i.capitalize() for i in names]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
emotion = ''
process_this_frame = 0
loc_count = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every fourth frame of video to save time
    if process_this_frame%4==0:
        # Resize frame of video to 1/4 size for faster face recognition processing
        # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        new_face_locations = face_recognition.face_locations(rgb_small_frame)
        loc_count = loc_count+1 if len(new_face_locations)==0 else 0
        face_locations = face_locations if 4>loc_count>0 else new_face_locations
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "???"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
    
    # If we have reached the the eigth frame
    if process_this_frame == 8:
        try:
            # Capture the current emotion and pick the dominant one
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            captured_emotions = emotion_detector.detect_emotions(small_frame)
            emotions = captured_emotions[0]['emotions']
            emotion = max(emotions.items(),key=lambda x:x[1])[0]
        except:
            ...
    process_this_frame = (process_this_frame+1)%16


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, f'{name}:{emotion}', (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        # cv2.putText(frame, emotion, (left + 6, bottom +12), font, 0.5, (255, 255, 255), 1)
    
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()