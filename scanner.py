# License: zlib license
# see accompanying LICENSE file
import re

class Scanner:
  tokens = []
  rules  = {}
  comrx  = {}
  text   = ""
  pos    = 0
  
  def __init__(self, ignoreNone = False):
    self.ignoreNone = ignoreNone
  
  def setText(self, text):
    self.text = text
    
  def addText(self, text):
    self.text += text
  
  def addRule(self, rule, tok):
    self.rules[rule] = tok
    
  def getToken(self, advance = True):
    if self.text[self.pos:] == '':
      raise StopIteration
    
    for k,v in self.rules.iteritems():
      try:
        m = self.comrx[k].match(self.text, self.pos)
      except KeyError:
        self.comrx[k] = re.compile(k)
        m = self.comrx[k].match(self.text, self.pos)
        
      if not m:
        continue
      
      #print "matched '%s' -> '%s'" % (k, m.group(0))
      if advance:
        self.pos = m.end()
      
      if callable(v):
        v = v(m.group(0), m.group)
        if v is None and self.ignoreNone:
          return self.getToken()
        self.tokens.append(v)
        return v
      self.tokens.append(v)
      return v
      
    raise StopIteration
    
  def peek(self):
    return self.getToken(False)
    
  def next(self):
    return self.getToken()
    
  def __iter__(self):
    return self
   
"""   
# test
s = Scanner()
s.setText("one two <three> [four] ([five]) ()")
s.addRule(r" |\t", lambda v: None)
s.addRule(r"[a-zA-Z]+", "ident")
s.addRule(r"\[[a-zA-z]+\]", "sqbracketed")
s.addRule(r"<[a-zA-Z]+>", "bracketed")
s.addRule(r"\(.*?\)", "paren'd")

print "text:", s.text

while True:
  try:
    v = s.getToken()
    if v is not None:
      print v
  except StopIteration:
    break
"""
    