import math, numpy as np

def hat(w):
    wx,wy,wz=map(float,w)
    return np.array([[0,-wz,wy],[wz,0,-wx],[-wy,wx,0]],float)

def exp_so3(w):
    w=np.asarray(w,float).reshape(3); t=np.linalg.norm(w); K=hat(w)
    if t<1e-12: return np.eye(3)+K
    return np.eye(3)+math.sin(t)/t*K+(1-math.cos(t))/t**2*(K@K)

def euler_xyz_to_rotmat(a,b,g):
    ca,cb,cg=math.cos(a),math.cos(b),math.cos(g)
    sa,sb,sg=math.sin(a),math.sin(b),math.sin(g)
    Rx=np.array([[1,0,0],[0,ca,-sa],[0,sa,ca]],float)
    Ry=np.array([[cb,0,sb],[0,1,0],[-sb,0,cb]],float)
    Rz=np.array([[cg,-sg,0],[sg,cg,0],[0,0,1]],float)
    return Rz@Ry@Rx

def rotmat_to_euler_xyz(R):
    R=np.asarray(R,float); b=math.asin(np.clip(-R[2,0],-1,1))
    return math.atan2(R[2,1],R[2,2]),b,math.atan2(R[1,0],R[0,0])

def lie_state(alpha,beta,zoom):
    return np.array([alpha,beta,math.log(max(float(zoom),1e-6))],float)

def lie_distance(v1,v2): return float(np.linalg.norm(np.asarray(v1)-np.asarray(v2)))
def lie_bracket(v1,v2): return np.cross(np.asarray(v1,float),np.asarray(v2,float))
