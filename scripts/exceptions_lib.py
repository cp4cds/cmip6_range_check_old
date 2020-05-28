

class BasicFileStructureException(Exception):
    pass

class WorkflowException(Exception):
  def __init__(self,msg,**kwargs):
    self.msg = msg
    self.kwargs = kwargs
  
class InstantiationValueException(ValueError):
  def __init__(self,msg,**kwargs):
    self.msg = msg
    self.kwargs = kwargs
  
