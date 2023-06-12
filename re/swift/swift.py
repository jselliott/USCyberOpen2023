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
    