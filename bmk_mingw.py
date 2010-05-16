# License: zlib license
# see accompanying LICENSE file

from compiler import Compiler
from util import bmk_exec, prefixargs

class BMKC_MinGW(Compiler):
  bin = "gcc"
  
  def _gen_command(self):
    cmd = self.bin
    cmd += " "
    cmd += " ".join(self.source)
    cmd += " "
    cmd += " ".join(self.objs)
    cmd += " "
    cmd += " -o " + self.out
    cmd += " "
    cmd += " " + self.optimization
    cmd += " "
    cmd += prefixargs("-I", self.include_dirs)
    cmd += " "
    cmd += prefixargs("-L", self.lib_dirs)
    cmd += " "
    cmd += prefixargs("-l", self.libs)
    cmd += " "
    cmd += self.flags
    
    return cmd
    
  def build(self):
    cmd = self._gen_command()
    print "cmd:", cmd
    # run it
    r = bmk_exec(cmd)
    print "compiler returned:", r
    return True
    