import os, cv2, numpy as np, math.ceil

class GearTracker(object):

    def __init__(self, templateDir):

        self.templateDir = str(templateDir)
        self.template_filenames = os.listdir(self.templateDir)
        self.templates = [cv2.imread(self.templateDir + str(template), 0) for template in template_filenames]
        self.template_shapes = [template.shape[::-1] for template in templates]

    def track(self, frame):

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
            pw = ceil((min_loc[0] + h)/2)

            return True, min_loc, bottom_right, ph, pw

        return False, None, None, None, None
