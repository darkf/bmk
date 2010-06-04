# License: zlib license
# see accompanying LICENSE file

import sys, re, subprocess
  
# didn't say it had to be correct
posix_platforms = "linux darwin freebsd hpux sunos cygwin"

def get_platforms():
  # returns a list based on the platform we're running on
  # e.g. ["posix", "linux"], ["posix", "freebsd"], ["win32"] ...
  p = sys.platform
  
  if p == "win32":
    return ["win32"]
    
  s = re.split('\d+$', p)[0]
  if s in posix_platforms:
    return ["posix", s]
    
  if os.name == "posix":
    return ["posix", s]
  
  return [p]
  
def bmk_exec(args):
  try:
    proc = subprocess.Popen(args)#, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return proc.wait()
    #os.system(args)
  except Exception, e:
    print "build failed:", e
    sys.exit(3)
  
def prefixargs(p, a):
  return " ".join([p + x for x in a])