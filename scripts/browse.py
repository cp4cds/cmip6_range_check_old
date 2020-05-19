import cmd, glob, json
import utils
from dreqPy import dreq

import local_utilities

class Variables(dict):
  def __init__(self,data_dir = "json_ranges" ):
    for table in utils.table_list:
      fl = glob.glob( "%s/%s/*.json" % (data_dir,table) )
      for f in fl:
        fname = f.rpartition( "/" )[-1]
        var = fname.split("_")[0]
        self["%s.%s" % (table,var)] = (0,f,None)

class Test(cmd.Cmd):
  def __init__(self):
    self.vars = Variables()
    self.check_json = local_utilities.check_json
    super(Test, self).__init__()


  def do_x(self,line):
    print ("x", line )


  def default(self,line):
    words = line.split()
    if words[0] in self.vars:
      this = json.load( open( self.vars[words[0]][1] ) )
      print ( this.keys() )
      print ( this["data"].keys() )
    elif words[0][0] == "!":
      print ("bang" )
    else:
      cmd.Cmd.default(self,line)

  def do_check(self,line):
    words = line.split()
    table, var = words[0].split( "." )
    self.check_json( table, var=var )

  def do_eval(self,line):
    """Evaluate the line in python session."""
    try:
      eval ( line )
    except:
      print ( "Failed to execute %s" % line )

  def do_exit(self,line):
    return True

class TestRq(Test):
  def __init__(self):
    self.dq = dreq.loadDreq()
    super(TestRq, self).__init__()

    self.CMORvar_by_id = dict()
    for i in self.dq.coll["CMORvar"].items:
      self.CMORvar_by_id["%s.%s" % (i.mipTable,i.label) ] = i

t = TestRq()
t.cmdloop()
    
