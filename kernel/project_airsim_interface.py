from projectairsim import ProjectAirSimClient, World, Drone
from projectairsim.utils import projectairsim_log 

import asyncio, time, math
import cv2 # good website to study the lib: https://opencv.org/read-display-and-write-an-image-using-opencv/ 
import subprocess
import numpy as np

from kernel.interface.server import InterceptorServer
from kernel.other_drones.target_drone_trajectory import TargetDroneTrajectory
from companion_computer.Perception.camera_detection.camera_output import CameraOutput


class ProjectAirsimKernel:
    def __init__(self):
        #initalize the connection with the unreal 
        self.PAC = ProjectAirSimClient()
        self.PAC.connect() 

        self.world = World(self.PAC, "scene_cesium_drone.jsonc", delay_after_load_sec=2)

        self.interceptor = Drone(self.PAC, self.world, "interceptor")
        self.interceptor_maneuver = InterceptorServer()

        self.target = Drone(self.PAC, self.world, "target")
        self.target_maneuver = TargetDroneTrajectory()

        self.ffmpeg = None



    def start_stream(self, width, height, fps):
        cmd = [
            r"E:\tanya_download_stuffs\ffmpeg-8.1-essentials_build\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe",
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


    def stop_stream(self):
        if self.ffmpeg is not None:
            if self.ffmpeg.stdin:
                self.ffmpeg.stdin.close()
            self.ffmpeg.terminate()
            self.ffmpeg.wait()
            self.ffmpeg = None

    def show_camera_result(self, topic, msg):
        """ This callback function can have 3 diferent ways of manipultating the camera output.
         1) Using rerun library to generate camera frames in real time
          2) Using CV2 (OpenCV) library to show the pop-up window for all the frames
           3) Process it as a ROS image and send it to a ROS topic 
        
        Uncomment one to be able to publish those images"""
        if msg is None: return

        h = msg["height"]
        w = msg["width"]
        np_img = np.frombuffer(msg["data"], dtype=np.uint8) #take raw bytes and view them as NumPy 1D array

        # Display the image in a pop-up window
        # 
        #np_img = np_img.reshape((h, w, 3)) # makes its a 3D array (height, width, channels = BRG (so 3!))
        #cv2.imshow('Intercepto View', np_img)
        #cv2.waitKey(1) # wait 1 ms to assess if key pressed, otherwise continue 

        if self.ffmpeg is not None:
            self.ffmpeg.stdin.write(np_img.tobytes())

    def manager(self): 

        # general knowledge of current topics to play around with
        extractable_topics = self.PAC.get_topic_info()
        print(extractable_topics)

        # TODO: Add noise model to the config file for the camera sensor: https://iamaisim.github.io/ProjectAirSim/sensors/camera_post_processing_with_nn.html 

        #enable continuse image capturing 
        self.start_stream(1456, 1088, 20) 
        self.PAC.subscribe('/Sim/SceneBasicDrone/robots/interceptor/sensors/InterceptionCamera/scene_camera', self.show_camera_result)
        time.sleep(5)
        projectairsim_log().info("Drones about to take off in 2 sec")
        time.sleep(2)


        try: 
            while True: 
                # move interceptor in the world
                interceptor_pose = self.interceptor_maneuver._states()
                self.interceptor.set_pose(interceptor_pose)

                # move target in the world
                target_pose = self.target_maneuver.yz_circle_trajectory()
                self.target.set_pose(target_pose)


        except KeyboardInterrupt:
            print ("Stopped receiving data to drive the interceptor.")
            InterceptorServer().writeListToCsv()
            #cv2.destroyAllWindows()
            self.stop_stream()
            self.PAC.disconnect()   # this also lets u stop the process from terminal otherwise it stucks looking for next command


if __name__ == "__main__":
    interceptor_interface = ProjectAirsimKernel()
    interceptor_interface.manager()