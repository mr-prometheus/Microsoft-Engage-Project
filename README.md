Hello Greeting Everyone. Before you run this program in your terminal make sure you go through this document to the end.
1. pip install all the libraries given in the requirements.txt
2. Make sure you installed cmake, dlib before face_Recognition else it will not install. If you are not able to install
   dlib, I have included the file in this repository. Go to the directory command line then pip install "dlib-19.22.99-cp310-cp310-win_amd64.whl". 
   You are good to go.
3. After you have installed all the libraries as mentioned above you have to change the directories in the respective files.
4. Go to app.py then to line number 56 file_name_path ='Add your directory path of Photo folder within this file'
5. Go to final_verify.py to line number 38 file_name_path and add the same path as in point 4
6. Also you have to add your photo to verify your face, in final_verify.py go to line number 13, make a New folder with your name
   For example if your name is Krishna, make Folder named "Krishna" with a good quality picture of yours name "Krishna.jpg" in it.
7. Then in final_verify.py in line number 26 known_face_names add your name respective to the encoding as above.(If there are 2 encodings,
   then there should be 2 names out there).
8. Now you are ready to go.
9. To start the program, Run app.py in the command line and go to the local host link generated.

**Features**:
•	AI Based Face Recognition
•	Device Security
•	AirBoard - Virtual Drawing Board using Hand Gestures
•	Readifyme - Scroll Pages using computer vision
•	Gamestation - Play Snake Game using face recognition computer vision technology 
•	Attendance Board - See who logged into the system and when 


**Tech Stack**:
•	Front End: HTML,CSS, JAVASCRIPT
•	Backend- Flask
•	Database – SQLAlchemy
•	Technologies/libraries used – Numpy, OpeCV, Face_Recognition, Mediapipe, CVZONE, Pyautogui

