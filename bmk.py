# License: zlib license
# see accompanying LICENSE file
import os, sys, re, parse

f = open("test.bmk", "r")
text = f.read()
f.close()

p = parse.bmk_parse(text)

tasks = p["tasks"]

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

for task,platforms in tasks.iteritems():
  print "[%s]" % task
  
  for platform,options in platforms.iteritems():
    print "  platform:", platform
    
    for option,value in options.iteritems():
      print "    %s: %s" % (option, value)
  
  print "[/%s]" % task
