# License: zlib license
# see accompanying LICENSE file
import scanner

tokstr = ""
bmkdebug = False

def SAVE_TOKEN(v, t):
  return (t, v)
  
tok_keyword, tok_colon, tok_task, tok_platform, tok_string, tok_newline = range(6)
tok_names = ["tok_keyword", "tok_colon", "tok_task", "tok_platform", "tok_string", "tok_newline"]

scan = scanner.Scanner(True)
scan.addRule(r"[ \t]", lambda v: SAVE_TOKEN("", None))
scan.addRule(r"[\n\r]", lambda v: SAVE_TOKEN("", tok_newline))
scan.addRule(r"[a-zA-Z-._0-9]+", lambda v: SAVE_TOKEN(v(0), tok_keyword))
scan.addRule(r":", lambda v: SAVE_TOKEN("", tok_colon))
scan.addRule(r"\(([a-zA-Z-_.0-9]+)\)", lambda v: SAVE_TOKEN(v(1), tok_task))
scan.addRule(r"\[([a-zA-Z-_.0-9]+)\]", lambda v: SAVE_TOKEN(v(1), tok_platform))
scan.addRule(r"/\*.*\*/", lambda v: SAVE_TOKEN("", None))
scan.addRule(r"\"(.*?)\"", lambda v: SAVE_TOKEN(v(1), tok_string))

class Expected(Exception):
  def __init__(self, expected): self.expected = expected
  def __str__(self): return "Expected '%s'" % self.expected

bmkcommands = ["exec"]
  
def peektok():
  global tokstr
  t = scan.peek()
  
  tokstr = t[1]
  return t[0]
  
def gettok():
  global tokstr
  t = scan.get()
  
  tokstr = t[1]
  dlog("%s %s" % (tok_names[t[0]], repr(t[1])))
  return t[0]
  
def dlog(msg):
  if bmkdebug:
    print msg
  
def parse_values():
  # get values until newline
  vals = []
  while True:
    k = peektok()

    if (k is tok_keyword) or (k is tok_string) or (k is tok_task):
      gettok() # eat it
      #print "  vtok:", tok_names[k], "(%s)" % tokstr
      vals.append(tokstr)
    elif k is tok_newline:
      #print "  vnl! [2]"
      break
    else:
      dlog("  unexpected value (%s)" % tok_names[k])
      break
      
    if peektok() is tok_newline:
      #print "  vnl!"
      break
      
  return vals
  
def parse_task():
  platforms = {}
  platform = "none"
  taskname = tokstr
  
  dlog("[%s]" % taskname)
  
  # read the task body
  
  while True:
    try:
      if peektok() is tok_task:
        # another task - just ignore it and return, the parser will pick it up later
        break
      
      t = gettok()
    
      #if t is not tok_newline:
      #  print "  t: %s [%s]" % (tok_names[t], tokstr)
    
      name = tokstr
      if t is tok_keyword and peektok() is tok_colon:
        # keyword ':'
        gettok() # eat :

        vals = parse_values()
        if not platforms.has_key(platform):
          platforms[platform] = {}
        platforms[platform][name] = vals
        dlog("  %s:%s = %s" % (platform, name, repr(vals)))
        continue
      
      elif t is tok_platform:
        # switch platform
        platform = tokstr
        dlog("  switched to platform '%s'" % platform)
      
      elif t is tok_keyword and name in bmkcommands:
        # command
        if name == "exec":
          gettok() # get string
          dlog("  exec: %s" % tokstr)
          continue
        
      elif t is tok_newline:
        #print "  inl"
        #continue # ignore newlines
        pass
        
      else:
        print "  warning: unknown task-body token: %s [%s]" % (tok_names[t], tokstr)
        
    except StopIteration:
      break
      
  dlog("[/%s]\n" % taskname)
  
  return platforms
  
def bmk_parse(text):
  scan.setText(text)
  scan.parse()
  scan.tokens.append((tok_newline, "")) # fixes a bug if there isn't a newline
  tasks = {}
  #print "\n".join(["%s [%s]" % (tok_names[x[0]], x[1]) for x in _tokens if x[0] is not None])
  
  while True:
    try:
      # get the first task
      t = gettok()
      
      if t is tok_task:
        # task (build target)
        name = tokstr
        tasks[name] = parse_task()
      
    except StopIteration:
      break
      
  return {"tasks": tasks}