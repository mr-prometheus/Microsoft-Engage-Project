import cv2
import mediapipe as mp
import pyautogui
    
def reader_frames():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    hands=mp_hands.Hands()
    prev_pos = "neutral"
    while True:
        success, image = cap.read()
        
        image_height, image_width, _ = image.shape
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # pass by reference.
        results = hands.process(image)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        #left vertical line
        image = cv2.line(image , (image_width//2-int(image_width*0.1),0) , (image_width//2-int(image_width*0.1),image_height) , (255,255,255) , 2)
        #right vertical line
        image = cv2.line(image , (image_width//2+int(image_width*0.1),0) , (image_width//2+int(image_width*0.1),image_height) , (255,255,255) , 2)
        #top horizontal line
        image = cv2.line(image , (image_width//2-int(image_width*0.1),image_height//2-int(image_height*0.1)) , (image_width//2+int(image_width*0.1),image_height//2-int(image_height*0.1)) , (255,255,255) , 2)
        #down horizontal line
        image = cv2.line(image , (image_width//2-int(image_width*0.1),image_height//2+int(image_height*0.1)) , (image_width//2+int(image_width*0.1),image_height//2+int(image_height*0.1)) , (255,255,255) , 2)
        
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x,y = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width,
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)                                                                 
                cv2.circle(image, (int(x),int(y)), 20, (0, 255, 255), 2)
                #print(x,y)
            
                if x < (image_width//2-int(image_width*0.1)):
                    curr_pos = "left"
                    #print("left")
                elif x > (image_width//2+int(image_width*0.1)):
                    curr_pos = "right"
                    #print("right")
                elif y < (image_height//2-int(image_height*0.1)) and x > (image_width//2-int(image_width*0.1)) and x < (image_width//2+int(image_width*0.1)):
                    curr_pos = "up"
                    #print("up")
                    pyautogui.scroll(100) 
                elif y >  (image_height//2+int(image_height*0.1)) and x > (image_width//2-int(image_width*0.1)) and x < (image_width//2+int(image_width*0.1)):
                    curr_pos = "down"
                    #print("down")
                    pyautogui.scroll(-100) 
                else:
                    curr_pos = "neutral"

                if curr_pos!=prev_pos:
                    if curr_pos != "neutral":
                        pyautogui.press(curr_pos)
                    prev_pos = curr_pos
        ret,buffer=cv2.imencode('.jpg',image)
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')