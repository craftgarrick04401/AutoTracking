from HookTracker import HookTracker
from Settings import Settings
from nwtConnection import nwtConnection
import math, cv2

nwt = nwtConnection('roborio-4546-frc.local', '/SmartDashboard/', '/CameraPublisher/USB Camera 0/')
ht = HookTracker(Settings('./hsv_settings.txt'), './hook_bitmap.png')
s = Settings('./settings.txt')

nwt.find_stream()

cap = cv2.VideoCapture(nwt.streamURL)

while True:

    ret, frame = cap.read()

    if ret:

        tracking, rects, ph, pw = ht.track(frame)

        if tracking:

            for i in rects:
                x,y,w,h = i
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 3)

        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if ph == None:
    print("Hook was not detected.")
    os._exit(0)

hdist = float(input("hdist"))
s.dict['cameraHeight'] = float(input("cameraHeight"))
s.dict['MaxAngle'] = math.degrees(math.atan(hdist/s.dict['cameraHeight'])) + ph/s.dict['phMax']*s.dict['vFOV']

print("MaxAngle: " + str(s.dict['MaxAngle']))

s.write()
