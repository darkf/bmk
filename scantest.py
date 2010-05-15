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
scan.addRule(r"[ \t]", lambda v: SAVE_TOKEN("", None))
scan.addRule(r"[\n\r]", lambda v: SAVE_TOKEN("", tok_newline))
scan.addRule(r"[a-zA-Z-._0-9]+", lambda v: SAVE_TOKEN(v(0), tok_keyword))
scan.addRule(r":", lambda v: SAVE_TOKEN("", tok_colon))
scan.addRule(r"\(([a-zA-Z-_.0-9]+)\)", lambda v: SAVE_TOKEN(v(1), tok_task))
scan.addRule(r"\[([a-zA-Z-_.0-9]+)\]", lambda v: SAVE_TOKEN(v(1), tok_platform))
scan.addRule(r"/\*.*\*/", lambda v: SAVE_TOKEN("", None))
scan.addRule(r"\"(.*)\"", lambda v: SAVE_TOKEN(v(1), tok_string))

def printtok(t):
  print "%s [%s]" % (tok_names[t], tokstr)
  
#def printpeek(p):
#  print "[p] %s [%s]" % (tok_names[p], tokstr)
  
f = open("testsmall.bmk", "r")
text = f.read()
f.close()
scan.setText(text)

while True:
  try:
    p = scan.peek()
    printtok(p)
  except StopIteration:
    print "ended on peek"
    break
  try:
    t = scan.getToken()
    printtok(t)
  except StopIteration:
    print "ended on getToken"
    break
  print ""