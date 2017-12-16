import sys
d = {}
for line in sys.stdin:
  key = line.strip("\n")
  if key != "" and key in d:
    continue
  d[key]  = 1
  print(key)
