from GearTracker import GearTracker
from Settings import Setings
from nwtConnection import nwtConnection
import math, cv2

nwt_s = Settings('./nwt_settings.txt', True)
nwt = nwtConnection(nwt_s.dict['roboRioAddress'], nwt_s.dict['sdTableName'], nwt_s.dict['cpTableName'])
gt = GearTracker('./templates')
s = Settings('./settings.txt')

nwt.find_stream()

cap = cv2.VideoCapture(nwt.streamURL)

while True:

    ret, frame = cap.read()

    if ret:

        tracking, topLeft, bottomRight, ph = gt.track(frame)

        if tracking:

            cv2.rectangle(frame, topLeft, bottomRight, (0,0,255), 3)

        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if ph == None:
    print("Gear was not detected.")
    os._exit(0)

hdist = float(input("hdist"))
s.dict['cameraHeight'] = float(input("cameraHeight"))
s.dict['MaxAngle'] = math.degrees(math.atan(hdist/s.dict['cameraHeight'])) + ph/s.dict['phMax']*s.dict['vFOV']

print("MaxAngle: " + str(s.dict['MaxAngle']))

s.write()
