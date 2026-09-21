import math,numpy as np
from .lie import exp_so3,rotmat_to_euler_xyz,lie_state

class CameraModel:
    SENSOR_WIDTH=0.00368
    def __init__(self,img_w=640,img_h=480):
        self.img_w,self.img_h=img_w,img_h; self.R_cam=np.eye(3); self.t_cam=np.zeros(3)
        self.magnification=1.; self.K=np.array([[400.,0,img_w/2],[0,400.,img_h/2],[0,0,1.]])
    def update_position(self,x,y,z): self.t_cam=np.array([x,y,z],float)
    def update_orientation_increment(self,da,db,dg): self.R_cam=self.R_cam@exp_so3([da,db,dg])
    def update_magnification(self,s):
        self.magnification=max(float(s),.1); f=400*self.magnification
        self.K=np.array([[f,0,self.img_w/2],[0,f,self.img_h/2],[0,0,1.]])
        return self.fov_deg()
    def fov_deg(self):
        f=max(float(self.K[0,0])*self.SENSOR_WIDTH/self.img_w,1e-12)
        return 2*math.degrees(math.atan2(self.SENSOR_WIDTH,2*f))
    def meta(self):
        a,b,g=rotmat_to_euler_xyz(self.R_cam)
        return {"R":self.R_cam.tolist(),"t_vec":self.t_cam.tolist(),"K":self.K.tolist(),
                "euler_xyz":[a,b,g],"s":self.magnification,"V":lie_state(a,b,self.magnification).tolist()}
