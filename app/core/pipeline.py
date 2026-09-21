from pathlib import Path
import cv2
from ..perception.detector import SteelDetector,append_jsonl
class SteelPipeline:
    def __init__(self): self.detector=SteelDetector(); self.log_path=Path("run_frames.jsonl")
    def process(self,frame,meta):
        r=self.detector.detect(frame,meta.get("alpha",0),meta.get("beta",0),meta.get("zoom",1))
        v=self.detector.draw(frame,r); append_jsonl(self.log_path,r,meta); return v,r
