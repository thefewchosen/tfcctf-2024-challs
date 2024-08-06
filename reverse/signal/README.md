# Signal

Reverse engineering challenge I created for TFC CTF 2024

## Build instructions

`cmake .`

`cmake --build . --clean-first`

Run the binary to generate a new flag, then re-run the last command
to generate the actual binary that uses the flag

## Challenge idea

The flag is read as a command-line argument, then chunks of the flag
are checked across signal handlers.

- SIGSEGV
- SIGTRAP
- SIGILL
- SIGALRM
- SIGPIPE
- SIGABRT
