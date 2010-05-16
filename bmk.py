# License: zlib license
# see accompanying LICENSE file
import os, sys, re, parse, libutil
from bmkcompilers import compilers

f = open("test.bmk", "r")
text = f.read()
f.close()

p = parse.bmk_parse(text)

tasks = p["tasks"]
built = []
START_POINT = "start"
COMPILER = "mingw"

# didn't say it had to be correct
posix_platforms = "linux darwin freebsd hpux sunos cygwin"

def get_platforms():
  # returns a list based on the platform we're running on
  # e.g. ["posix", "linux"], ["posix", "freebsd"], ["win32"] ...
  p = sys.platform
  
  #print "p:", p
  
  if p == "win32":
    return ["win32"]
    
  s = re.split('\d+$', p)[0]
  if s in posix_platforms:
    return ["posix", s]
    
  if os.name == "posix":
    return ["posix", s]
  
  return [p]

#print "\n\n\n\n"

print "platform:", get_platforms()

def composite_platforms(platforms):
  options = {}
  p = get_platforms()
  
  for platform,opts in platforms.iteritems():
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
      if options.has_key(k): # append to the already-existing option
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
    
  if not tasks.has_key(task):
    print "skipping - unknown task '%s'" % task
    return
  
  for k,v in tasks[task].iteritems():
    if k == "depends":
      for t in v:
        print "building depend %s" % t
        buildtask(t)
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
  [c.add_lib(x) for x in libs]
  [c.add_source(x) for x in source]
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
    del c
    sys.exit(1)
    
  del c
  
  built.append(task)
  
  
def main():
  global tasks, START_POINT
  
  if len(sys.argv) > 1:
    START_POINT = sys.argv[1]
  
  # composite them all
  for k,platforms in tasks.iteritems():
    tasks[k] = composite_platforms(platforms)
    
  print "building %s" % START_POINT
  
  # check for (start)
  if tasks.has_key(START_POINT):
    buildtask(START_POINT)
  else:
    print "error: no start task"
    return
    
    
if __name__ == '__main__': main()