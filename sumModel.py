import os 
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import sys
import scipy as sp
import numpy as np
import tensorflow as tf

alpha = [5e-11, 1e-11, 5e-7, 5e-6, 5e-6, 5e-6, 5e-6]
total = 10000
threshold = 0.0001

#累加模型的分子部分
def Gx(k, x):
	return np.power(x[0], k[0]) + np.power(x[1], k[1]) + np.power(x[2], k[2]) + np.power(x[3], k[3])

#累加模型的log形式的hazard function
def LnScModelH(a, b, theta, k, x, t):
	result = Gx(k, x)
	lbd = a * result / np.power(t, theta) + b
	if lbd <= 0:
		print lbd
		print str(a) + ' ' + str(result) + ' ' + str(np.power(t, theta)) + ' ' + str(b)
	return np.log(a * result / np.power(t, theta) + b)

#累加模型的log形式的survival function
def LnScModelS(a, b, theta, k, x, t):
	result = Gx(k, x)
	exponent = -1 * a * result * np.power(t, 1 - theta) / (1 - theta) - b * t
	return exponent

#log形式的目标函数，目标函数为最大似然估计
def LnObj(cd, ncd, p):
	obj = 0
	for item in cd:
		x = item.split('\t')
		x = [(int(k) + 1) for k in x]
		for time in cd[item]:
			obj += LnScModelH(p[0], p[1], p[2], p[3:], x, time) * cd[item][time]
			obj += LnScModelS(p[0], p[1], p[2], p[3:], x, time) * cd[item][time]
	for item in ncd:
		x = item.split('\t')
		x = [(int(k) + 1) for k in x]
		for time in ncd[item]:
			obj += LnScModelS(p[0], p[1], p[2], p[3:], x, time) * ncd[item][time]
	return obj

#log形式的hazard function对a的偏导
def DlnhDa(a, b, theta, k, x, t):
	result = Gx(k, x)
	return result / (a * result + np.power(t, theta) * b)

#log形式的hazard function对b的偏导
def DlnhDb(a, b, theta, k, x, t):
	result = Gx(k, x)
	return np.power(t, theta) / (a * result + b * np.power(t, theta))

#log形式的hazard function对k的偏导
def DlnhDk(a, b, theta, k, x, t):
	result = list()
	total = sum(x)
	for i in range(4):
		up = a * np.power(x[i], k[i]) * np.log(x[i])
		down = a * total + b * np.power(t, theta)
		result.append(up / down)
	return result

#log形式的hazard function对thetha的偏导
def DlnhDtheta(a, b, theta, k, x, t):
	result = Gx(k, x)
	return -1 * a * result * np.log(t) / (a * result + b * np.power(t, theta))

#log形式的survival function对a的偏导
def DlnsDa(a, b, theta, k, x, t):
	result = Gx(k, x)
	return -1 * result * np.power(t, 1 - theta) / (1 - theta)

#log形式的survival function对b的偏导
def DlnsDb(a, b, theta, k, x, t):
	return -1 * t

#log形式的survival function对k的偏导
def DlnsDk(a, b, theta, k, x, t):
	result = list()
	for i in range(4):
		s = a * np.power(x[i], k[i]) * np.power(t, 1-theta) * np.log(x[i])
		result.append(s / (theta - 1))
	return result

#log形式的survival function对theta的偏导
def DlnsDtheta(a, b, theta, k, x, t):
	result = Gx(k, x)
	r1 = a * result * np.power(t, 1 - theta) * np.log(t) / (1 - theta)
	r2 = a * result * np.power(t, 1 - theta) / (1 - theta) / (1 - theta)
	return r1 - r2

