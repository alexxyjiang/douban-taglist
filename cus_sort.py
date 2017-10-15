import sys

count   = 0
dict_a  = {}
dict_b  = {}
for line in open("./douban.md"):
  if line.startswith("*"):
    count += 1
    key   = line.strip("\n")[2:]
    dict_a[key]   = count
    dict_b[count] = key

for line in sys.stdin:
  items   = line.strip("\n").split(" ")
  s_items = sorted([dict_a[i] for i in items])
  print " ".join([dict_b[i] for i in s_items])
