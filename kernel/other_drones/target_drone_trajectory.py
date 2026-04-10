import math

class TargetDroneTrajectory:
    """This class is about different mission plan (trajectory models)
    (currently the dynamics are not driven by forces and moments)"""
    def __init__(self):

        self.t =  0 # s
        self.omega = 0.02 #rad/s
        
        self.yaw_angle = 0 #degree

        self.x = 60
        self.y = 0
        self.z = -5                                  
        self.qw = 1
        self.qx = 0
        self.qy = 0
        self.qz = 0

    def lawnmower_trajectory(self):
        """ a growing lawnmower motion (flight pattern for drones)"""

        # constant forward motion
        v_x = 0.01
        self.x = self.x + (v_x * self.t)

        # smooth sinosodal motion
        omega = 0.02
        self.y = self.y + (2*math.sin(omega * self.t))
        v_y = 2*omega * math.cos(omega * self.t)

        # for the quaternion, assume the roll and pitch both zeros 
        yaw_angle = math.atan2(v_y, v_x)
        # (focus on yaw only - drone face the dirrection of movmenet)
        self.qw = math.cos(yaw_angle /2)
        self.qz = math.sin(yaw_angle /2)


        pose = { "frame_id": "DEFAULT_FRAME", 
                "translation": { "x": self.x, "y": self.y, "z": self.z }, 
                "rotation": { "w": self.qw, "x": self.qx, "y": self.qy, "z": self.qz } 
                }
        
        self.t += 0.01
        
        return pose
    

    def vertical_occilation_trajectory(self):
        omega = 0.3
        self.z = (-3 + 2 * math.sin(omega * self.t))

        pose = { "frame_id": "DEFAULT_FRAME", 
                "translation": { "x": self.x, "y": self.y, "z": self.z }, 
                "rotation": { "w": self.qw, "x": self.qx, "y": self.qy, "z": self.qz } 
                }
        

        self.t +=0.1 

        return pose


    def yz_circle_trajectory(self):
        r = 1.0
        omega = -20

        self.y = 5* (r * math.cos(omega * self.t))
        self.z = self.z - (r * math.sin(omega * self.t))

        if self.z > 0: 
            self.z = 0 # since the frame conversion in terms of NED

        pose = { "frame_id": "DEFAULT_FRAME", 
                "translation": { "x": self.x, "y": self.y, "z": self.z }, 
                "rotation": { "w": self.qw, "x": self.qx, "y": self.qy, "z": self.qz } 
                }
        
        self.t += 0.01

        return pose


    def hold_position(self):

        pose = { "frame_id": "WORLD", 
                "translation": { "x": self.x, "y": self.y, "z": self.z }, 
                "rotation": { "w": self.qw, "x": self.qx, "y": self.qy, "z": self.qz } 
                }
        
        return pose
    

if __name__ == "__main__":
    target_motion = TargetDroneTrajectory()
    while True: 
        tar_pose = target_motion.yz_circle_trajectory()
        print (tar_pose)