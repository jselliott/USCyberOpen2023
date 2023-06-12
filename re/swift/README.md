# Swift

My buddy tried and tried to get tickets to the Eras Tour but failed. To take his mind off it, he decided to experiment with creating a new programming language with a simple set of operations and two registers in a simulated processor. I've got a "Blank Space baby", for a flag.....

This challenge uses Taylow Swift songs to encode simple instructions into a 5,000 line "program".

## Solution

Much of the program is unreachable junk but starting at the top line there is the instructions "Jump Then Fall" followed by a number. A little intuition would lead the player to realize this is an instruction to jump to a certain line in the program. Following these jumps, there are other opcodes that appear in a sequence "Blank Space", "Change", "Both Of Us", and "Breath". Which are essentially, "Set a register to 0", "Set a register value", "XOR two registers", "Print a register". Follwing the instructions and jumps, the encoded flag is XOR'd with a key and printed.

### Solution Code

```python

registers = [0,0]

program = [line for line in open("program.swft","r").readlines()]

pc = 0

test = 0

while True:

    x = program[pc].strip().split("\t")

    if x[0] == "Jump Then Fall":
        pc = int(x[1])
        continue
    elif x[0] == "Change":
        r = int(x[1])
        v = int(x[2])
        registers[r] = v
    elif x[0] == "Blank Space":
        r = int(x[1])
        registers[r] = 0
    elif x[0] == "Both of Us":
        r1 = int(x[1])
        r2 = int(x[2])
        registers[r1] = registers[r1] ^ registers[r2]
    elif x[0] == "Breathe":
        r = int(x[1])
        print(chr(registers[r]),end="")
    elif x[0] == "End Game":
        exit()
    pc += 1
    
```