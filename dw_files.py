import os
import sys

f=sys.argv[1]
links=open(f,"r").read().split("\n")

for link in links:
    os.system("/usr/bin/wget  --load-cookies /home/daruis1/.urs_cookies --save-cookies /home/daruis1/.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition {0}".format(link))
