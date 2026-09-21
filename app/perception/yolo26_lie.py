import numpy as np
from ..localization.lie import lie_state,lie_bracket
from .granular_ball import aggregate_granular_balls
from .hypergraph import build_adaptive_hyperedges

class YOLO26LieFeatureAdapter:
    def enrich(self,detections,alpha=0.,beta=0.,zoom=1.):
        V=lie_state(alpha,beta,zoom)
        if not detections:return {"detections":[],"V":V.tolist(),"granular_balls":[],"hyperedges":[]}
        feats=[[d["bbox"][0],d["bbox"][1],d["bbox"][2]-d["bbox"][0],d["bbox"][3]-d["bbox"][1],d["confidence"]] for d in detections]
        balls=aggregate_granular_balls(feats,[V]*len(feats),[zoom]*len(feats))
        edges=build_adaptive_hyperedges(balls)
        for d in detections:
            d["lie_state"]=V.tolist(); d["hyperedge_count"]=len(edges)
            d["lie_bracket_norm"]=float(np.linalg.norm(lie_bracket(V,V)))
        return {"detections":detections,"V":V.tolist(),"granular_balls":balls,"hyperedges":edges}
