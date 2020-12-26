data = """ 1 import tkinter
 2 import cv2
 3 import PIL.Image, PIL.ImageTk
 4 import time
 5 
 6 class App:
 7     def __init__(self, window, window_title, video_source=0):
 8         self.window = window
 9         self.window.title(window_title)
10         self.video_source = video_source
11 
12         # open video source (by default this will try to open the computer webcam)
13         self.vid = MyVideoCapture(self.video_source)
14 
15         # Create a canvas that can fit the above video source size
16         self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
17         self.canvas.pack()
18 
19         # Button that lets the user take a snapshot
20         self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
21         self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
22 
23         # After it is called once, the update method will be automatically called every delay milliseconds
24         self.delay = 15
25         self.update()
26 
27         self.window.mainloop()
28 
29     def snapshot(self):
30         # Get a frame from the video source
31         ret, frame = self.vid.get_frame()
32 
33         if ret:
34             cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
35 
36     def update(self):
37         # Get a frame from the video source
38         ret, frame = self.vid.get_frame()
39 
40         if ret:
41             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
42             self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
43 
44         self.window.after(self.delay, self.update)
45 
46 
47 class MyVideoCapture:
48     def __init__(self, video_source=0):
49         # Open the video source
50         self.vid = cv2.VideoCapture(video_source)
51         if not self.vid.isOpened():
52             raise ValueError("Unable to open video source", video_source)
53 
54         # Get video source width and height
55         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
56         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
57 
58     def get_frame(self):
59         if self.vid.isOpened():
60             ret, frame = self.vid.read()
61             if ret:
62                 # Return a boolean success flag and the current frame converted to BGR
63                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
64             else:
65                 return (ret, None)
66         else:
67             return (ret, None)
68 
69     # Release the video source when the object is destroyed
70     def __del__(self):
71         if self.vid.isOpened():
72             self.vid.release()
73 
74 # Create a window and pass it to the Application object
75 App(tkinter.Tk(), "Tkinter and OpenCV")"""

f = open("out.py", "w")
for item in data.split("\n"):
    f.write(item[3:]+"\n")
f.close()