
import socket, struct, time, csv, os

# log 
desktop = os.path.expanduser("~/Desktop") 
LOG_PATH = os.path.join(desktop, "timestamp_visualizer_log.csv")

class InterceptorServer:
    def __init__(self):
        self.win_ip = "0.0.0.0"
        self.port_state = 55556
        self.socket_state = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_state.bind((self.win_ip,self.port_state))
        
        # positional, rotational and timestamp data of every state
        self.x = 0
        self.y = 0
        self.z = 0 
        self.qw = 1
        self.qx = 0
        self.qy = 0
        self.qz = 0
        self.operating_systems_dt = []
    
    def writeListToCsv(self):
        dataList = self.operating_systems_dt
        header = "Visualizer steptime between 2 PCs"
        fileDir = LOG_PATH
        with open(fileDir, 'w', newline='') as file: 
            writer = csv.writer(file) 
            writer.writerow([header]) 
            for val in dataList: 
                writer.writerow([val]) 
            file.close 
        print(f"Successfully wrote data to {fileDir}")

    def _states (self):
       
        buf_state, addr_state = self.socket_state.recvfrom(8024)    # UDP receive
        state_data = struct.unpack("<3f4fQ", buf_state)
                
        # convert to expected coordinate frame and unit expected by interface (NED, SI)
        self.x = state_data[0] 
        self.y = state_data[1] 
        self.z = state_data[2] 

        self.qw = state_data[3] 
        self.qx = state_data[4]
        self.qy = state_data[5]
        self.qz = state_data[6] 

        # timestamp analysis
        t_now = time.perf_counter_ns()
        self.operating_systems_dt.append(t_now - state_data[7])

        # the struct is based on the Transform class from ProjectAirsim > Drone > Pose 
        pose = { "frame_id": "DEFAULT_FRAME", 
                "translation": { "x": self.x, "y": self.y, "z": self.z }, 
                "rotation": { "w": self.qw, "x": self.qx, "y": self.qy, "z": self.qz } 
                }

        return pose