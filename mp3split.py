#!/usr/bin/python3

import os
import sys
import numpy as np
import getopt

opts, args = getopt.getopt(sys.argv[1:], 'hXa:l:y:')

helpmsg = """mp3split.py [-hX] <options>  <mp3_file> <split_info_file>
-h  Display this message.
-X  Just print the commands without executing them.
<options> will be forwarded as is to mp3info. See the mp3info man page for more options."""
if len(args)<2:
    print(helpmsg)
    sys.exit(0)

bigmp3 = args[0]
infofile = args[1]

noexec = False

id3_opts = ""
for o,a in opts:
    if o=='-h':
        print(helpmsg)
        sys.exit(0)
    elif o=='-X':
        noexec = True
    else:
        id3_opts += " {} \"{}\"".format(o,a)

info = np.genfromtxt(infofile, dtype=str, delimiter=',')


for idx, (start, songname) in enumerate(info):
    smallmp3 = "\"{}.mp3\"".format(songname)
    if idx==len(info)-1:
        cmd = "ffmpeg -i \"{}\" -acodec copy -ss {} {} ".format(bigmp3, start, smallmp3)
    else:
        stop = info[idx+1][0]
        cmd = "ffmpeg -i \"{}\" -acodec copy -ss {} -to {} \"{}.mp3\" ".format(bigmp3, start, stop, songname)
    print(cmd)
    if not noexec:
        os.system(cmd)

    if len(id3_opts)>0:
        id3_cmd = "mp3info " + id3_opts + " -n {} -t \"{}\" ".format(idx+1, songname) + smallmp3
        print(id3_cmd)
        if not noexec:
            os.system(id3_cmd)

