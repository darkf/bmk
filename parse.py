# License: zlib license
# see accompanying LICENSE file
import scanner

tokstr = ""
curtok = None

def SAVE_TOKEN(v, t):
  global tokstr
  tokstr = v
  return t
  
tok_keyword, tok_colon, tok_task, tok_platform, tok_string, tok_newline = range(6)
tok_names = ["tok_keyword", "tok_colon", "tok_task", "tok_platform", "tok_string", "tok_newline"]

scan = scanner.Scanner(True)
scan.addRule(r" |\t", lambda v,a: None)
scan.addRule(r"\n", tok_newline)
scan.addRule(r"[a-zA-Z-._0-9]+", lambda v,a: SAVE_TOKEN(v, tok_keyword))
scan.addRule(r":", tok_colon)
scan.addRule(r"\(([a-zA-Z-_.0-9]+)\)", lambda v,a: SAVE_TOKEN(a(1), tok_task))
scan.addRule(r"\[([a-zA-Z-_.0-9]+)\]", lambda v,a: SAVE_TOKEN(a(1), tok_platform))
scan.addRule(r"/\*.*\*/", lambda v,a: None)
scan.addRule(r"\"(.*)\"", lambda v,a: SAVE_TOKEN(a(1), tok_string))

class Expected(Exception):
  def __init__(self, expected): self.expected = expected
  def __str__(self): return "Expected '%s'" % self.expected

bmkcommands = ["exec"]
  
def parse_values():
  # get values until newline
  vals = []
  while True:
    k = scan.peek()

    if (k is tok_keyword) or (k is tok_string) or (k is tok_task):
      print "vate:", tok_names[scan.getToken()] # eat it
      print "  vtok:", tok_names[k], "(%s)" % tokstr
      vals.append(tokstr)
    else:
      print "  unexpected value (%s)" % tok_names[k]
      break
      
    if scan.peek() is tok_newline:
      print "  vnl!"
      break
      
  return vals
  
def parse_task():
  platforms = {"none": {}, "win32": {}, "posix": {}}
  platform = "none"
  taskname = tokstr
  
  print "[%s]" % taskname
  
  # read the task body
  
  while True:
    if scan.peek() is tok_task:
      # another task - just ignore it and return, the parser will pick it up later
      break
      
    t = scan.getToken()
    
    print "  t:", tok_names[t], "(%s)" % tokstr
    
    if t is tok_keyword and scan.peek() is tok_colon:
      # keyword ':'
      name = tokstr
      print "  eating:", tok_names[scan.getToken()] # eat :
      print "_PEEK_:", tok_names[scan.peek()]
      print "_CONSUME_:", tok_names[scan.getToken()]
      vals = parse_values()
      print "_PEEK2_", tok_names[scan.peek()]
      print "_CONSUME2_", tok_names[scan.getToken()]
      platforms[platform][name] = vals
      print "  %s:%s =" % (platform,name), vals
      continue
      
    if t is tok_keyword and tokstr in bmkcommands:
      # command
      if tokstr == "exec":
        scan.getToken() # get string
        print "exec:", tokstr
        continue
        
    if t is tok_newline:
      print "  inl"
      #continue # ignore newlines
        
    else:
      print "  unknown task-body token:", tok_names[t], "(%s)" % tokstr
      
  print "[/%s]\n" % taskname
      
  return platforms
  
def bmk_parse(text):
  scan.setText(text)
  tasks = {}
  
  while True:
    try:
      # get the first task
      t = scan.getToken()
      
      if t is tok_task:
        # task (build target)
        name = tokstr
        #print "{%s}" % name
        tasks[name] = parse_task()
      
    except StopIteration:
      print "end"
      break
      
  return {"tasks": tasks}
  
"""
def parse_task():
  platforms = {"none": {}, "win32": {}, "posix": {}}
  platform = "none"
  taskname = tokstr

  print "[%s]" % taskname
  
  try:
    while True:
      if scan.peek() is tok_task:
        break
      
      t = scan.getToken()
      
      print "t:", tok_names[t]
      
      if t is tok_keyword:
        name = tokstr
        x = scan.getToken()
        print "tok:", tok_names[x]
        while True:
          if x is tok_newline: x = scan.getToken()
          else: break
        
        if (x is tok_keyword or x is tok_string) and (name in bmkcommands):
          if name == "exec":
            print "  exec:", tokstr
            continue
        
        if x is not tok_colon:
          print "error: expected ':'"
          print "but got %s (%s)" % (tok_names[x], tokstr)
          print "name = %s | t = %s" % (name, tok_names[t])
          raise Expected(':')
        
        vals = parse_values()
        platforms[platform][name] = vals
        #print " ", platform, ":", name, "=", vals
        print "  %s:%s =" % (platform, name), vals
      
      elif t is tok_platform:
        name = tokstr
        #print "  platform:", name
        if not name in platforms.keys():
          print "Unknown platform '%s'" % name
          raise ValueError
        
        platform = name
        
  finally:
    print "[/%s]" % taskname
    print ""
    return platforms
    
def bmk_parse(text):
  scan.setText(text)
  tasks = {}
  
  while True:
    try:
      # get the first task
      t = scan.getToken()
      
      if t is tok_task:
        # task (build target)
        name = tokstr
        #print "{%s}" % name
        tasks[name] = parse_task()
      
    except StopIteration:
      print "end"
      break
      
  #print "tasks:", tasks 
  return {"tasks": tasks}
"""