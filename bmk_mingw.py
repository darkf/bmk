# License: zlib license
# see accompanying LICENSE file

from basecompiler import Compiler
from util import bmk_exec, prefixargs

class BMKC_MinGW(Compiler):
  bin = "gcc"
  
  def prepare(self):
    self.gen_command()
  
  def gen_command(self):
    if self.out[-4:] != ".exe":
      # we're on Windows (mingw), add an .exe
      self.out += ".exe"
    cmd = self.bin
    if len(self.source) > 0: cmd += " "; cmd += " ".join(self.source)
    if len(self.objs) > 0:   cmd += " "; cmd += " ".join(self.objs)
    cmd += " -o " + self.out
    if self.optimization: cmd += " "; cmd += " " + self.optimization
    if len(self.include_dirs) > 0:    cmd += " "; cmd += prefixargs("-I", self.include_dirs)
    if len(self.lib_dirs) > 0:        cmd += " "; cmd += prefixargs("-L", self.lib_dirs)
    if len(self.libs) > 0:            cmd += " "; cmd += prefixargs("-l", self.libs)
    if self.flags:                    cmd += " "; cmd += self.flags
    
    return cmd
    
  def build(self):
    cmd = self.gen_command()
    print "cmd:", cmd
    # run it
    r = bmk_exec(cmd)
    print "compiler returned:", r
    
    if r > 0:
      return False
    return True
    