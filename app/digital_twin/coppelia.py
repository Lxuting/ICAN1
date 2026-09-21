import math
try: import sim
except Exception: sim=None
class CoppeliaSimCameraController:
    def __init__(self):self.client_id=-1;self.camera_handle=None;self.dummy_handle=None
    def connect(self):
        if sim is None:return False
        sim.simxFinish(-1); self.client_id=sim.simxStart("127.0.0.1",19999,True,True,5000,5)
        if self.client_id==-1:return False
        e1,self.camera_handle=sim.simxGetObjectHandle(self.client_id,"Vision_sensor",sim.simx_opmode_blocking)
        e2,self.dummy_handle=sim.simxGetObjectHandle(self.client_id,"Dummy",sim.simx_opmode_blocking)
        return e1==sim.simx_return_ok and e2==sim.simx_return_ok
    def update_position(self,x,y,z):
        if sim is None or self.client_id==-1:return False
        return sim.simxSetObjectPosition(self.client_id,self.camera_handle,-1,[x,y,z],sim.simx_opmode_oneshot)==sim.simx_return_ok
    def update_fov(self,fov):
        if sim is None or self.client_id==-1:return False
        e=sim.simxSetObjectFloatParameter(self.client_id,self.camera_handle,sim.sim_visionfloatparam_perspective_angle,math.radians(fov),sim.simx_opmode_blocking)
        return e==sim.simx_return_ok
    def close(self):
        if sim is not None and self.client_id!=-1:sim.simxFinish(self.client_id);self.client_id=-1
