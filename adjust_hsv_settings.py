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
cv2.namedWindow('BGRtrackbars')
cv2.createTrackbar('lowerB', 'BGRtrackbars', s.dict['lowerB'], 255, nothing)
cv2.createTrackbar('lowerG', 'BGRtrackbars', s.dict['lowerG'], 255, nothing)
cv2.createTrackbar('lowerR', 'BGRtrackbars', s.dict['lowerR'], 255, nothing)
cv2.createTrackbar('higherB', 'BGRtrackbars', s.dict['higherB'], 255, nothing)
cv2.createTrackbar('higherG', 'BGRtrackbars', s.dict['higherG'], 255, nothing)
cv2.createTrackbar('higherR', 'BGRtrackbars', s.dict['higherR'], 255, nothing)

nwt_s = Settings('./nwt_settings.txt', True)
nwt = nwtConnection(nwt_s.dict['roboRioAddress'], nwt_s.dict['sdTableName'], nwt_s.dict['cpTableName'])
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
    resHSV = cv2.bitwise_and(frame, frame, mask=maskHSV)

    lowerThreshBGR = np.array([cv2.getTrackbarPos('lowerB', 'BGRtrackbars'), \
                               cv2.getTrackbarPos('lowerG', 'BGRtrackbars'), \
                               cv2.getTrackbarPos('lowerR', 'BGRtrackbars')])
    higherThreshBGR = np.array([cv2.getTrackbarPos('higherB', 'BGRtrackbars'), \
                                cv2.getTrackbarPos('higherG', 'BGRtrackbars'), \
                                cv2.getTrackbarPos('higherR', 'BGRtrackbars')])
    
    maskBGR = cv2.inRange(resHSV, lowerThreshBGR, higherThreshBGR)
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(maskBGR, cv2.MORPH_OPEN, kernel)
    median = cv2.medianBlur(opening, 5)
    resBGR = cv2.bitwise_and(resHSV, resHSV, mask=median)
    

    cv2.imshow('frame', frame)
    cv2.imshow('resHSV', resHSV)
    cv2.imshow('resBGR', resBGR)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

s.dict['lowerH'] = cv2.getTrackbarPos('lowerH', 'HSVtrackbars')
s.dict['lowerS'] = cv2.getTrackbarPos('lowerS', 'HSVtrackbars')
s.dict['lowerV'] = cv2.getTrackbarPos('lowerV', 'HSVtrackbars')
s.dict['higherH'] = cv2.getTrackbarPos('higherH', 'HSVtrackbars')
s.dict['higherS'] = cv2.getTrackbarPos('higherS', 'HSVtrackbars')
s.dict['higherV'] = cv2.getTrackbarPos('higherV', 'HSVtrackbars')
s.dict['lowerB'] = cv2.getTrackbarPos('lowerB', 'BGRtrackbars')
s.dict['lowerG'] = cv2.getTrackbarPos('lowerG', 'BGRtrackbars')
s.dict['lowerR'] = cv2.getTrackbarPos('lowerR', 'BGRtrackbars')
s.dict['higherB'] = cv2.getTrackbarPos('higherB', 'BGRtrackbars')
s.dict['higherG'] = cv2.getTrackbarPos('higherG', 'BGRtrackbars')
s.dict['higherR'] = cv2.getTrackbarPos('higherR', 'BGRtrackbars')

s.write()

cap.release()
cv2.destroyAllWindows()
