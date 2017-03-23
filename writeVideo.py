import cv2, numpy as np
from nwtConnection import nwtConnection
from Settings import Settings

nwt_s = Settings('./nwt_settings.txt', True)
nwt = nwtConnection(nwt_s.dict['roboRioAddress'], nwt_s.dict['sdTableName'], nwt_s.dict['cpTableName'])

nwt.find_stream()

cap = cv2.VideoCapture(nwt.streamURL)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out.write(frame)
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
