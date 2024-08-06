# Solution

Python's `random.seed` function will take the absolute value of the given parameter. This means that if the seed is negative, it will be converted to a positive number. This can be exploited to generate the same random numbers for different seeds.

The code is designed in such a way that giving the same seed twice will cancel the shuffle and return the original data. Using this 3 times will give the flag.

Input example: 1, -1, 5, -5, 100, -100