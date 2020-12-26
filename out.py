import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk
import time


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # open video source (by default this will try to open the computer webcam)
        self.vid = CameraCapture()
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.create_widgets()
        self.delay = 15
        self.update()

        self.window.mainloop()

    def create_widgets(self):
        # Create a canvas that can fit the above video source size
        self.capture_canvas = tk.Canvas(
            self.window, width=self.vid.width, height=self.vid.height)
        self.capture_canvas.pack(expand=True, fill=tk.BOTH)

        # Button that lets the user take a snapshot
        self.btn_snapshot = tk.Button(
            self.window, text="Snapshot", width=50)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.cv_image = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))
            self.capture_canvas.create_image(
                0, 0, image=self.cv_image, anchor=tk.NW)

        self.window.after(self.delay, self.update)


class CameraCapture:
    def __init__(self):
        # Open the video source
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source")

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the Application object
App(tk.Tk(), "Tkinter and OpenCV")
