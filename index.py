import cv2

video_object = cv2.VideoCapture(0)
while (True):
    ret, frame = video_object.read()
    cv2.imshow("Frames", frame)
    key = cv2.waitKey(1)
    if key == "q":
        break