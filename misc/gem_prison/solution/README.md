# Solution

This was inspired by a challenge from [DownUnderCTF 2023](https://github.com/DownUnderCTF/Challenges_2023_Public/tree/main/misc/real-baby-ruby). Tried to make it harder by adding a few more restrictions, but failed to do so.

This had uninteded solutions that allowed just printing the flag to STDOUT - was supposed to close it in the source.

The intended solution was to use the `$\` separator to read the flag byte by byte. Solve script in `solve.py`