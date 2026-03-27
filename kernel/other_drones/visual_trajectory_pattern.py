import matplotlib.pyplot as plt
import numpy as np
import math

class PlotTrajectory:
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


        self.u = 0
        self.v = 0 
        self.w = 0

        self.listx = []
        self.listy = []
        self.listz = []
        self.listu = []
        self.listv = []
        self.listw = []

    def lawnmower_trajectory(self):
        """ this function is suppose to define a trajectory model (flight path for drones)"""

        # constant forward motion
        self.v_x = 0.1
        self.x = self.v_x * self.t

        # smooth sinosodal motion
        self.y = 2*math.sin(self.omega * self.t)
        self.v_y = 2*self.omega * math.cos(self.omega * self.t)
        
        self.z = 5

        # for the quaternion, assume the roll and pitch both zeros 
        self.yaw_angle = math.atan2(self.v_y, self.v_x)
        # (focus on yaw only - drone face the dirrection of movmenet)
        self.qw = math.cos(self.yaw_angle /2)
        self.qx = 0
        self.qy = 0
        self.qz = math.sin(self.yaw_angle /2)

        # arrow (dirrection) of xyz in order
        u = math.cos(self.yaw_angle)
        v = math.sin(self.yaw_angle)
        w = 0

    def plot (self):

        while self.t < 500: 
            self.lawnmower_trajectory()
            self.listx.append(self.x)
            self.listy.append(self.y)
            self.listz.append(self.z)

            self.listu.append(self.u)
            self.listv.append(self.v)
            self.listw.append(self.w)
            self.t += 0.01



        # 3d figure setup
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.plot(self.listx, self.listy, self.listz)

        step = 10
        ax.quiver(
            self.listx[::step], self.listy[::step], self.listz[::step],
            self.listu[::step], self.listv[::step], self.listw[::step],
            length=0.4, normalize=True
        )

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_title("3D Path with Yaw Direction")

        plt.show()


if __name__ == "__main__":
    PlotTrajectory().plot()