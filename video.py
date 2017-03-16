import cv2, numpy as np, math, os

template_filenames = os.listdir('./templates')
templates = [cv2.imread('./templates/' + str(template), 0) for template in template_filenames]
template_shapes = [template.shape[::-1] for template in templates]



cap = cv2.VideoCapture(0)

maxAngle = 109.11284593595938 # This needs to be calibrated before every match
cameraHeight = 29 + 3/16
targetHeight = 2
pMax = 480
vFOV = 38.243

while True:

    ret, frame = cap.read()

    if ret:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        matches = [cv2.matchTemplate(gray, template, cv2.TM_SQDIFF_NORMED) for template in templates]
        res = [cv2.minMaxLoc(match) for match in matches]
        min_vals, max_vals, min_locs, max_locs = zip(*res)
        if min_val < 0.04:
            min_val = min(min_vals)
            for i in range(len(res)):
                if min_vals[i] == min_val:
                    min_loc = min_locs[i] # top left point
                    w, h = template_shapes[i]
                    res = matches[i]
                    break
                
            bottom_right = (min_loc[0] + w, min_loc[1] + h)
            cv2.rectangle(frame, min_loc, bottom_right, (0,0,255), 3)

        
        
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
