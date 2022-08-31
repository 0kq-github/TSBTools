import os
import subprocess

with open("test.py",mode="r") as f:
  old = f.read()
os.remove("test.py")
with open("test.py",mode="w") as f:
  f.write("print(\"Updated!\")\nexit()\n"+old)
subprocess.Popen(["python","test.py"])