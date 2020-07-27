#!/usr/bin/python3

import os
import sys
import numpy as np

if len(sys.argv)<3:
    print("mp3split.py <mp3_file> <split_info_file>")
    sys.exit(0)

bigmp3 = sys.argv[1]
infofile = sys.argv[2]

info = np.genfromtxt(infofile, dtype=str)

for idx, (start, songname) in enumerate(info):
    if idx==len(info)-1:
        cmd = "ffmpeg -i \"{}\" -acodec copy -ss {} \"{}.mp3\"".format(bigmp3, start, songname)
    else:
        stop = info[idx+1][0]
        cmd = "ffmpeg -i \"{}\" -acodec copy -ss {} -to {} \"{}.mp3\"".format(bigmp3, start, stop, songname)
    print(cmd)
    os.system(cmd)

