import cv2
from nwtConnection import nwtConnection
from Settings import Settings

nwt_s = Settings('./nwt_settings.txt', True)
nwt = nwtConnection(nwt_s.dict['roboRioAddress'], nwt_s.dict['sdTableName'], nwt_s.dict['cpTableName'])

nwt.find_stream()

cap = cv2.VideoCapture(nwt.streamURL)

while True:

    ret, frame = cap.read()

    if ret:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
