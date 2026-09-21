class PPOAgent:
    def __init__(self,n_cranes=2):self.n_cranes=n_cranes
    def select_action(self,state):
        loads=state.get("crane_loads",[0]*self.n_cranes); return min(range(self.n_cranes),key=lambda i:loads[i])
    def score_task(self,t,_=None):
        return 2*t.get("priority",1)-.1*t.get("distance",1)-5*t.get("conflict",0)
