import subprocess
from matplotlib import pyplot as plt

fig = plt.figure()

x = []
y = []
for k in range(2,50):
    x.append(k)
    cmd = "python mondrian.py " + str(k)
    proc = subprocess.Popen(cmd,-1,stdout=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    y.append(float(out.strip()))
save_name = "mondrian k-Loss figure"
plt.plot(x,y)
plt.savefig(save_name)