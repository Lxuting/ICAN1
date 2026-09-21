from dataclasses import dataclass
import numpy as np
from .lie import hat,exp_so3

@dataclass
class LMConfig:
    max_iter:int=15; lambda0:float=1e-2; eps:float=1e-9

def project_points(K,R,t,X):
    Xc=(R@X.T+np.asarray(t).reshape(3,1)).T; z=np.maximum(Xc[:,2],1e-9)
    xy=np.vstack([Xc[:,0]/z,Xc[:,1]/z,np.ones(len(X))])
    return (K@xy).T[:,:2]

def lm_refine_rotation_focal(K,R,t,Xw,uv,cfg=LMConfig()):
    Xw,uv=np.asarray(Xw,float),np.asarray(uv,float); f=float(K[0,0]); cx,cy=K[0,2],K[1,2]; lam=cfg.lambda0
    for _ in range(cfg.max_iter):
        Ku=np.array([[f,0,cx],[0,f,cy],[0,0,1.]],float); r=(project_points(Ku,R,t,Xw)-uv).reshape(-1); J=[]
        for X in Xw:
            Xc=R@X+np.asarray(t); z=Xc[2]
            if z<=1e-9: continue
            x,y=Xc[0]/z,Xc[1]/z; d=np.array([[1/z,0,-Xc[0]/z**2],[0,1/z,-Xc[1]/z**2]])
            Jw=np.array([[f,0],[0,f]])@d@(-hat(R@X)); J.append(np.hstack([Jw,np.array([[x],[y]])]))
        if not J: break
        J=np.vstack(J)
        try: delta=-np.linalg.solve(J.T@J+lam*np.eye(4),J.T@r)
        except np.linalg.LinAlgError: break
        Rn=R@exp_so3(delta[:3]); fn=max(50.,f+float(delta[3]))
        Kn=np.array([[fn,0,cx],[0,fn,cy],[0,0,1.]])
        if np.linalg.norm(project_points(Kn,Rn,t,Xw)-uv)<np.linalg.norm(r.reshape(-1,2)):
            R,f=Rn,fn; lam=max(1e-6,lam/2)
        else: lam=min(1e3,lam*2)
        if np.linalg.norm(delta)<cfg.eps: break
    return R,np.array([[f,0,cx],[0,f,cy],[0,0,1.]])
