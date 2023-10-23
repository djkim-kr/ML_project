# Notice
This directory is for energy difference calculation using 'normal' and 'harmonic' way

You need a proper data for both way, which should include informations about hessian matrix and displacement vectors.
For example, in 'data' directory, you can find 'h2o.c1.freq.24.int.log' which has those informations. 
and by using 'export_rawdata.py', you can extract proper informations for calculation. 

python3 export_rawdata.py > raw.c1.int.log

! For 'normal' way, we additionally need the data for interpolation. 
In this case, wm_(1,2,3)_0.1.xyz are those.

# test_normal+har.py
will automatically gets infomation from 'data' folder and conduct the calculation using interpolation and hessian matrix. 
You will get 'nor_{}.xyz' , 'har_{}.xyz' as a result. Once you have the output files, you can conduct ML process using files in 'scipts' folder

! You need proper data in proper format in 'data' folder so that it can be conducted successfully. 

if you only want to conduct the calculation in 'normal' way, use 'test_normalmode.py

For plotting, use _plot.py

# test_rancoeff_generate.py
You can generate your own molecule structures with random coefficients to each vibration mode displacement vectors.
