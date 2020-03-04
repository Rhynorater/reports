import re
import sys
import subprocess
import random
import os
devnull = open("/dev/null", "w")

###
#Usage: python report.py template [arguments]
###


def runPipeSubprocess(cmd):
    commands = cmd.split("|")
    ps = None
    for command in commands:
        print command
        command = command.strip()
        if ps:
            ps = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stdin=ps.stdout)
        else:
            ps = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
    return ps.communicate()[0]

template = sys.argv[1]
args = sys.argv[2:]

lt = open(template).read()

for i in range(0, len(args)):
    lt = lt.replace("$"+str(i), args[i])

commands = re.findall("(\{\$(.+)\})", lt)
for rcmd,cmd in commands:
    cmd = cmd.strip()
    result = runPipeSubprocess(cmd)
    lt = lt.replace(rcmd, result)

ofn ="/tmp/"+str(random.randint(0,10000000))+"-report.md" 
of = open(ofn, "w")
of.write(lt)
of.close()
os.system("xdg-open "+ofn)

