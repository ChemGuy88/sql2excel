"""
Replace contents of and rename all files
"""

from pathlib import Path
import os
import random
import string

targetDir = r"\\hq3hfsvip01\autoreh\Professional Development"
allTargets = Path(targetDir).rglob("*")

def scrambleContents(path):
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

def scrambleName(path):
    bag = string.ascii_letters + "".join([str(num) for num in range(10)])
    newName = "".join(random.sample(bag, len(bag)))
    newPath = os.path.join(path.parent, newName)
    path.rename(newPath)

directories = []
errors = []
for path in allTargets:
    if path.is_file():
        scrambleContents(path)
    elif path.is_dir():
        directories.append(path)
    else:
        errors.append(path)

it = 0
li = []
for path in directories:
    it += 1
    try:
        scrambleName(path)
    except Exception:
        li.append(path)

print(errors)
