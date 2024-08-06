# Solution

The problem with the server is that it assigns an ID for each player and uses it to perform actions without any further validation. This means that if we can get the ID of the bot, we can use it to perform actions on the bot's behalf.

The bot is just another player in the game. One simple solution is to add the following to the provided `play.py` file:

```python
# add to get_input function
elif ch == "w":
    for i in range(100):
        s.send(f"{i}|M|0;".encode())
```

After pressing `w`, the bot will move left and we will be able to shoot it and get the flag.