class Cache():
  def __init__(self,name = 'My Cache'):
    self.name = name
    self.data = [
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""}
    ]
    self.fifo_idx = 0
  def get_from_cache(self, address):
    for entry in self.data:
      if entry["tag"] == address:          
          return entry["data"]    
    return None
  def replace_value(self,address,value):
    #when we want to store in memory a value from register that is different from initial memory value
    self.data[address]['data'] = value
    
  def test_tag(self,tag):
    #test tag is used to check if a given memory slot is present in the cache (used for function sw)
    i=0
    for entry in self.data:
      if entry['tag'] == tag:
        return i
      i+=1
    return None

    
    
