import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os
sns.set()
sns.set_style('white')
from scipy import optimize

#生成一条直线
def f_1(x, A, B):
    return A*x + B

#各种类型边的数量与null model参数的对应关系
#social follows
x4 = [1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 45, 60]
y4 = [0.000893, 0.00058, 0.000417, 0.00033, 0.0002526, 0.0002281, 0.0001783, 0.0001378, 0.0001, 0.00007654, 0.000060748, 0.0000512545]

#content follows
x1 = [1, 3, 5, 10, 20, 30, 50, 80, 120, 220, 340, 520]
y1 = [0.001277, 0.00051, 0.000314, 0.0000877, 0.0000787, 0.0000622, 0.0001, 0.0000705, 0.0000446756, 0.00002, 0.0000174, 0.00001063]

#social fans
x2 = [1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 45, 60]
y2 = [0.000858, 0.00051536, 0.000378559, 0.0003, 0.00025, 0.00019, 0.000147, 0.0001, 0.0000915, 0.000085, 0.000054, 0.0000445]

#content fans
x3 = [1, 2, 3, 5, 7, 10, 20, 30, 40, 80, 120, 160]
y3 = [0.000374, 0.000195, 0.000112, 0.000153, 0.000098543, 0.00008, 0.0000866, 0.00007091, 0.000072554, 0.000064, 0.0000291, 0.000028]

logx1 = [np.log(k) for k in x1]
logy1 = [np.log(k) for k in y1]

logx2 = [np.log(k) for k in x2]
logy2 = [np.log(k) for k in y2]

logx3 = [np.log(k) for k in x3]
logy3 = [np.log(k) for k in y3]

logx4 = [np.log(k) for k in x4]
logy4 = [np.log(k) for k in y4]

#使用直线模型进行fit
A1, B1 = optimize.curve_fit(f_1, logx1, logy1)[0]
n1 = np.arange(0, max(logx1), 0.01)
m1 = A1 * n1 + B1
n1 = [np.exp(k) for k in n1]
m1 = [np.exp(k) for k in m1]

#画图观察fit效果
plt.xlabel('Content Outward Links', fontsize=12)
plt.ylabel('c', fontsize=16)
plt.xscale('log')
plt.yscale('log')
#plt.grid()
plt.xticks(fontsize=12)
plt.yticks(fontsize=16)
plt.scatter(x1, y1, marker='o', c='', s=200, edgecolors='k', label='Value of c', linewidth=2.5)
plt.plot(n1, m1, '--', c='b', label='Power-law fit', linewidth=5)
plt.legend(fontsize=24)
plt.savefig('content_fol.eps', dpi=1200)



