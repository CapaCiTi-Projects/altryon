import cv2
import os
import PIL.Image
import PIL.ImageTk
import tkinter as tk

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


class CameraCapture:
    def __init__(self):
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", 0)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        cv2.destroyAllWindows()
        if self.vid.isOpened():
            self.vid.release()


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.delay = 15
        self.capture = CameraCapture()

        self.prev_motion_frame = None
        self.face_detected = False
        self.motion_detected = False
        self.should_detect_motion = False

        self.create_widgets()
        self.update()

        self.mainloop()

    def create_widgets(self):
        self.read_canvas = tk.Canvas(
            self, width=self.capture.width, height=self.capture.height, bg="#ffffff")
        self.read_canvas.pack()

        self.motion_label = tk.Label(self, text="Not Detecting Motion")
        self.motion_label.pack()

        self.refresh_button = tk.Button(
            self, text="Refresh")
        self.refresh_button.pack()

    def load_cv_image(self):
        ret, frame = self.capture.get_frame()
        if ret:
            result, self.face_detected = face_detect(frame)
            if self.face_detected:
                self.tk_image = result
                self.should_detect_motion = True
            else:
                self.should_detect_motion = False

            if self.prev_motion_frame is None:
                self.prev_motion_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.should_detect_motion:
                self.motion_detected, prev_motion_frame = motion_detect(
                    frame, self.prev_motion_frame)
                if self.motion_detected:
                    self.prev_motion_frame = prev_motion_frame
                    self.motion_label["text"] = "Movement Detected."
                else:
                    self.motion_label["text"] = "No movement detected."
            else:
                self.motion_label["text"] = "Not looking for movement."

            self.tk_image = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))
            self.read_canvas.create_image(
                0, 0, image=self.tk_image, anchor=tk.NW)

    def update(self):
        self.load_cv_image()
        self.after(self.delay, self.update)


def face_detect(photo):
    grayscale = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(grayscale)
    detect_image = None

    for x, y, w, h in faces:
        detect_image = cv2.rectangle(
            photo, (x, y), (x+w, y+h), (0, 255, 0), 3)

    return (detect_image, True) if (detect_image is not None) and detect_image.any() else (photo, False)


def motion_detect(photo, last=None):
    grayscale = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    grayscale = cv2.GaussianBlur(grayscale, (21, 21), 0)

    if last is None:
        return False, last
    else:
        delta_frame = cv2.absdiff(last, grayscale)
        thresh_delta = cv2.threshold(
            delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)

        cnts, _ = cv2.findContours(
            thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < 1000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
        return True, grayscale
    return False, last


app = Application()
