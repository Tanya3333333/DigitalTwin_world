from projectairsim import ProjectAirSimClient, World, Drone 
import asyncio
import cv2 # good website to study the lib: https://opencv.org/read-display-and-write-an-image-using-opencv/ 
import numpy as np
from kernel.interface.server import InterceptorServer
from kernel.other_drones.target_drone_dynamics import TargetDrone


class ProjectAirsimKernel:
    def __init__(self):
        #initalize the connection with the unreal 
        self.PAC = ProjectAirSimClient()
        self.PAC.connect() 
        self.world = World(self.PAC, "scene_cesium_drone.jsonc", delay_after_load_sec=2)
        self.interceptor = Drone(self.PAC, self.world, "interceptor")
        self.target = Drone(self.PAC, self.world, "target")

    def show_camera_output(self, msg):
        
        print("frame received")
        print(type(msg))
        print(msg)

        #np_img = cv2.imread("", cv2.IMREAD_UNCHANGED) # read the data as it is and convert to NumPy array
        #if np_img is None: return
        #else:
            # Display the image in a pop-up window 
            #cv2.imshow('Intercepto View', np_img)

            #Wait indefinitely for a key press (0 means wait forever -> keeps window open)
            #cv2.waitKey(0)


    def manager(self): 
        extractable_topics = self.PAC.get_topic_info()
        print(extractable_topics)


        #enable continuse image capturing 
        # TODO: Add noise model to the config file for the camera sensor: https://iamaisim.github.io/ProjectAirSim/sensors/camera_post_processing_with_nn.html 
        self.PAC.subscribe('/Sim/SceneBasicDrone/robots/interceptor/sensors/InterceptionCamera/scene_camera', self.show_camera_output)

        try: 
            while True: 
                pass

                # move interceptor in the world
                #interceptor_pose = InterceptorServer()._states()
                #self.interceptor.set_pose(interceptor_pose)

                # move target in the world
                #target_pose = TargetDrone().lawnmower_trajectory()
                #self.target.set_pose(target_pose)

                
        except KeyboardInterrupt:
            print ("Stopped receiving data to drive the interceptor.")
            InterceptorServer().writeListToCsv()
            cv2.destroyAllWindows()
            self.PAC.disconnect()   # this also lets u stop the process from terminal otherwise it stucks looking for next command


if __name__ == "__main__":
    interceptor_interface = ProjectAirsimKernel()
    interceptor_interface.manager()