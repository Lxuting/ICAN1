from .ppo_agent import PPOAgent
class CraneScheduler:
    def __init__(self,n_cranes=2):self.agent=PPOAgent(n_cranes);self.n=n_cranes
    def schedule(self,tasks,cranes):
        loads=[0]*self.n; out=[]
        for t in sorted(tasks,key=lambda x:self.agent.score_task(x),reverse=True):
            k=self.agent.select_action({"crane_loads":loads}); loads[k]+=t.get("duration",1)
            out.append({"task_id":t.get("task_id","T001"),"coil_id":t.get("coil_id","G2025001"),
                        "crane":cranes[k],"target":t.get("target","B区-05-03"),
                        "status":"运行中" if not out else "待命"})
        return out
