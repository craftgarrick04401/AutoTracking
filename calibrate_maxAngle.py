import cv2, math


cap = cv2.VideoCapture(1)

while True:

    

hdist = float(input("hdist"))
cameraHeight = float(input("cameraHeight"))
targetHeight = float(input("targetHeight"))
pMax = int(input("pMax"))


hdist = 143 + 3/16
camHeight = 29 + 3/16
targetHeight = 2
pMax = 480
pH = (376+393)/2
vFOV = 38.243

maxAngle = math.degrees(math.atan(hdist/camHeight)) + pH/pMax*vFOV
print(maxAngle)
print(pH/pMax*vFOV)
