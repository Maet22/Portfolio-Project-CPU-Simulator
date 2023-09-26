class Register():
  def __init__(self,name = 'My Register'): 
    self.name = name
    #24 first registers will load the instructions and get renewed when necessary, 8 last register will hold values   
    self.data = [None]*24+[0]*8
  def __repr__(self):
    format_repr_register = ['INSTRUCTIONS REGISTERS (0 TO 23)',{'R0': None}, {'R1': None},{'R2': None},{'R3': None},{'R4': None},{'R5': None},{'R6': None},{'R7': None},{'R8': None},{'R9': None},{'R10': None},{'R11': None},{'R12': None},{'R13': None},{'R14': None},{'R15': None},{'R16': None},{'R17': None},{'R18': None},{'R19': None},{'R20': None},{'R21': None},{'R22': None},{'R23': None},'DATA REGISTERS (24 TO 31)',{'R24': None},{'R25': None},{'R26': None},{'R27': None},{'R28': None},{'R29': None},{'R30': None},{'R31': None}]
    reg = 1
    while reg < 34:
      if reg == 25:
        reg+=1
      elif reg < 25:      
        format_repr_register[reg] = {'R'+str(reg-1):self.data[reg-1]}
        reg += 1
      elif reg > 25:
        format_repr_register[reg] = {'R'+str(reg-2):self.data[reg-2]}
        reg+=1
    return str(format_repr_register)  
  def add_to_register(self, destination, value):
    self.data[destination] = value
  def get_register_value(self,register):
    return self.data[register]
  
  def reset_registers(self):
    self.data = [None]*24+[0]*8
      





   
