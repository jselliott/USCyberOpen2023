import random

songs = [x.strip() for x in open("songs.txt").readlines()]

code = [""] * 5000

x = [52,56,41,32,23,91,56,24,8,95,28,55,29,92,30,55,18,90,20,95,52,7,25,94,16,18,3,89,24]
y = [97,107,106,103,108,106,103,115,102,108,107,104,100,108,107,104,101,105,102,108,107,115,107,110,101,112,111,106,101]

cursor = random.randint(1,4999)

code[0] = "Jump Then Fall\t%d" % cursor

for a,b in zip(x,y):

    commands = ["Blank Space\t0","Change\t0\t%d" % a,"Blank Space\t1","Change\t1\t%d" % b,"Both of Us\t0\t1","Breathe\t0"]

    for c in commands:

        code[cursor] = c

        while True:
            new_cursor = random.randint(1,4999)
            if code[new_cursor] == "" and code[new_cursor+1] == "":
                code[cursor+1] = "Jump Then Fall\t%d" % new_cursor
                cursor = new_cursor
                break

code[cursor] = "End Game"

for i in range(len(code)):
    if code[i] == "":
        code[i] = random.choice(songs) + "\t%d\t%d" % (random.choice([0,1,2]),random.randint(0,255))

output = open("program.swft","w")

for c in code:
    output.write("%s\n" % c)