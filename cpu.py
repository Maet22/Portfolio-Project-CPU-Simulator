from registers import Register
from memory import Memory
from cache import Cache
from random import randint


class cpu():
  def __init__(self,name = 'My CPU'):
    self.register = Register()
    self.memory =  Memory()
    self.counter = 0
    self.stop = False
    #24 instructions registers therefore if more than 24 instructions they will be sliced into batches of 24 and these batches will be proceeded one by one
    self.slice = 1
    self.slice_from = (self.slice-1)*24 +1
    self.slice_to = (self.slice)*24
    self.processing_time = 0
    self.cache = None
  def fifo_replacement(self,new_tag,new_value):
    #replacement policy for the cache is fifo
    #write back writing policy: the modified data gets written into memory when it exits the cache
    mem_slot = self.cache.data[self.cache.fifo_idx]['tag']
    mem_value = self.cache.data[self.cache.fifo_idx]['data']
    self.memory.data[mem_slot] = mem_value
    self.cache.data[self.cache.fifo_idx]['tag'] = new_tag
    self.cache.data[self.cache.fifo_idx]['data'] = new_value
    self.cache.fifo_idx += 1
    if self.cache.fifo_idx == 8:
      self.cache.fifo_idx = 0
  def init_cache(self):
    #cache is by default not activated, when activated it gets populated with random values from the memory
    filled = 0
    mem = self.memory.get_non_empty_slots()
    while filled < 8: 
      if mem == []:
        break             
      pick_in_memory = randint(0, len(mem)-1)
      pop = mem.pop(pick_in_memory)    
      self.cache.data[filled]["tag"] = pop
      self.cache.data[filled]["data"] = self.memory.data[pop]      
      filled+=1
    self.cache.fifo_idx = 0    
  def populate_memory(self,file):
    #alongside with the instructions file, a memory file is used to fill the memory before starting to execute the instructions
    with open(file) as codefile:
        code = codefile.readlines()
        mem_data = [line.strip() for line in code if line.strip() != '']                  
        for dat in mem_data:
            splitted = dat.split(' ')
            index = int(splitted[0][1:])
            data = int(splitted[1])
            self.memory.write_to_memory(index,data)    
        
  def set_cache(self,indic):
    if indic == 0:
      self.cache = None
      print('CACHE UNACTIVATED!')
    elif indic == 1:
      self.cache = Cache()
      self.init_cache()
      print('CACHE ACTIVATED!')
    elif indic == 2:
      #cache flush: we populate the cache with new random values from memory
      if self.cache == None:
        self.cache = Cache()
        self.init_cache()
        print('CACHE DATA INITIALIZED!')
      else:
        self.init_cache()
        print('CACHE DATA REINITIALIZED!')
  def add(self,rd,r1,r2):
    self.register.add_to_register(rd,self.register.get_register_value(r1)+ self.register.get_register_value(r2))
    self.processing_time += 0.3
  def sub(self,rd,r1,r2):
    self.register.add_to_register(rd,self.register.get_register_value(r1)- self.register.get_register_value(r2))
    self.processing_time += 0.3
  def add_i(self,rd,r1,i):         
    self.register.data[rd] = self.register.data[r1] + i
    self.processing_time += 0.2    
  def slt(self,rd,r1,r2):
    if self.register.get_register_value(r2)>self.register.get_register_value(r1):
      self.register.add_to_register(rd,-1)
    else:
      self.register.add_to_register(rd,0)
    self.processing_time += 0.3  
  def lw(self,reg_target,mem_source):    
    if self.cache != None:
      if self.cache.get_from_cache(mem_source) != None:
        self.register.add_to_register(reg_target,self.cache.get_from_cache(mem_source))
        print("CACHE HIT!")
        self.processing_time += 0.6
      else:
        self.register.add_to_register(reg_target,self.memory.data[mem_source])
        print("CACHE MISS! RECOVERY FROM MAIN MEMORY!")
        self.fifo_replacement(mem_source,self.memory.data[mem_source])
        self.processing_time += 30.1
    else:
      self.register.add_to_register(reg_target,self.memory.data[mem_source])      
      self.processing_time += 30.1

  def sw(self,reg_source,mem_dest):
    if self.cache != None:
      if self.cache.test_tag(mem_dest) != None:
        self.cache.replace_value(self.cache.test_tag(mem_dest),self.register.get_register_value(reg_source))
        self.processing_time += 0.6
        print('CACHE HIT!')
      else:
        self.memory.data[mem_dest] = self.register.get_register_value(reg_source)        
        self.processing_time += 30.1
        print('CACHE MISS! WRITE DIRECTLY TO MAIN MEMORY!')
        self.fifo_replacement(mem_dest,self.memory.data[mem_dest])
    else:
      self.memory.data[mem_dest] = self.register.get_register_value(reg_source)
      self.processing_time += 30.1
  def jump(self,jump):
    self.counter = jump
    self.processing_time += 0.1
  def halt(self):
    #halt will happen if there will be the 'halt' in the instructions or if the instruction the count will point to will be None. It will stop the execution of the program, reset the registers, return the total processing time
    self.processing_time += 0.1
    self.register.reset_registers()    
    print(f'TOTAL PROCESSING TIME = {self.processing_time:.2f} NANOSECONDS')  
    self.stop = True    
  def renew_instructions_registers(self,instructions):
    #we renew the instructions registers when starting the program or reaching the end of a slice of 24 instructions
    if self.slice > 1:
      address = 0
      self.counter = 0
      while address < 24:   
       
        self.register.add_to_register(address,None)
        address +=1
        self.processing_time += 0.1
    address = 0
    from_inst = (self.slice - 1)* 24
    to_inst = self.slice*24        
    for instruction in instructions[from_inst:to_inst]:
      self.register.add_to_register(address,instruction)
      address += 1
      self.processing_time += 0.1     
  def exec_instructions_batch(self,file):
    with open(file) as codefile:
        code = codefile.readlines()
        instructions = [line.strip() for line in code if line.strip() != '']
    if self.stop == True:
      #if prior execution of a file of instructions: we remove the stop status, reset the processing time, counter, slice, remove the cache if any
      self.stop = False
      self.processing_time = 0
      self.counter = 0
      self.slice = 1
      self.cache = None
    self.renew_instructions_registers(instructions) 
         
    while not self.stop:      
      self.execute_instruction(self.register.get_register_value(self.counter),instructions)      
      self.counter += 1
      if self.counter == 24 and not self.stop:        
        self.slice += 1
        self.renew_instructions_registers(instructions)
        print(f'END OF SLICE {self.slice-1}!!\n....LOADING FURTHER INSTRUCTIONS.......')      
  def execute_instruction(self,instruction,instructions):
    if instruction == None:
      print('NO PENDING INSTRUCTIONS!')
      self.halt()
      return    
    splitted = instruction.split(' ')
    #translation from the assembly language of the instructions into Python instructions
    #the execution of each instruction returns the description of what is done for the user      
    if splitted[0] == 'add':
      #add: addition of two regs into a third one
      rd = int(splitted[1][1:])
      rs = int(splitted[2][1:])
      rt = int(splitted[3][1:])
      self.add(rd,rs,rt)
      print(f"{(self.slice-1)*24+self.counter+1} ADDING  R{rs} PLUS R{rt} TO R{rd}")
    elif splitted[0] == 'sub':
      #sub = substraction of two registers into a third one
      rd = int(splitted[1][1:])
      rs = int(splitted[2][1:])
      rt = int(splitted[3][1:])
      self.sub(rd,rs,rt)
      print(f"{(self.slice-1)*24+self.counter+1} SUBSTRACTING R{rt} FROM R{rt} IN R{rd}")
    elif splitted[0] == 'addi':
      #addi: addition of a constant and a reg into an other register
      rt = int(splitted[1][1:])
      rs = int(splitted[2][1:])
      i = int(splitted[3])              
      self.add_i(rt,rs,i)
      print(f"{(self.slice-1)*24 +self.counter+1} ADDING  R{rs} PLUS CONSTANT {i} TO R{rt}")      
    elif splitted[0] == 'slt':
      #we compare two registers and the outcome is stored in a third register
      rd = int(splitted[1][1:])
      rs = int(splitted[2][1:])
      rt = int(splitted[3][1:])
      self.slt(rd,rs,rt)
      print(f"{(self.slice-1)*24+self.counter+1} COMPARING R{rt} AND R{rs}, RESULT IN R{rd}")
    elif splitted[0] == 'j':
      #jump moves to a subsequent instruction that is either in the current slice of instructions or in an other one      
      jump = int(splitted[1])
      print(f"{(self.slice-1)*24+self.counter+1} WE JUMP DIRECTLY TO INSTRUCTION NUMBER {jump}")
      if (jump >= self.slice_from and jump <= self.slice_to):
        self.jump(jump-2)        
      
      else:
        self.slice = jump//24 +1        
        self.renew_instructions_registers(instructions)               
        self.jump((jump%24)-2)
                    
    elif splitted[0] == 'lw':
      #lw: load from memory into register
      rt = int(splitted[1][1:])
      mem_source = int(splitted[2])
      print(f'{(self.slice-1)*24+self.counter+1} ADDING INTO R{rt} WHAT IS IN MEMORY SLOT {mem_source}')
      self.lw(rt,mem_source)      
    elif splitted[0] == 'sw':
      #sw: store from register into memory
      rt = int(splitted[1][1:])
      mem_target = int(splitted[2])
      print(f'{(self.slice-1)*24+self.counter+1} ADDING INTO MEMORY SLOT {mem_target} WHAT IS IN R{rt}')
      self.sw(rt,mem_target)
    elif splitted[0] == 'cache':
      #cache: manipulations with the cache
      self.set_cache(int(splitted[1]))     
    elif splitted[0] == 'halt':    
      
      print('END OF THE INSTRUCTIONS!')
      self.halt()
    else:
      print(f'INSTRUCTION NUMBER {(self.slice-1)*24+self.counter+1} NOT UNDERSTANDABLE!')

          


  

    
    
    

cpu1 = cpu()
cpu1.populate_memory('memory')
cpu1.exec_instructions_batch('instructions')
































  
    
