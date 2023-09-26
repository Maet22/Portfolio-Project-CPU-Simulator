class Memory():
  def __init__(self, name = 'My Memory'):
    self.name = name
    #memory has 64 slots
    self.data = [''] * 64
  def get_non_empty_slots(self):
    #list of non empty slots will be used to populate the cache
    non_empty = []
    i=0
    for data in self.data:
      if data != '':
        non_empty.append(i)
      i+=1
    return non_empty

  def __repr__(self):
    i=0
    empty = 0
    for slot in self.data:
      if slot == '':
        print(f'SLOT {i}: EMPTY')
        empty+=1
      else:
        print(f'SLOT {i}: {slot}')
      i+=1
    capacity = str(empty) + ' AVAILABLE MEMORY SLOTS OUT OF 64!'
    return capacity
    
  def write_to_memory(self,destination,value):
    self.data[destination] = value
  



