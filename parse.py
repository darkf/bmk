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
scan.addRule(r" |\t", lambda v: SAVE_TOKEN("", None))
scan.addRule(r"\n|\r", lambda v: SAVE_TOKEN("", tok_newline))
scan.addRule(r"[a-zA-Z-._0-9]+", lambda v: SAVE_TOKEN(v(0), tok_keyword))
scan.addRule(r":", lambda v: SAVE_TOKEN("", tok_colon))
scan.addRule(r"\(([a-zA-Z-_.0-9]+)\)", lambda v: SAVE_TOKEN(v(1), tok_task))
scan.addRule(r"\[([a-zA-Z-_.0-9]+)\]", lambda v: SAVE_TOKEN(v(1), tok_platform))
scan.addRule(r"/\*.*\*/", lambda v: SAVE_TOKEN("", None))
scan.addRule(r"\"(.*)\"", lambda v: SAVE_TOKEN(v(1), tok_string))

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
      p = scan.peek()
      print "_PEEK_:", tok_names[p], "(%s)" % tokstr
      p = scan.getToken()
      print "_CONSUME_:", tok_names[p], "(%s)" % tokstr
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
        tasks[name] = parse_task()
      
    except StopIteration:
      print "end"
      break
      
  return {"tasks": tasks}