import os
for count in range(12):
    os.system("git clone https://github.com/lichess-bot-devs/lichess-bot.git")
    if count != 11:
        os.rename("lichess-bot", f"stockfish-{count*10}CPL")