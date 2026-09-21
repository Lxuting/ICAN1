def on_segment(p,q,r):
    return q[0]<=max(p[0],r[0]) and q[0]>=min(p[0],r[0]) and q[1]<=max(p[1],r[1]) and q[1]>=min(p[1],r[1])
def orientation(p,q,r):
    v=(q[1]-p[1])*(r[0]-q[0])-(q[0]-p[0])*(r[1]-q[1])
    return 0 if abs(v)<1e-12 else (1 if v>0 else 2)
def segments_intersect(p1,q1,p2,q2):
    a,b,c,d=orientation(p1,q1,p2),orientation(p1,q1,q2),orientation(p2,q2,p1),orientation(p2,q2,q1)
    return (a!=b and c!=d) or (a==0 and on_segment(p1,p2,q1)) or (b==0 and on_segment(p1,q2,q1)) or (c==0 and on_segment(p2,p1,q2)) or (d==0 and on_segment(p2,q1,q2))
def polyline_conflict(a,b):
    return any(segments_intersect(a[i],a[i+1],b[j],b[j+1]) for i in range(len(a)-1) for j in range(len(b)-1))
