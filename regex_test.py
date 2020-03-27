import re
import os

def extract_function_name(template):
  bracket_pos = template.find("(")
  last_not_white_space_pos = 0
  for c in template:
    if c != " ":
      break
    last_not_white_space_pos = last_not_white_space_pos + 1
  return template[last_not_white_space_pos:bracket_pos]

def trace_at_begin(allfile, item, reobj, what_to_print):
  bfr = allfile[:item.end()]
  nsrt = "printf(\"{}\\n\");".format(what_to_print)
  tl = allfile[item.end():]
  newallfile = bfr
  newallfile += nsrt
  newallfile += tl
  allfile = newallfile
  pos = item.end() + len(nsrt)
  return (allfile, pos)

def trace_at_end(allfile, pos, what_to_print):
  open_brace = 1
  close_brace = 0
  while True:
    ob_pos = allfile.find("{", pos)
    cb_pos = allfile.find("}", pos)
    if cb_pos < ob_pos and ob_pos != -1:
      # it is end of brace block
      open_brace = open_brace - 1
      if open_brace == 0:
        bfr = allfile[:cb_pos]
        nsrt = "printf(\"{}\\n\");".format(what_to_print)
        tl = allfile[cb_pos:]
        newallfile = bfr
        newallfile += nsrt
        newallfile += tl
        allfile = newallfile
        break
      pos = cb_pos + 1
      continue
    if cb_pos > ob_pos and ob_pos != -1:
      # we are inside
      pos = ob_pos + 1
      open_brace = open_brace + 1
    if cb_pos > ob_pos and ob_pos == -1:
      open_brace = open_brace - 1
      if open_brace == 0:
        bfr = allfile[:cb_pos]
        nsrt = "printf(\"{}\\n\");".format(what_to_print)
        tl = allfile[cb_pos:]
        newallfile = bfr
        newallfile += nsrt
        newallfile += tl
        allfile = newallfile
        break
      pos = cb_pos + 1
      continue
  return (allfile, pos)

def add_trace():
  reobj = re.compile("^[ ]*[^\n()]+[ ]+[^\n()]+[::]*[a-zA-Z]+\([^;{]*\n[ ]*{", flags=re.MULTILINE)
  for  root, dirs,files in os.walk('C:\\Users\\Svyatoslav.Kovalev\\Documents\\avc_regex_test\\avc\\avc'):
      for file in files:
        try:
          if ".cpp" in file:
            pos = 0
            allfile = ""
            with open(root + "\\" + file, 'r',errors='ignore') as f:
              allfile = f.read()
              item = reobj.search(allfile, pos)
              while item != None:
                tmp = item[0]
                if "catch" in tmp or "switch" in tmp or "class" in tmp or "BOOST_SCOPE_EXIT" in tmp or "if" in tmp or "return" in tmp:
                  pos = item.end()
                  item = reobj.search(allfile, pos)
                  continue
                else:
                  fun_name = extract_function_name(item[0])
                  inserted = trace_at_begin(allfile, item, reobj,fun_name)
                  allfile = inserted[0]
                  pos = inserted[1]
                  inserted = trace_at_end(allfile, pos, fun_name)
                  allfile = inserted[0]
                  pos = inserted[1]
                  item = reobj.search(allfile, pos)
            with open(root + "\\" + file, 'w',errors='ignore') as f:
              f.write(allfile)
        except IOError as ioerror:
          print(ioerror.args)

if __name__=="__main__":
  add_trace()
