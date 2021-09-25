This project controls a robotic car on the basis of Hand Gestures.

Libraries used- Mediapipe, OpenCv, Socket in python
Hardware used to control the car- ESP8266
Protocol used for information exchange- TCP.

The NodeMcu acts as the server and waits for signal from the PC that acts as client.

In the Python Code, the MediaPipe Library is used to detect the 21 hand landmarks. Based on the relative positioning of the landmarks, the finger count is detected and the 
same is sent to the server to control the car.

