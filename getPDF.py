import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os
sns.set()
sns.set_style('white')

#对分布进行分bin
def GetBin(a, x, y):
	newx = list()
	newy = list()
	length = len(x)
	binnum = 1
	pos = 0
	s = 0
	tempy = 0
	tempx = 0
	tempz = 0
	while pos < length:
		s += a
		tempx = s - a / 2
		while x[pos] <= s:
			tempy += y[pos]
			tempz += 1
			pos += 1
			if pos >= length:
				break
		if tempy > 0:
			newx.append(tempx)
			newy.append(tempy / tempz)
		binnum += 1
		tempy = 0
		tempz = 0
	return newx, newy
'''
ourx = list()
oury = list()
fr = open('../../../Bytedance/Data/pdf_train_our_model.csv', 'r')    
info = fr.readlines()
fr.close()
n = len(info)
for i in range(1, n):
	temp = info[i].split(',')
	ourx.append(int(temp[0]))
	oury.append(float(temp[1]))
'''
#统计真实数据中的流失时间分布情况
gdx = list()
gdy = list()
fr = open('../../../Bytedance/Data/pdf_train_ground_truth.csv', 'r')    
info = fr.readlines()
fr.close()
n = len(info)
for i in range(1, n):
	temp = info[i].split(',')
	gdx.append(int(temp[0]))
	gdy.append(float(temp[1]))

#binrx, binry = GetBin(1000, realsize, realcum) 
#rs = np.array(binrx)
#rn = np.array(binry) * 1.0 / realsum

#gdx, gdy = GetBin(5, gdx, gdy)
#ourx, oury = GetBin(20, ourx, oury)

#plt.ylim(ymin=1e-5)
#plt.xlim(xmin=1000)
#画图观察真实数据中的流失时间在不同尺度下的分布
plt.xscale('log')
plt.yscale('log')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
#plt.xticks(fontsize=14)
#plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#plt.set_xticks([0, 20000, 40000, 60000, 80000])
#plt.yticks(fontsize=14)
plt.plot(gdx, gdy, 'b', label='Real', linewidth=2.5)
plt.grid()
#plt.plot(ourx, oury, 'b', label='SCM', linewidth=2.5)
#plt.plot(bs, bn, 'k', label='Poisson', linewidth=2.5)
plt.xlabel(u'Days', fontsize=14)
plt.ylabel(u'PDF', fontsize=14)
plt.title('PDF on a log scale', fontsize=25)
#plt.legend(fontsize=20);
plt.savefig('pdf_loglog.eps',dpi=1200)
plt.cla()