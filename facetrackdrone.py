import time
from djitellopy import Tello
import cv2
import numpy as np

# Initialize Tello
me = Tello()
me.connect()
print("Battery:", me.get_battery())

# Start video stream
me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 25, 0)
time.sleep(2)     #can lower or upper the drone with this value

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.5,0.5,0.1]
pError = 0

def findFace(img):
    # Ensure the correct path to the Haar Cascade file
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if faceCascade.empty():
        raise IOError("Unable to load the face cascade classifier xml file.")

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]

def trackFace( face_info, w, pid, pError):

    area = face_info[1]
    x, y = face_info[0]
    fb = 0
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:

        fb = 0

    elif area > fbRange[1]:

        fb = -20

    elif area < fbRange[0] and area != 0:

        fb = 20



    if x == 0:
       speed = 0
       error = 0

    #print(speed, fb)

    me.send_rc_control(0, fb, 0, speed)
    return error




while True:
    # Get frame from Tello
    frame_read = me.get_frame_read()
    img = frame_read.frame

    # Resize the frame for display
    img = cv2.resize(img, (w, h))

    # Convert from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect faces
    img, face_info = findFace(img)
    pError = trackFace(face_info, w, pid, pError)

    #print("Area", face_info[1])
    #print("Center",face_info[0], "Area",face_info[1])


    # Display the frame
    cv2.imshow("Image", img)

    # Wait for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

# Cleanup
cv2.destroyAllWindows()
me.streamoff()