import cmd, glob, json
import utils

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

  def do_exit(self,line):
    return True



t = Test()
t.cmdloop()
    
