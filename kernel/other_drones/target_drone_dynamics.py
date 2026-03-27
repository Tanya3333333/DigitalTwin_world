import math

class TargetDrone:
    def __init__(self):

        self.t =  0 # s
        self.omega = 0.2 #rad/s
    
        self.v_x = 0 #forward speed m/s
        self.v_y = 0 #m/s
        
        self.yaw_angle = 0 #degree

        self.x = 0
        self.y = 0
        self.z = 0                                  
        self.qw = 1
        self.qx = 0
        self.qy = 0
        self.qz = 0

    def lawnmower_trajectory(self):
        """ this function is suppose to define a trajectory path model (flight pattern for drones)"""

        # constant forward motion
        self.v_x = 0.1
        self.x = self.v_x * self.t

        # smooth sinosodal motion
        self.y = 2*math.sin(self.omega * self.t)
        self.v_y = 2*self.omega * math.cos(self.omega * self.t)
        
        self.z = 0

        # for the quaternion, assume the roll and pitch both zeros 
        self.yaw_angle = math.atan2(self.v_y, self.v_x)
        # (focus on yaw only - drone face the dirrection of movmenet)
        self.qw = math.cos(self.yaw_angle /2)
        self.qx = 0
        self.qy = 0
        self.qz = math.sin(self.yaw_angle /2)

        pose = { "frame_id": "DEFAULT_FRAME", 
                "translation": { "x": self.x, "y": self.y, "z": self.z }, 
                "rotation": { "w": self.qw, "x": self.qx, "y": self.qy, "z": self.qz } 
                }
        
        self.t += 0.01
        
        return pose
            

