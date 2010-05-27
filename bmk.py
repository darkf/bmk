# License: zlib license
# see accompanying LICENSE file
import os, sys, re, parse, libutil
from bmkcompilers import compilers
from util import get_platforms

tasks = {}
built = []
START_POINT = "start"
COMPILER = "mingw"
FILE = "build.bmk"

def composite_options(platformopts):
  options = {}
  p = get_platforms()
  
  for platform,opts in platformopts.iteritems():
    if platform != "none" and (not platform in p):
      continue
      
    # problem: if you have, say,
    # [posix]
    # out: foo
    # [linux]
    # out: bar
    #
    # then composited it will be out: foo bar
    # but which one do we choose? :)
    #
    # I could add some more syntax, such as:
    # !out: bar
    # or
    # out!: bar
    # which would force it to out: bar
      
    for k,v in opts.iteritems():
      if k in options: # append to the already-existing option
        options[k].extend(v)
        continue
      options[k] = v
  
  return options

def buildtask(task):
  libs     = []
  source   = []
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
    else:
      print "unknown option '%s'" % k
      
  if len(source) == 0:
    # no sources, skip it
    return
      
  print "<%s>" % task
  print "  libs:", libs
  print "  source:", source
  print "  requires:", requires
  print "  type:", type
  print "  out:", out
  print ""
  
  c = compilers[COMPILER]() # new instance of compiler
  for x in libs: c.add_lib(x)
  for x in source: c.add_source(x)
  c.set_type(type)
  c.set_out(out)
  
  for d in requires:
    l = libutil.find_lib(d)
    if l is None:
      print "error: couldn't find required library '%s'" % d
      return
    
    c.add_lib_dir(l[0])
    c.add_lib(l[1])
    
  if not c.build():
    # build failed
    print "build failed"
    sys.exit(1)
  
  built.append(task)
  
def main():
  global tasks, START_POINT, FILE
  
  if len(sys.argv) > 1:
    START_POINT = sys.argv[1]
    
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