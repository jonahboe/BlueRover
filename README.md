# Blue Rover
This project showcases the use of common Python libraries in developing a robotic emotional support animal. The system can roam around, identify and approach its owner, recognize emotions, and respond accordingly with audio feedback.

This project was completed as the final for the CS-6510 robotics course at Utah State University. The report for this project is located [here](https://github.com/jonahboe/BlueRover/blob/main/report.pdf).

Group members: [Jonah Boe](https://github.com/jonahboe), [Colton Hill](https://github.com/ColtonChill), [Kobra Bohlourihajar](https://github.com/Ela1624), and [Tyler Conley](https://github.com/tylerTaerak)

## Useful library links
### **face_recognition:**
This library was used for identifying the owner. See the documentation [here](https://github.com/ageitgey/face_recognition). To install the library use the command:
```
pip install face_recognition
```
### **fer:**
This library was used for recognizing emotions. See the documentation [here](https://pypi.org/project/fer/). To install the library use the command:
```
pip install fer
```
## Running the robot
In order to run the robot, use the command:
```
python main.py
```
There is a flag for rendering the webcam feed. In order to use this feature, use the command:
```
python main.py render=true
```

