import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

userdic = {}
prefix = '../../../Bytedance/Data/'
suffix = '.text'
filename = 'aweme_fans_rate_day_6'
fr = open(prefix+filename+suffix, 'r')
data = fr.readlines()
data.sort()
n = len(data)
last_total = 0
last_social = 0
for i in range(n):
	temp = data[i].split('\t')
	if not userdic.has_key(temp[0]):
		last_total = int(temp[2])
		last_social = int(temp[3])
		userdic[temp[0]] = {}
		userdic[temp[0]][temp[1]] = last_social * 1.0 / last_total
	else:
		last_total += int(temp[2])
		last_social += int(temp[3])
		userdic[temp[0]][temp[1]] = last_social * 1.0 / last_total
cnt = 0
for k in userdic:
	if cnt > 1000:
		break
	x = list()
	y = list()
	keylist = sorted(userdic[k].keys())
	start = datetime.datetime.strptime(keylist[0], '%Y%m%d')
	for key in keylist:
		current = datetime.datetime.strptime(key, '%Y%m%d')
		x.append((current-start).days)
		y.append(userdic[k][key])
	x = np.array(x)
	y = np.array(y)
	#print x
	#print y
	plt.xlabel('Days')
	plt.ylabel('Social Ratio')
	plt.title(keylist[0])
	plt.grid()
	plt.plot(x, y, marker='.')
	plt.savefig('../../../Bytedance/Figs/daily_dynamics/fans_6/'+k+'.png')
	plt.cla()
	cnt += 1