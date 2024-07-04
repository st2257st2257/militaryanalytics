from pathlib import Path
import shutil
import os

src = '../media/fileImages'
trg = '../static/fileImages'

files = os.listdir(src)

for fileName in files:
    print(fileName)
    # if fileName.split('.')[-1] == "xls":
    shutil.copy2(os.path.join(src, fileName), trg)
    #  os.remove(src + "/" + fileName)
