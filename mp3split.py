#!/usr/bin/python3

import os
import sys
import numpy as np
import getopt

opts, args = getopt.getopt(sys.argv[1:], 'ha:l:y:')

helpmsg = "mp3split.py <mp3_file> <split_info_file>"
if len(args)<2:
    print(helpmsg)
    sys.exit(0)

bigmp3 = args[0]
infofile = args[1]

id3_opts = ""
for o,a in opts:
    if o=='-h':
        print(helpmsg)
        sys.exit(0)
    else:
        id3_opts += " {} \"{}\"".format(o,a)

print(id3_opts)


info = np.genfromtxt(infofile, dtype=str, delimiter=',')


for idx, (start, songname) in enumerate(info):
    smallmp3 = "\"{}.mp3\"".format(songname)
    if idx==len(info)-1:
        cmd = "ffmpeg -i \"{}\" -acodec copy -ss {} {} ".format(bigmp3, start, smallmp3)
    else:
        stop = info[idx+1][0]
        cmd = "ffmpeg -i \"{}\" -acodec copy -ss {} -to {} \"{}.mp3\" ".format(bigmp3, start, stop, songname)
    print(cmd)
    os.system(cmd)

    if len(id3_opts)>0:
        id3_cmd = "mp3info " + id3_opts + " -n {} ".format(idx+1) + smallmp3
        print(id3_cmd)
        os.system(id3_cmd)

