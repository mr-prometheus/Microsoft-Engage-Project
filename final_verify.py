import face_recognition
import cv2
import numpy as np

def verify_image():
    global i,verified,j
    verified = 0
    j=1
    i = 0


    # Load a sample picture and learn how to recognize it.
    Deepan_image = face_recognition.load_image_file("Deepan/Deepan.jpg")
    Deepan_face_encoding = face_recognition.face_encodings(Deepan_image)[0]
    
    # mole_image = face_recognition.load_image_file("Anmol/Anmol.jpg")
    # mole_face_encoding = face_recognition.face_encodings(mole_image)[0]
    Navneet_image = face_recognition.load_image_file("Navneet/Navneet.jpg")
    Navneet_face_encoding = face_recognition.face_encodings(Navneet_image)[0]
    # Create arrays of known face encodings and their names
    known_face_encodings = [
        Deepan_face_encoding,
        Navneet_face_encoding,
        
    ]
    known_face_names = [
        "Deepan",
        "Navneet"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while j<=11:
        file_name_path = "D:\Programming World\Another Testing Folder\Sample Testing - database\Photo/"+str("Photo")+str(j)+'.jpg'
        #video_capture = cv2.imread(file_name_path)
        frame = cv2.imread(file_name_path)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    #print(name)
                    i+=1

                face_names.append(name)
        j+=1
        if i>5:
            #print(name)
            return name
        
    # Display the resulting image
 
