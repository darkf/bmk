# License: zlib license
# see accompanying LICENSE file
import re
from odict import odict

class Scanner:
  rules  = odict()
  text   = ""
  tokens = []
  index  = 0
  compre = {}
  
  def __init__(self, ignoreNone = True):
    self.ignoreNone = ignoreNone
  
  def setText(self, text):
    self.text = text
  
  def addRule(self, rule, action):
    self.rules[rule] = action
    
  def __setitem__(self, rule, action):
    self.addRule(rule, action)
    
  def parse(self):
    pos = 0
    
    while True:
      if self.text[pos:] == '': # no more text to cover
        break
    
      for k,v in self.rules.iteritems():
        try: # check if the regex is precompiled
          m = self.compre[k].match(self.text, pos)
        except KeyError: # otherwise compile it
          self.compre[k] = re.compile(k)
          m = self.compre[k].match(self.text, pos)
        
        if not m: # no match
          continue
        
        #print "matched '%s' -> '%s'" % (k, m.group(0))
        pos = m.end()
        
        if callable(v):
          v = v(m.group)
          
        try:
          if v[0] is None and self.ignoreNone: # ignore it and get new token
            break
        except:
          if v is None and self.ignoreNone:
            break
          
        self.tokens.append(v)
        
  def reset(self):
    self.tokens = []
    self.index = 0
    self.text = ""
    
  def peek(self):
    if self.index >= len(self.tokens):
      raise StopIteration

    return self.tokens[self.index]
    
  def get(self):
    r = self.peek()
    self.index += 1
    return r
    
  def next(self):
    return self.get()
    
  def __iter__(self):
    return self