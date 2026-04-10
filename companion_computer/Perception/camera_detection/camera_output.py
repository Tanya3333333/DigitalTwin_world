import numpy as np

import cv2
import subprocess # this library lets python run external programs such as ffmpeg

class CameraOutput:
    """
    show camera sensor output in different styles for the users and robotic applications!

    """
    def __init__(self):
        self.ffmpeg = None

    
    def show_camera_result_using_cv2(self, topic, msg):
        """ This callback function can have 3 diferent ways of manipultating the camera output.
         1) Using rerun library to generate camera frames in real time
          2) Using CV2 (OpenCV) library to show the pop-up window for all the frames
        """
        if msg is None: return

        h = msg["height"]
        w = msg["width"]
        np_img = np.frombuffer(msg["data"], dtype=np.uint8) #take raw bytes and view them as NumPy 1D array
        np_img = np_img.reshape((h, w, 3)) # makes its a 3D array (height, width, channels = BRG (so 3!))

        # Display the image in a pop-up window
        cv2.imshow('Intercepto View', np_img)
        cv2.waitKey(1) # wait 1 ms to assess if key pressed, otherwise continue


    
    def start_stream(self, width, height, fps):
        cmd = [
            r"E:\tanya_download_stuffs\ffmpeg-8.1-essentials_build\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe",
            "-re",
            "-f", "rawvideo",
            "-pix_fmt", "bgr24",
            "-s", f"{width}x{height}",
            "-r", str(fps),
            "-i", "-",
            "-an",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-pix_fmt", "yuv420p",
            "-f", "rtsp",
            "-rtsp_transport", "tcp",
            "rtsp://127.0.0.1:8554/interceptor"
        ]

        self.ffmpeg = subprocess.Popen(cmd, stdin=subprocess.PIPE) 


    def show_camera_result_using_mediaMTX (self, msg):

        """ In order to use this function, make sure to install the mediaMTX and ffmpeg executable files to be able to see the camera outputs in an external web browser. 
        1) install the mediaMTX from the asset list according to the current OS in use: https://github.com/bluenviron/mediamtx/releases 
        2) then in your OS terminal, go to the path of your download and run the mediamtx.exe file
        3) install the ffmpeg: https://ffmpeg.org/download.html and make sure its added to PATH (System Environment Variables)
        4) 

        """
        if msg is None: return

        h = msg["height"]
        w = msg["width"]
        np_img = np.frombuffer(msg["data"], dtype=np.uint8) #take raw bytes and view them as NumPy 1D array

        if self.ffmpeg is not None:
            self.ffmpeg.stdin.write(np_img.tobytes())


    def publish_camera_result_to_ROS(self):
        pass