#使用梯度下降法对参数进行优化
def GradDes(cd, ncd, p, lr):
	grad = list()
	newp = list()
	for i in range(7):
		grad.append(0) #a, b, theta, k1, k2, k3, k4
		newp.append(p[i])
	for item in cd:
		x = item.split('\t')
		x = [(int(k) + 1) for k in x]
		for time in cd[item]:
			grad[0] += (DlnhDa(p[0], p[1], p[2], p[3:], x, time) + DlnsDa(p[0], p[1], p[2], p[3:], x, time)) * cd[item][time]
			grad[1] += (DlnhDb(p[0], p[1], p[2], p[3:], x, time) + DlnsDb(p[0], p[1], p[2], p[3:], x, time)) * cd[item][time]
			grad[2] += (DlnhDtheta(p[0], p[1], p[2], p[3:], x, time) + DlnsDtheta(p[0], p[1], p[2], p[3:], x, time)) * cd[item][time]
			resulth = DlnhDk(p[0], p[1], p[2], p[3:], x, time)
			results = DlnsDk(p[0], p[1], p[2], p[3:], x, time)
			for i in range(3, 7):
				grad[i] += (resulth[i-3] + results[i-3]) * cd[item][time]

	for item in ncd:
		x = item.split('\t')
		x = [(int(k) + 1) for k in x]
		for time in ncd[item]:
			grad[0] += DlnsDa(p[0], p[1], p[2], p[3:], x, time) * ncd[item][time]
			grad[1] += DlnsDb(p[0], p[1], p[2], p[3:], x, time) * ncd[item][time]
			grad[2] += DlnsDtheta(p[0], p[1], p[2], p[3:], x, time) * ncd[item][time]
			result = DlnsDk(p[0], p[1], p[2], p[3:], x, time)
			for i in range(3, 7):
				grad[i] += result[i-3] * ncd[item][time]

	#grad[0] += 1.0 / p[0]
	#grad[1] += 1.0 / p[1]
	for i in range(7):
		newp[i] += grad[i] * lr[i]
	return newp

'''
fr = open('../../dataset/aweme/aweme_status_iet_50to100.text', 'r')
data = fr.readlines()
fr.close()
fr = open('../../dataset/aweme/aweme_status_iet_100to500.text', 'r')
data.extend(fr.readlines())
fr.close()
'''
fr = open('../../dataset/aweme/aweme_status_iet_train_half.text', 'r')
data = fr.readlines()
fr.close()
#统计真实数据中流失的用户（使用概率密度函数）和未流失的用户（使用survival function）
cdic = {} #info to time to popularity
ncdic = {} #info to time to popularity
n = len(data)
for i in range(n):
	temp = data[i][:-1].split('\t')
	info = temp[1] + '\t' + temp[2] + '\t' + temp[3] + '\t' + temp[4]
	if temp[0] == '1':
		if not cdic.has_key(info):
			cdic[info] = {}
		if cdic[info].has_key(int(temp[5])):
			cdic[info][int(temp[5])] += int(temp[6])
		else:
			cdic[info][int(temp[5])] = int(temp[6])
	else:
		if not ncdic.has_key(info):
			ncdic[info] = {}
		if ncdic[info].has_key(int(temp[5])):
			ncdic[info][int(temp[5])] += int(temp[6])
		else:
			ncdic[info][int(temp[5])] = int(temp[6])		

cnt = 0
#下面即为优化得到的一组理想参数
p = [0.0006918450936869507, 0.0002696139131102916, -0.05516546747161913, -2.5598930328475156, -2.129070594433223, -2.58587634308447, -2.462745716163459] #a, b, theta, k1, k2, k3, k4
lastObj = LnObj(cdic, ncdic, p)
#迭代优化参数
while cnt < total:
	p = GradDes(cdic, ncdic, p, alpha)
	newObj = LnObj(cdic, ncdic, p)
	delta = newObj - lastObj
	s = ''
	for i in range(7):
		s += str(p[i]) + '\t'
	print 'Step ' + str(cnt) + ': ' + str(newObj) + ' (' + str(delta) + ' increased)'
	print s
	if delta <= threshold:
		break
	cnt += 1
	lastObj = newObj
print 'a: ' + str(p[0])
print 'b: ' + str(p[1])
print 'theta: ' + str(p[2])
print 'k1: ' + str(p[3])
print 'k2: ' + str(p[4])
print 'k3: ' + str(p[5])
print 'k4: ' + str(p[6])
