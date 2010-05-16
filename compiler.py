# License: zlib license
# see accompanying LICENSE file

class Compiler:
  libs = []
  source = []
  objs = []
  include_dirs = []
  lib_dirs = []
  optimization = ""
  flags = ""
  type = "executable"
  out = "a.out"
  
  def add_lib(self, lib): self.libs.append(lib)
  def add_source(self, src): self.source.append(src)
  
  def add_include_dir(self, dir): self.include_dirs.append(dir)
  def add_lib_dir(self, dir): self.lib_dirs.append(dir)
  
  def add_obj(self, obj): self.objs.append(obj)
  def set_optimization(self, o): self.optimization = o
  def add_flag(self, flag): self.flags += " " + flag
  
  def set_type(self, type): self.type = type
  def set_out(self, out): self.out = out
  
  def build(self): return False