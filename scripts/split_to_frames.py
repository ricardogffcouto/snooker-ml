import cv2
import os
count=1

vid = 'video.mp4'
vidcap = cv2.VideoCapture(vid)
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("image_" + str(count) + ".jpg", image)
    return hasFrames
sec = 0
frameRate = 25

success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)