# License: zlib license
# see accompanying LICENSE file

import subprocess

def bmk_exec(args):
  proc = subprocess.Popen(args)#, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  return proc.wait()
  #os.system(args)
  
def prefixargs(p, a):
  return " ".join([p + x for x in a])