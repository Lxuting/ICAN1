import numpy as np
def build_adaptive_hyperedges(balls,image_bandwidth=1.,lie_bandwidth=.8,zoom_bandwidth=.8):
    edges=[]
    for i,b in enumerate(balls):
        mem=[i]
        for j,c in enumerate(balls):
            if i==j:continue
            di=np.linalg.norm(np.asarray(b["center"])-np.asarray(c["center"]))
            dl=np.linalg.norm(np.asarray(b["lie_center"])-np.asarray(c["lie_center"]))
            dz=abs(b["zoom_mean"]-c["zoom_mean"])
            w=np.exp(-di**2/(2*image_bandwidth**2)-dl**2/(2*lie_bandwidth**2)-dz**2/(2*zoom_bandwidth**2))
            if w>.35: mem.append(j)
        edges.append({"members":mem,"weight":1.})
    return edges
