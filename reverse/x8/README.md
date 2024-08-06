# x8

Reverse engineering challenge I created for TFC CTF 2024

## Build instructions

`cargo run -- --file program.bin` to generate a debug build -- this creates the challenge file

`cargo build --release` to generate the actual program

## Challenge idea

A small virtual machine, which interprets a list of instructions.

The `program.bin` file does 2 things:

1. Decodes the rest of the program: it iterates through the rest of the program and applies the XOR operation with
the value 0x41

2. Runs the rest of the program after decoding, with an algorithm equivalent to
the following pseudocode:

```
R0 = FLAG_LEN;
while (R0 != 0) {
   R3 = pop(); // read byte
   R4 = deref([R1:R2]); // xor value
   R4 ^= 0x41
   R2 += 1;
   R5 = deref([R1:R2]); // xor flag
   R5 ^= 0x41;
   R2 += 1;
   R3 ^= R4;
   if (R3 != R5) {
       fail!;
   }
}
success!;
```

R0-R7 are general purpose registers

PC/R8 is the program counter

SP/R9 is the stack pointer

The memory layout is as follows:

```
[0, 0x100) => instructions
[0x100, 0x300) => memory
[0x300, 0x400) => stack
```

All registers are 8-bit, but some instructions allow referencing a 16-bit address
with 2 registers/values (`[high:low]`)

The flag is encoded as follows:

- A sequence of random numbers is generated, which represents the XOR values
- The flag is XORed with each number
- The pair `(xor_result ^ 0x41, xor_value ^ 0x41)` is stored in the program memory,
for each flag byte

When reading input, the VM stores the result on the stack. So, the algorithm pops
each read letter from the stack, XORs it with the XOR value from the data segment 
and checks if the result is equal to the XOR result from memory.
