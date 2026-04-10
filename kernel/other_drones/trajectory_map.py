import matplotlib.pyplot as plt
import numpy as np
import math
from kernel.other_drones.target_drone_trajectory import TargetDroneTrajectory
"""


this class is outdated!!! fix before using

"""
class PlotTrajectory:
    def __init__(self):

        self.listx = []
        self.listy = []
        self.listz = []
        self.listu = []
        self.listv = []
        self.listw = []

        self.path_model = TargetDroneTrajectory()


    def _trajectory(self):
        """ this function is suppose to define a list of trajectory points """

        while self.path_model.t < 1000: 
            self.path_model.lawnmower_trajectory()
            self.listx.append(self.path_model.x)
            self.listy.append(self.path_model.y)
            self.listz.append(self.path_model.z)

    def plot (self):
        self._trajectory()

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
        ax.set_title("3D Path with Direction")

        limit = 10   # change this value as needed
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)

        ax.set_box_aspect([1, 1, 1])   # makes x,y,z scale look equal

        plt.show()


if __name__ == "__main__":
    PlotTrajectory().plot()