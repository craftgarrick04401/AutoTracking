from nwtConnection import nwtConnection
from GearTracker import GearTracker
from Settings import Settings

nwt = nwtConnection('roborio-4546-frc.local', '/SmartDashboard/', '/CameraPublisher/USB Camera 0/')
gt = GearTracker('./templates')
s = Settings('./settings.txt')

nwt.find_stream()

cap = cv2.VideoCapture(nwt.streamURL)

while True:

    ret, frame = cap.read()

    if ret and nwt.sd.getBoolean("Tracking", False):

        if nwt.sd.getString("Tracker", '') == "gear":

            tracking, topLeft, bottomRight, ph, pw = gt.track(frame)

            if tracking:

                hdist = (s.dict['cameraHeight'] - s.dict['gearHeight']) * math.tan(math.radians(s.dict['maxAngle'] - ph/s.dict['phMax']*s.dict['vFOV']))
                offset = (pw - s.dict['pwCenter']) / s.dict['pwCenter']
                nwt.sd.putNumber("hdist", hdist)
                nwt.sd.putNumber("offset", offset)

            else:

                nwt.sd.putNumber("hdist", -1)

        if nwt.sd.getString("Tracker", '') == "hook":
            pass

    else:

        nwt.sd.putNumber("hdist", -2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

            
