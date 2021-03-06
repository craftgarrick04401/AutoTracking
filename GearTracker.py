import os, cv2, numpy as np, math
from Settings import Settings
from nwtConnection import nwtConnection

class GearTracker(object):

    def __init__(self, templateDir):

        self.templateDir = templateDir
        self.template_filenames = os.listdir(self.templateDir)
        self.templates = [cv2.imread(self.templateDir + str(template), 0) for template in self.template_filenames]
        self.template_shapes = [template.shape[::-1] for template in self.templates]

    def track(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        matches = [cv2.matchTemplate(gray, template, cv2.TM_SQDIFF) for template in self.templates]
        res = [cv2.minMaxLoc(match) for match in matches]
        min_vals, max_vals, min_locs, max_locs = zip(*res)
        min_val = min(min_vals)
        if min_val != None:
            for i in range(len(res)):
                if min_vals[i] == min_val:
                    min_loc = min_locs[i] # top left point
                    w, h = self.template_shapes[i]
                    res = matches[i]
                    break
                    
            bottom_right = (min_loc[0] + w, min_loc[1] + h)
            cv2.rectangle(frame, min_loc, bottom_right, (0,0,255), 3)
            cv2.imshow('this', matches[0])

            ph = min_loc[1]
            pw = math.ceil((min_loc[0] + h)/2)

            return True, min_loc, bottom_right, ph, pw

        return False, None, None, None, None

if __name__ == '__main__':

    nwt_s = Settings('./nwt_settings.txt', True)
    nwt = nwtConnection(nwt_s.dict['roboRioAddress'], nwt_s.dict['sdTableName'], nwt_s.dict['cpTableName'])
    gt = GearTracker('./templates/')

    nwt.find_stream()

    cap = cv2.VideoCapture(nwt.streamURL)

    while True:

        ret, frame = cap.read()

        if ret:

            tracking, topLeft, bottomRight, ph, pw = gt.track(frame)

            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
