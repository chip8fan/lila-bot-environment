import threading
import os
import subprocess
current_dir = os.getcwd()
def run_bot(dir):
    os.chdir(dir)
    process = subprocess.Popen(["python3", "lichess-bot.py"], cwd=dir)
for count in range(11):
    bot_dir = f"{current_dir}/stockfish-{count*10}CPL"
    thread = threading.Thread(target=run_bot, args=(bot_dir,))
    thread.start()