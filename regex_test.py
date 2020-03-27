import re
import os

reobj = re.compile("^[ ]*[^\n()]+[ ]+[^\n()]+[::]*[a-zA-Z]+\([^;{]*\n[ ]*{", flags=re.MULTILINE)
for  root, dirs,files in os.walk('C:\\Users\\Svyatoslav.Kovalev\\Documents\\avc_regex_test\\avc\\avc'):
    for file in files:
      try:
        if ".cpp" in file:
          pos = 0
          allfile = ""
          with open(root + "\\" + file, 'r',errors='ignore') as f:
            allfile = f.read()
            #print(root + "\\" + file,":")
            item = reobj.search(allfile, pos)
            while item != None:
              #print(item.start(), item.end())
              tmp = item[0]
              if "catch" in tmp or "switch" in tmp or "class" in tmp or "BOOST_SCOPE_EXIT" in tmp or "if" in tmp or "return" in tmp:
                pos = item.end()
                item = reobj.search(allfile, pos)
                continue
              else:
                bfr = allfile[:item.end()]
                nsrt = "printf(\"Hallo\\n\");"
                tl = allfile[item.end():]
                newallfile = bfr
                newallfile += nsrt
                newallfile += tl
                allfile = newallfile
                pos = item.end() + len(nsrt)
                item = reobj.search(allfile, pos)
                #print(item[0])
              #input(" ")
          with open(root + "\\" + file, 'w',errors='ignore') as f:
            f.write(allfile)
      except IOError as ioerror:
        print(ioerror.args)

