import cv2, numpy as np

class HookTracker(object):

    def __init__(self, settings):

        self.s = settings

    def track(self, frame):

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lowerThresh = np.array(self.s.dict['lowerH'], self.s.dict['lowerS'], self.s.dict['lowerV'])
        higherThresh = np.array(self.s.dict['higherH'], self.s.dict['higherS'], self.s.dict['higherV'])

        mask = cv2.inRange(hsv, lowerThresh, higherThresh)
        median = cv2.medianBlur(maskHSV, 5)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        
        
