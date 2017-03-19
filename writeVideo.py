import cv2, numpy as np
from nwtConnection import nwtConnection

nwt = nwtConnection('roborio-4546-frc.local', '/SmartDashboard/', '/CameraPublisher/USB Camera 0/')

nwt.find_stream()

cap = cv2.VideoCapture(nwt.streamURL)
fourcc =cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,480))

while True:

    ret, frame = cap.read()

    if ret:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)
        out.write(gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
out.release()
cap.release()
cv2.destroyAllWindows()
