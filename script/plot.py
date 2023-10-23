#!/usr/bin python3

import glob
import os
import subprocess

for paramdir in sorted(glob.glob("???_size_????")):
    if (os.path.exists(os.path.join(paramdir, "quip_train.xyz")) 
        and os.path.exists(os.path.join(paramdir, "quip_valid.xyz"))
        and os.path.exists(os.path.join(paramdir, "quip_test.xyz"))):
            
        plot_gap_path = os.path.join(paramdir,'plot_gap.py')
        if os.path.exists(plot_gap_path):
            subprocess.run(["python3" , 'plot_gap.py'], cwd=paramdir)

print('plot_gap.py is all excuted ')