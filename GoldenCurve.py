import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import seaborn as sns
sns.set()
sns.set_style('white')

#真实数据中边数对应的取得最低流失率的social ratio
totalfan = [10, 15, 20, 24, 30, 34, 40, 45, 50]
ratiofan = [9.0/13, 13.0/17, 17.0/22, 19.0/24, 25.0/30, 27.0/32, 35.0/40, 39.0/46, 43.0/50]

totalfol = [10, 15, 20, 24, 30, 34, 40, 45, 50]
ratiofol = [0.5, 7.0/13, 8.0/13, 16.0/25, 20.0/30, 25.0/35, 28.0/40, 33.0/48, 37.0/52]

#根据学习出来的参数计算曲线
#k = [-0.22245946650594897, -1.4060611697500127]
k = [-0.5461767532082837, -2.968440144320875]
#k = [-0.1252557667896992, -1.5249187807474907]
#k = [-0.1877745162465406, -1.635660504854519]

#比较hazard function对不同类型边数量的偏导数的绝对值大小，决定当前状态下哪种边对降低流失更有用
def balanced(x):
	d = k[0] * np.power(x, k[0] - 1) / k[1]
	#print d
	return np.power(d, 1.0 / (k[1] - 1))

#根据模型计算边数一定的情况下流失率最低的social ratio
def best(r, n):
	return k[0] * np.power(r, k[0] - 1) * np.power(n, k[0] - 1) - k[1] * np.power(1 - r, k[1] - 1) * np.power(n, k[1] - 1)

#画图对比模型得出的流失率最低的social ratio与真实数据中的统计结果
x = list()
y = list()
for i in range(30):
	x.append(2 * i + 1)
	y.append(balanced(2 * i + 1))

x = list()
y = list()
for i in range(10, 51):
	x.append(i)
	flag = False
	rate = 0.001
	while rate < 1:
		d = best(rate, i)
		if d == 0:
			y.append(rate)
			flag = True
			break
		if d > 0:
			y.append(rate-0.001)
			flag = True
			break
		rate += 0.001
	if not flag:
		y.append(1.0)

x = np.array(x)
y = np.array(y)
t = np.array(totalfan)
r = np.array(ratiofan)
plt.xlabel('Total number of inward links', fontsize=15)
plt.ylabel('Social-content ratio', fontsize=15)
#plt.xlim(xmax=500)
#plt.ylim(ymax=0.6)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('Balance Curve for Inward Links', fontsize=25)
plt.scatter(t, r, marker='o', c='', s=200, edgecolors='k', label='Ratio with the lowest churn rate', linewidth=2.5)
plt.plot(x, y, '-', c='b', label='Balance curve from SCM', linewidth=5)
plt.legend(fontsize=16)
#plt.xlim(0, 10)
#plt.ylim(1e-8, 1)
#plt.xscale('log')
#plt.yscale('log')
plt.savefig('balance_fan.eps', dpi=1200)

