from nwtConnection import nwtConnection
from GearTracker import GearTracker
from HookTracker import HookTracker
from Settings import Settings
import math, cv2, numpy as np

nwt_s = Settings('./nwt_settings.txt', True)
nwt = nwtConnection(nwt_s.dict['roboRioAddress'], nwt_s.dict['sdTableName'], nwt_s.dict['cpTableName'])
gt = GearTracker('./templates/')
ht = HookTracker(Settings('./hsv_settings.txt'), './hook_bitmap.png')
s = Settings('./settings.txt')

nwt.find_stream()

cap = cv2.VideoCapture(nwt.streamURL)

while True:

    ret, frame = cap.read()

    if ret and nwt.sd.getBoolean("Tracking", False):

        if nwt.sd.getString("Target", '') == "gear":

            tracking, topLeft, bottomRight, ph, pw = gt.track(frame)

            if tracking:

                hdist = (s.dict['cameraHeight'] - s.dict['gearHeight']) * math.tan(math.radians(s.dict['maxAngle'] - ph/s.dict['phMax']*s.dict['vFOV']))
                offset = (pw - s.dict['pwCenter']) / s.dict['pwCenter']
                nwt.sd.putNumber("hdist", hdist)
                nwt.sd.putNumber("offset", offset)

            else:

                nwt.sd.putNumber("hdist", -1)

        if nwt.sd.getString("Target", '') == "hook":

            tracking, rects, ph, pw = ht.track(frame)

            if tracking:
                
                hdist = (s.dict['cameraHeight'] - s.dict['tapeHeight']) * math.tan(math.radians(s.dict['maxAngle'] - ph/s.dict['phMax']*s.dict['vFOV']))
                offset = (pw - s.dict['pwCenter']) / s.dict['pwCenter']
                nwt.sd.putNumber("hdist", hdist)
                nwt.sd.putNumber("offset", offset)

            else:
                
                nwt.sd.putNumber("hdist", -1)
                
    else:

        nwt.sd.putNumber("hdist", -2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

            
