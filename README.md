# Portfolio-Project-CPU-Simulator
Portfolio Project CPU Simulator from CodeCademy's Computer Science career path

The goal of this project was to create a program that would be able to mirror the functioning of a CPU, with the help of different instances that are the CPU itself, the CPU's registers, the Cache, the Memory. Each of these instances has its class created in this project. 

The file "cpu.py" is the main one, where are defined the core working rules for the processor, how it manages the flow of instructions, how it returns output to the user, how it decodes the instructions that are formulated in the MIPS assembly language, how it manages the cache, how it stops its own work and returns execution time when the instructions are over.

The file 'registers.py' defines the corresponding class. To note that we have defined a 32 slots register with 24 to be used by the instructions, 8 to be used by the data (with exchanges with the cache and memory). The limitation of 24 instructions that can be stored drove me to design a system in which the instructions renew themselves, on base of the file containing the whole list of instructions, when a 'slice' of 24 instructions was proceeded and there are more to handle in the base file. While it might not be how real processors' registers work, this way to design my imaginary processor's register provided a challenge as to how to automatically renew the instructions, and in this sense is justified. It would have been easier but less enriching to have only data registers and to proceed the instructions from the file one by one.

The file 'memory.py' defines the corresponding class. Memory was given 64 slots.

The file 'cache.py' defines the corresponding class. Cache has 8 slots and as a default setting is not enabled on the cpu. I defined a fifo replacement policy. No rules for associativity, any memory slot can be represented in any cache slot. The write policy is of the type 'write-back'. If we modify a memory slot represented in the cache, it will be written into memory only when the memory slot exits the cache. 

The file 'memory' contains instructions as to how to populate the memory before starting the instructions program.

The file 'instructions' contains instructions in MIPS assembly language to be proceeded by the cpu. The functions that were modelized in the program are add, addi (add a constraint), sub, slt (comparing two values), cache (activate/reinitialize/deactivate the cache), jump (move to a subsequent instruction), lw (load from memory to register), sw (store from memory to register) halt (stop execution). Arithmetic operations are made between two registers with storage in a third register of the result. Lw and sw involve data registers as well as the memory and potentially the cache. 

