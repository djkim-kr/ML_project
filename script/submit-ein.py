#!/usr/bin python3

import glob
import os
import subprocess

for paramdir in sorted(glob.glob("???_size_????")):
    runscripts = [os.path.join(paramdir, "quip_run.sh")]

    if runscripts:
        subprocess.run(["chain_submit.py"] + runscripts)

print('run script is all excuted ')
