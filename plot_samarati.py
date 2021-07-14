import os
import numpy
import subprocess
from matplotlib import pyplot as plt

fig = plt.figure()

x = []
y = []
z = []
# for k in range(5,6):
#     y = []
#     z = []
#     for maxsup in range(5,40,5):
#         y.append(maxsup)
#         cmd = "python samarati.py " + str(k) + " " + str(maxsup)
#         proc = subprocess.Popen(cmd,-1, stdout=subprocess.PIPE, shell=True)
#         out, err = proc.communicate()
#         z.append(float(out.strip()))
#         plt.subplot(10,1,(10 * (k - 5) + maxsup / 5))
#         plt.plot(y,z)
for k in range(2,16):
    y = []
    z = []
    for maxsup in range(5,100,5):
        y.append(maxsup)
        cmd = "python samarati.py " + str(k) + " " + str(maxsup)
        proc = subprocess.Popen(cmd,-1, stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        z.append(float(out.strip()))
    save_name = "plt" + str(k) + "anonimity" + ".jpg"
    plt.clf()
    plt.plot(y,z)
    plt.savefig(save_name)
