import os, sys, parse

f = open("test.bmk", "r")
text = f.read()
f.close()

p = parse.bmk_parse(text)

tasks = p["tasks"]

"""
print ""
print ""

for task,platforms in tasks.iteritems():
  print "[%s]" % task
  
  for platform,options in platforms.iteritems():
    print "  platform:", platform
    
    for option,value in options.iteritems():
      print "    %s: %s" % (option, value)
  
  print "[/%s]" % task
"""