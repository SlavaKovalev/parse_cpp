import re
import os

for  root, dirs,files in os.walk('C:\\Users\\Svyatoslav.Kovalev\\Documents\\avc'):
    for file in files:
      try:
        if ".cpp" in file:
          with open(root + "\\" + file, 'r',errors='ignore') as f:
            allfile = f.read()
            print(root + "\\" + file,":")
            for item in re.finditer("^[ ]*[^\n()]+[ ]+[^\n()]+[::]*[a-zA-Z]+\([^;{]*\n[ ]*{", allfile, flags=re.MULTILINE):
              tmp = item[0]
              if "catch" in tmp or "switch" in tmp or "class" in tmp or "BOOST_SCOPE_EXIT" in tmp or "if" in tmp or "return" in tmp:
                continue
              else:
                print(item[0])
              input(" ")
      except IOError as ioerror:
        print(ioerror.args)

