import numpy as np
def aggregate_granular_balls(features,lie_vectors,zooms,split_std=.8,merge_lie=.35,merge_zoom=1.5):
    X,V,S=np.asarray(features,float),np.asarray(lie_vectors,float),np.asarray(zooms,float)
    if len(X)==0:return []
    idx=np.arange(len(X)); groups=[idx]
    if np.std(S)>split_std:
        m=np.median(S); groups=[idx[S<=m],idx[S>m]]
    out=[]
    for g in groups:
        if len(g)==0: continue
        out.append({"indices":g.tolist(),"center":X[g].mean(0).tolist(),
                    "lie_center":V[g].mean(0).tolist(),"zoom_mean":float(S[g].mean())})
    return out
