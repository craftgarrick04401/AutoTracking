from nwtConnection import nwtConnection
from Settings import Settings
import cv2, numpy as np

def nothing(x):
    pass

s = Settings('./hsv_settings.txt')

cv2.namedWindow('HSVtrackbars')
cv2.createTrackbar('lowerH', 'HSVtrackbars', s.dict['lowerH'], 255, nothing)
cv2.createTrackbar('lowerS', 'HSVtrackbars', s.dict['lowerS'], 255, nothing)
cv2.createTrackbar('lowerV', 'HSVtrackbars', s.dict['lowerV'], 255, nothing)
cv2.createTrackbar('higherH', 'HSVtrackbars', s.dict['higherH'], 255, nothing)
cv2.createTrackbar('higherS', 'HSVtrackbars', s.dict['higherS'], 255, nothing)
cv2.createTrackbar('higherV', 'HSVtrackbars', s.dict['higherV'], 255, nothing)

nwt = nwtConnection('roborio-4546-frc.local', '/SmartDashboard/', '/CameraPublisher/USB Camera 0/')
nwt.find_stream()

cap = cv2.VideoCapture(nwt.streamURL)

while True:

    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerThreshHSV = np.array([cv2.getTrackbarPos('lowerH', 'HSVtrackbars'), \
                               cv2.getTrackbarPos('lowerS', 'HSVtrackbars'), \
                               cv2.getTrackbarPos('lowerV', 'HSVtrackbars')])
    higherThreshHSV = np.array([cv2.getTrackbarPos('higherH', 'HSVtrackbars'), \
                                cv2.getTrackbarPos('higherS', 'HSVtrackbars'), \
                                cv2.getTrackbarPos('higherV', 'HSVtrackbars')])

    maskHSV = cv2.inRange(hsv, lowerThreshHSV, higherThreshHSV)
    median = cv2.medianBlur(maskHSV, 5)
    resHSV = cv2.bitwise_and(frame, frame, mask=median)

    cv2.imshow('maskHSV', maskHSV)
    cv2.imshow('frame', frame)
    cv2.imshow('resHSV', resHSV)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

s.dict['lowerH'] = cv2.getTrackbarPos('lowerH', 'HSVtrackbars')
s.dict['lowerS'] = cv2.getTrackbarPos('lowerS', 'HSVtrackbars')
s.dict['lowerV'] = cv2.getTrackbarPos('lowerV', 'HSVtrackbars')
s.dict['higherH'] = cv2.getTrackbarPos('higherH', 'HSVtrackbars')
s.dict['higherS'] = cv2.getTrackbarPos('higherS', 'HSVtrackbars')
s.dict['higherV'] = cv2.getTrackbarPos('higherV', 'HSVtrackbars')

s.write()

cap.release()
cv2.destroyAllWindows()
