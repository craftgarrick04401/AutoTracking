from networktables import NetworkTables as nwt
import numpy as np, cv2, time, logging, math, os

#initialize Networktables and get the stream url

print("Initializing Networktables...")

logging.basicConfig(level=logging.DEBUG)

nwt.initialize(server="roborio-4546-frc.local") #roborio adress

sd = nwt.getTable('/SmartDashboard/')
cp = nwt.getTable('/CameraPublisher/USB Camera 0/')

print("Connecting to RoboRio...")

while nwt.getRemoteAddress() == None:
    time.sleep(1)
print("Obtaining stream url...")
for i in range(len(cp.getKeys())):
    if cp.getKeys()[i] == 'streams':
        streamURL = cp.getStringArray(cp.getKeys()[i])[0].split("mjpg:")[1]
        print("Stream found at " + streamURL)
        break
else:
    print("Could not find stream.")
    os._exit(0)


#start video capture from stream url

print("Starting Automatic Capture...")
cap = cv2.VideoCapture(streamURL)

#start video analysis

cap = cv2.VideoCapture(streamURL)

template_filenames = os.listdir('./templates')
templates = [cv2.imread('./templates/' + str(template), 0) for template in template_filenames]
template_shapes = [template.shape[::-1] for template in templates]

while True:
    mode = input("Select mode... (match, calibration)").lower()
    if mode == 'c' or \
       mode == 'calibration' or \
       mode == 'm' or \
       mode == 'match':
        break

with open('./settings.txt', 'r') as f:
    settings = f.readlines()

if mode == 'c' or mode == 'calibration':
    lines = [settings[i].split(' ')[0] + ' ' + input(settings[i].split(' ')[0]) for i in range(len(settings)-3)]
    for i in range(2, 4):
        lines.append(settings[i])
    print(lines)
    hdist = float(input("hdist"))
    values = [eval(line.split(' ')[1]) for line in lines]
    cameraHeight, targetHeight, pMax, vFOV = values
else:
    for line in settings:
        print(line)
    values = [eval(line.split(' ')[1]) for line in settings]
    cameraHeight, targetHeight, pMax, vFOV, maxAngle = values

while True:

    tracking = sd.getBoolean("Tracking", False)
    
    ret, frame = cap.read()

    if ret and tracking:

        target = sd.getString("Target", "None")

        if target == "Hook":
            pass
        else:
        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            matches = [cv2.matchTemplate(gray, template, cv2.TM_SQDIFF_NORMED) for template in templates]
            res = [cv2.minMaxLoc(match) for match in matches]
            min_vals, max_vals, min_locs, max_locs = zip(*res)
            min_val = min(min_vals)
            if min_val < 0.08:
                for i in range(len(res)):
                    if min_vals[i] == min_val:
                        min_loc = min_locs[i] # top left point
                        w, h = template_shapes[i]
                        res = matches[i]
                        break
                    
                bottom_right = (min_loc[0] + w, min_loc[1] + h)
                cv2.rectangle(frame, min_loc, bottom_right, (0,0,255), 3)

                ph = min_loc[1]

                if mode == 'm' or mode == 'match':
                    hdist = (cameraHeight - targetHeight) * (math.tan(math.radians(maxAngle - ph/pMax*vFOV)))
                    sd.putNumber("hdist", hdist)
            else:
                sd.putNumber("hdist", -1)

            cv2.imshow('frame', frame)

    else:

        sd.putNumber("hdist", -2)
        print("Waiting for stream...")
        time.sleep(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        if mode == 'c' or mode == 'calibration':
            maxAngle = math.degrees(math.atan(hdist/cameraHeight)) + ph/pMax*vFOV
            with open('./settings.txt', 'w') as f:
                for line in lines:
                    f.write(line + '\n')
                f.write('maxAngle ' + str(maxAngle))
                
        break

cap.release()
cv2.destroyAllWindows()
