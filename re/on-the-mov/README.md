# On The MOV

This challenge involves a simple crackme-style binary which has been MOVfuscated. Meaning that every opcode has been replaced instead with a series of MOV instructions. This makes the program funtionally the same but must more difficult to debug or reverse engineer.

## Solution

There are a few different ways to approach this challenge. Some players who are more familiar with tools like Angr can use it to simulate and explore different paths in the program until they find one that reaches the success state indicating they have the correct flag.

Another option for bare-metal linux players is to use the *perf* command to measure the number of instructions that are executed. By looping through each possible ASCII character and running the executable through perf, the correct letter will cause more instructions to be executed because the program advanced further in the execution instead of exiting. This allows for a very fast brute-force of the flag without needing to understand the underlying logic.

The final option is just to use your debug tool of choice and try to find the point where a comparison is happening between the flag and the input and see if you can capture each byte of the encoded flag as well as the xor key which is only a single byte.