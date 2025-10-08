import os
import sys
import shutil
if sys.argv[1] != "false":
    os.system("git add .")
    os.system(f"git commit -m \"{sys.argv[1]}\"")
    os.system("git push")
shutil.copy(os.getcwd() + "/engine.py", os.getcwd() + "/chess-engine")