import json,time
from pathlib import Path
import cv2,numpy as np
try: from ultralytics import YOLO
except Exception: YOLO=None
from .yolo26_lie import YOLO26LieFeatureAdapter

class SteelDetector:
    def __init__(self,model_path=None,conf=.35):
        self.conf=conf; self.model=None; self.class_names=["Steel coil","Information","QR code"]
        self.adapter=YOLO26LieFeatureAdapter()
        self.model_path=Path(model_path or Path(__file__).resolve().parents[2]/"models/yolo26n.pt")
        if YOLO and self.model_path.exists():
            try:self.model=YOLO(str(self.model_path))
            except Exception:pass
        self.qr=cv2.QRCodeDetector()
    def _fallback(self,frame):
        g=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY); e=cv2.Canny(cv2.GaussianBlur(g,(5,5),0),60,150)
        cs,_=cv2.findContours(e,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); out=[]
        for c in sorted(cs,key=cv2.contourArea,reverse=True)[:8]:
            x,y,w,h=cv2.boundingRect(c)
            if w*h<1500:continue
            out.append({"label":"Steel coil","confidence":.65,"bbox":[x,y,x+w,y+h]})
        return out
    def detect(self,frame,alpha=0.,beta=0.,zoom=1.):
        t=time.time(); ds=[]
        if self.model:
            try:
                for r in self.model(frame,conf=self.conf,verbose=False):
                    if r.boxes is None:continue
                    for row in r.boxes.data.cpu().numpy():
                        x1,y1,x2,y2,cf,cl=row[:6]; cl=int(cl)
                        ds.append({"label":self.class_names[cl] if cl<len(self.class_names) else str(cl),
                                   "confidence":float(cf),"bbox":[float(x1),float(y1),float(x2),float(y2)]})
            except Exception: ds=[]
        if not ds:ds=self._fallback(frame)
        qr=""
        try:
            data,_,_=self.qr.detectAndDecode(frame); qr=data or ""
        except Exception:pass
        h,w=frame.shape[:2]
        for d in ds:
            x1,y1,x2,y2=d["bbox"]; cx=((x1+x2)/2)/w; cy=((y1+y2)/2)/h
            d["warehouse_position"]=f"A区-{int(cx*10)+1:02d}-{int(cy*10)+1:02d}"
            d["coil_id"]="G2025001" if d["label"]=="Steel coil" else ""; d["qr_text"]=qr or "未识别"
        z=self.adapter.enrich(ds,alpha,beta,zoom); z["latency_ms"]=(time.time()-t)*1000
        return z
    def draw(self,frame,result):
        out=frame.copy()
        for d in result.get("detections",[]):
            x1,y1,x2,y2=map(int,d["bbox"]); cv2.rectangle(out,(x1,y1),(x2,y2),(0,220,120),2)
            cv2.putText(out,f'{d["label"]} {d["confidence"]:.2f}',(x1,max(20,y1-8)),
                        cv2.FONT_HERSHEY_SIMPLEX,.55,(0,220,120),2)
        return out

def append_jsonl(path,result,meta):
    with open(path,"a",encoding="utf-8") as f:f.write(json.dumps({"timestamp":time.time(),"meta":meta,"result":result},ensure_ascii=False)+"\n")
