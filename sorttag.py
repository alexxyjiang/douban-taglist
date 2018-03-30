import sys
import libdtag

def main():
  dtdict = libdtag.DoubanTagDict()
  for line in open("./douban.md"):
    if line.startswith("*"):
      name = line.strip("\n")[2:]
      dtdict.add(name)
  for line in sys.stdin:
    names = line.strip("\n").split(" ")
    dtags = [dtdict.seek(name) for name in names if dtdict.seek(name) != None]
    dtags.sort()
    print(' '.join([str(tag) for tag in dtags]))

if __name__ == '__main__':
  main()
