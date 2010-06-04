# License: zlib license
# see accompanying LICENSE file
import os, sys, optparse, parse, libutil
from bmkcompilers import compilers
from util import get_platforms

tasks = {}
built = []
START_POINT = "start"
COMPILER = "mingw"
FILE = "build.bmk"
REBUILD = False

def composite_options(platformopts):
  options = {}
  p = get_platforms()
  
  for platform,opts in platformopts.iteritems():
    if platform != "none" and (not platform in p):
      continue
      
    for k,v in opts.iteritems():
      if k in options: # append to the already-existing option
        options[k].extend(v)
        continue
      options[k] = v
  
  return options

def buildtask(task):
  libs     = []
  source   = []
  objs     = []
  requires = []
  type     = ""
  out      = ""
  
  if task in built:
    print "skipping '%s' - already built" % task
    return
    
  if not task in tasks:
    print "skipping - unknown task '%s'" % task
    return
  
  for k,v in tasks[task].iteritems():
    if k == "depends":
      for d in v:
        print "building depend %s" % d
        buildtask(d)
    elif k == "libs":
      libs = v
    elif k == "source":
      source = v
    elif k == "requires":
      requires = v
    elif k == "type":
      type = v[0]
    elif k == "out":
      out = v[0]
    elif k == "objs":
      objs = v
    else:
      print "unknown option '%s'" % k
      
  if len(source) == 0 and len(objs) == 0:
    # no sources or object files, skip it
    return
      
  print "<%s>" % task
  print "  libs:", libs
  print "  source:", source
  print "  requires:", requires
  print "  type:", type
  print "  out:", out
  print ""
  
  c = compilers[COMPILER]() # new instance of compiler
  for x in source: c.add_source(x)
  for x in libs: c.add_lib(x)
  for x in objs: c.add_obj(x)
  c.set_type(type)
  c.set_out(out)
  
  for d in requires:
    l = libutil.find_package(d)
    if l is None:
      print "error: couldn't find required package '%s'" % d
      return
    
    c.add_lib_dir(l[0])
    c.add_lib(l[1])
  
  c.prepare()
  
  touched = False
  try: otime = os.path.getmtime(c.out)
  except:
    otime = None
    touched = True
  
  for x in source:
    if not os.path.exists(x):
      print "error: source file '%s' not found" % x
      sys.exit(4)

    if not touched and not REBUILD and otime is not None:
      if os.path.getmtime(x) > otime:
        touched = True
        
  if not touched:
    print "skipping '%s' - not modified" % task
    return # don't need to rebuild
    
  if not c.build():
    # build failed
    print "build failed"
    sys.exit(1)
  
  built.append(task)
  
def main():
  global tasks, START_POINT, FILE, COMPILER, REBUILD
  
  opt = optparse.OptionParser()
  opt.add_option("-f", "--in", dest="file", help="input .bmk file", metavar="FILE", default=FILE)
  opt.add_option("-s", "--start", dest="startpoint", help="which task to start with", metavar="STARTPOINT", default=START_POINT)
  opt.add_option("-c", "--compiler", dest="compiler", help="which compiler to use", metavar="COMPILER", default=COMPILER)
  opt.add_option("-r", "--rebuild", dest="rebuild", help="rebuild project (skip checking of file dates)", action="store_true", metavar="REBUILD", default=REBUILD)
  opt.add_option("", "--debug", help="turn debugging on", action="store_true", default=False, metavar="DEBUG")
  
  options, args = opt.parse_args()
  
  START_POINT = options.startpoint
  FILE = options.file
  COMPILER = options.compiler
  REBUILD = options.rebuild
    
  print "platform:", get_platforms()
    
  try:
    f = open(FILE, "r")
    text = f.read()
    f.close()
  except:
    print "error opening file %s" % FILE
    sys.exit(1)

  p = parse.bmk_parse(text)
  tasks = p["tasks"]
  
  # composite them all
  for k,platformopts in tasks.iteritems():
    tasks[k] = composite_options(platformopts)
    
  print "building %s" % START_POINT
  
  # check for (start)
  if START_POINT in tasks:
    buildtask(START_POINT)
  else:
    print "error: no task '%s'" % START_POINT
    sys.exit(2)
    
if __name__ == '__main__': main()