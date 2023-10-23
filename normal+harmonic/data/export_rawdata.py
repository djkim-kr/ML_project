import os 
import subprocess

with open("h2o.c1.freq24.int.log", "r") as f:
    lines = f.readlines()

    msg1 = os.popen("cat h2o.c1.freq24.int.log | grep -A 4 '^ ATOM'").read()
    msg2 = os.popen("cat h2o.c1.freq24.int.log | grep -A 22 '  CARTESIAN'").read()
    msg3 = os.popen("cat h2o.c1.freq24.int.log | grep -i -A 12 frequency").read()

    # msg1 = subprocess.run("grep -A 4 '^ ATOM' h2o.sp.min.reoriented.OHalongX.log", shell=True, capture_output=True, text=True).stdout
    # msg2 = subprocess.run("grep -A 22 '  CARTESIAN' h2o.sp.min.reoriented.OHalongX.log", shell=True, capture_output=True, text=True).stdout
    # msg3 = subprocess.run("grep -i -A 28 frequency h2o.sp.min.reoriented.OHalongX.log | grep -A 12 20.18", shell=True, capture_output=True, text=True).stdout

    msg = msg1 + msg3 + msg2
    print(msg)





