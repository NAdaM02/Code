import cv2
import own.tools as ot
import time

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

number = 1
now = time.gmtime()
detections = []

# To capture video from webcam.
cap = cv2.VideoCapture(0)
# To use a video file as input
#cap = cv2.VideoCapture("")

while True:
    # Read the frame
    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.15, 4)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        now = time.gmtime()
        detections.append((number,now[3],now[4],now[5],time.time()))
        number+=1

    # Display
    cv2.imshow('img', img)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release the VideoCapture object
cap.release()
ot.p(detections)
ot.pn("")
i=0
all_in_all = 0
while(i <= len(detections)-1):
    seek = i
    together = True
    first = 0
    last = 0
    count = 0
    while(together and seek + 1 < len(detections)):
        if (detections[seek][4]+0.2 >= detections[seek+1][4]):
            if(count == 0):
                first = seek
            last = seek+1
            count += 1
            seek+=1
        else:
            together = False
    i+=seek-i+1
    if(count >= 10):
        if(detections[first][1]+2 >= 24):
            print(str(detections[first][1] + 2 - 24 + 1) + ":" + str(detections[first][2]) + ":" + str(detections[first][3]) + " - " + str(detections[last][1] + 2 - 24 + 1) + ":" + str(detections[last][2]) + ":" + str(detections[last][3]))
        else:
            print(str(detections[first][1] + 2 + 1) + ":" + str(detections[first][2]) + ":" + str(detections[first][3]) + " - " + str(detections[last][1] + 2 + 1) + ":" + str(detections[last][2]) + ":" + str(detections[last][3]))
        ot.p("Number of detections: " + str(last-first))
        ot.p("Seconds: " + str(int((detections[last][1] - detections[first][1]) * 3600 + (detections[last][2] - detections[first][2]) * 60 - detections[first][3] + detections[last][3])))
        all_in_all += int((detections[last][1] - detections[first][1]) * 3600 + (detections[last][2] - detections[first][2]) * 60 - detections[first][3] + detections[last][3])
        ot.p("")
ot.pn("All together: "+str(all_in_all)+' seconds')
