

class WorkflowException(Exception):
  def __init__(self,msg,**kwargs):
    self.msg = msg
    self.kwargs = kwargs
  
