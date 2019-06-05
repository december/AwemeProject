import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np

#cluster = [290985616, 87370202, 21839778, 1785307, 6191603, 413330, 1111, 860174, 11157, 14]
cluster = [379574095, 4736376, 1312471, 672697, 12295315, 115352, 12566, 4772838, 1542, 412]
x = list()
y = list()
for i in range(10):
    x.append([])
    y.append([])

fr = open('../../../Bytedance/Data/retention_delta_cluster.csv', 'r')    
info = fr.readlines()
n = len(info)
for i in range(n):
    temp = info[i].split(',')
    if temp[0] == 'None':
        continue
    tp = int(temp[1])
    days = int(temp[0])
    num = int(temp[2])
    if days < 0:
        continue
    if days == 0:
        cluster[tp] = num
    x[tp].append(days)
    y[tp].append(num * 1.0 / cluster[tp])
#print(y[1])

x = np.array(x)
y = np.array(y)
plt.xlabel('Days', fontsize=14)
plt.ylabel('Retention rate', fontsize=18)
plt.xlim(xmax=400)
plt.ylim(ymax=0.6)
plt.xticks(fontsize=14)
plt.yticks(fontsize=18)
plt.grid()
plt.plot(x[1], y[1], ':', color='r', label='Low Ratio', linewidth=5)
plt.plot(x[4], y[4], color='g', label='Middle Ratio', linewidth=5)
plt.plot(x[7], y[7], '--', color='b', label='High Ratio', linewidth=5)
plt.legend(fontsize=20)
#plt.xlim(0, 10)
#plt.ylim(1e-8, 1)
#plt.xscale('log')
#plt.yscale('log')
plt.savefig('retention_fan.png')
