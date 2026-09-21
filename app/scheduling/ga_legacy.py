import random
def crossover(parents,count):
    children=[]
    if not parents:return children
    while len(children)<max(0,count-len(parents)):
        a,b=random.sample(parents,2) if len(parents)>1 else (parents[0],parents[0])
        n=len(a)//2
        if n<2:break
        A=[(a[i],a[n+i]) for i in range(n)]; B=[(b[i],b[n+i]) for i in range(n)]
        l,r=sorted(random.sample(range(n),2)); seg=B[l:r]; ids={g[0] for g in seg}; c=[]
        for i,g in enumerate(A):
            if i==l:c+=seg
            if g[0] not in ids:c.append(g)
        c=c[:n]; children.append([g[0] for g in c]+[g[1] for g in c])
    return children
def local_improve(x,distance_fn,tries=20):
    best=x[:]; bd=distance_fn(best); n=len(x)//2
    for _ in range(tries):
        y=best[:]; a,b=random.sample(range(n),2); y[a],y[b]=y[b],y[a]; d=distance_fn(y)
        if d<bd:best,bd=y,d
    return best
def task_crane(x,sampled_rows_x,sampled_rows_y):
    n=len(x)//2; seq,alloc=x[:n],x[n:]; a,b=[],[]
    for i,t in enumerate(seq):
        (a if int(alloc[i])==0 else b).append(t)
    return a,b,max(len(a),len(b))
