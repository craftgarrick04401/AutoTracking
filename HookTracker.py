import cv2, numpy as np, math
from Settings import Settings
from nwtConnection import nwtConnection

class HookTracker(object):

    def __init__(self, settings, bitmap):

        self.s = settings
        self.bitmap = cv2.imread(bitmap, 0)
        _i, self.bitmapCont, _h = cv2.findContours(self.bitmap, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.bitmapCont = self.bitmapCont[0]

    def track(self, frame):

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lowerThreshHSV = np.array([self.s.dict['lowerH'], self.s.dict['lowerS'], self.s.dict['lowerV']])
        higherThreshHSV = np.array([self.s.dict['higherH'], self.s.dict['higherS'], self.s.dict['higherV']])
        
        maskHSV = cv2.inRange(hsv, lowerThreshHSV, higherThreshHSV)
        resHSV = cv2.bitwise_and(frame, frame, mask=maskHSV)
        
        lowerThreshBGR = np.array([self.s.dict['lowerB'], self.s.dict['lowerG'], self.s.dict['lowerR']])
        higherThreshBGR = np.array([self.s.dict['higherB'], self.s.dict['higherG'], self.s.dict['higherR']])
        
        maskBGR = cv2.inRange(resHSV, lowerThreshBGR, higherThreshBGR)
        kernel = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(maskBGR, cv2.MORPH_OPEN, kernel)
        median = cv2.medianBlur(opening, 5)

        im2, contours, hierarchy = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        indexB = 0
        indexSB = 0
        for i in range(len(contours)):
            if cv2.matchShapes(self.bitmap, i, 1, 0.0) >= cv2.matchShapes(self.bitmap, indexB, 1, 0.0):
                indexSB = indexB
                indexB = i
        
##        if contours == []:
##            return False, None, None, None
##        
##        indexLA = 0
##        indexSLA = 0
##        for i in range(len(contours)):
##            if cv2.contourArea(contours[i]) >= cv2.contourArea(contours[indexLA]):
##                indexSLA = indexLA
##                indexLA = i
        rects = [cv2.boundingRect(contours[indexSB]), cv2.boundingRect(contours[indexB])]
        pw = math.ceil(rects[0][0] + rects[1][0] + rects[1][2]) / 2
        ph = rects[1][1]
        return True, rects, int(ph), int(pw)

if __name__ == '__main__':

    nwt = nwtConnection('roborio-4546-frc.local', '/SmartDashboard/', '/CameraPublisher/USB Camera 0/')
    s = Settings('./hsv_settings.txt')
    ss = Settings('./settings.txt')
    ht = HookTracker(s, './hook_bitmap.png')

    nwt.find_stream()

    cap = cv2.VideoCapture(nwt.streamURL)

    while True:
        
        ret, frame = cap.read()

        if ret:

            tracking, rects, ph, pw = ht.track(frame)
            if tracking:
                for i in rects:
                    x, y, w, h = i
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                if pw != None:
                    cv2.circle(frame, (pw, ph), 5, (255,0,0), 3)
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

        
        
        
        
