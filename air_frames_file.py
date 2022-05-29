import cv2
import mediapipe as mp  
import numpy as np
from collections import deque
from flask import Flask, render_template, Response,request,url_for



def air_frames():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    tipIds = [4, 8, 12, 16, 20]

    black_index = 0
    green_index = 0
    red_index = 0
    voilet_index = 0

    bpoints = [deque(maxlen=1024)]
    gpoints = [deque(maxlen=1024)]
    rpoints = [deque(maxlen=1024)] 
    vpoints = [deque(maxlen=1024)]

    kernel = np.ones((5, 5), np.uint8)
    colors = [(0, 0, 0), (255,0, 0), (0, 255, 0), (0, 0, 255)]
    colorIndex = 0

    # Here is code for Canvas setup

    paintWindow = np.zeros((471, 636, 3)) + 0xFF

    #cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    hands=mp_hands.Hands()
    prev_pos = "neutral"
    while True:
        success, image = cap.read()
        
        image_height, image_width, _ = image.shape
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        results = hands.process(image)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        #left vertical line
        image = cv2.circle(image,(40,90), 20, (255,255,255),-1)
        image = cv2.circle(image,(40,140), 20, (0,0,0),-1)
        image = cv2.circle(image,(40,190),20,(255,0,0),-1)
        image = cv2.circle(image,(40,240), 20, (0,255,0),-1)
        image = cv2.circle(image,(40,290), 20, (0,0,255),-1)
        cv2.putText(
            image,
            'C',
            (32,94),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,0,0),
            2,
            cv2.LINE_AA,
        )
        #tracing the landmarks for the drawing using handlandmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x,y = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width,
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height) 
                center = (int(x),int(y))
                #making circle around the index finger tip                                                                
                cv2.circle(image, (int(x),int(y)), 20, (0, 255, 255), 2)
                #print(x,y)
                if center[0] <= 60:

                    # Clear Button

                    if 70 <= center[1] <= 110:
                        bpoints = [deque(maxlen=512)]
                        gpoints = [deque(maxlen=512)]
                        rpoints = [deque(maxlen=512)]
                        vpoints = [deque(maxlen=512)]

                        black_index = 0
                        green_index = 0
                        red_index = 0
                        voilet_index = 0

                        paintWindow[:, :, :] = 0xFF
                    elif 120 <= center[1] <= 160:
                        colorIndex = 0  # Black
                    elif 170 <= center[1] <= 210:
                        colorIndex = 1  # Voilet
                    elif 220 <= center[1] <= 260:
                        colorIndex = 2  # Green
                    elif 270 <= center[1] <= 310:
                        colorIndex = 3  # Red
                else:
                    if colorIndex == 0:
                        bpoints[black_index].appendleft(center)
                    elif colorIndex == 1:
                        vpoints[voilet_index].appendleft(center)
                    elif colorIndex == 2:
                        gpoints[green_index].appendleft(center)
                    elif colorIndex == 3:
                        rpoints[red_index].appendleft(center)
            #print("Index finger is present")
        else:
            #print("Finger is not present")
            bpoints.append(deque(maxlen=512))
            black_index += 1
            vpoints.append(deque(maxlen=512))
            voilet_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
        points = [bpoints, vpoints, gpoints, rpoints]
        for i in range(len(points)):

            for j in range(len(points[i])):

                for k in range(1, len(points[i][j])):

                    if points[i][j][k - 1] is None or points[i][j][k] \
                        is None:
                        continue
                    #drawing the line with the respective color
                    cv2.line(image, points[i][j][k - 1], points[i][j][k],
                            colors[i], 10)
        ret,buffer=cv2.imencode('.jpg',image)
        frame=buffer.tobytes()
        #returning the bytes
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')