import os 
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import sys
import scipy as sp
import numpy as np
import tensorflow as tf

alpha1 = 2e-10
alpha2 = 2e-8
alpha3 = 2e-10
total = 100000
threshold = 0.00001

def LogNormal(x, u, s):
	p = 1.0 / x / s / np.sqrt(np.pi * 2)
	p /= np.exp((np.log(x) - u) ** 2 / 2 / (s ** 2))
	return p

#Null Model的log形式的hazard function
def LnStExpH(lbd, theta, b, t):
	return np.log(lbd / np.power(t, theta) + b)

#Null Model的log形式的survival function
def LnStExpS(lbd, theta, b, t):
	return -1 * lbd * np.power(t, 1-theta) / (1 - theta) - b * t

#log形式的目标函数，目标函数为最大似然估计
def LnObj(cd, ncd, lbd, theta, b):
	obj = 0
	for item in cd:
		obj += LnStExpH(lbd, theta, b, item) * cd[item]
		obj += LnStExpS(lbd, theta, b, item) * cd[item]
	for item in ncd:
		obj += LnStExpS(lbd, theta, b, item) * ncd[item]
	return obj

#log形式的hazard function对lambda的偏导
def DlnhDlbd(lbd, theta, b, t):
	return 1.0 / (lbd + b * np.power(t, theta))

#log形式的hazard function对theta的偏导
def DlnhDtheta(lbd, theta, b, t):
	return -1 * np.log(t) * lbd / (lbd + b * np.power(t, theta))

#log形式的hazard function对b的偏导
def DlnhDb(lbd, theta, b, t):
	return 1 / (b + lbd * np.power(t, -1 * theta))

#log形式的survival function对lambda的偏导
def DlnsDlbd(lbd, theta, b, t):
	return -1 * np.power(t, 1-theta) / (1 - theta)

#log形式的survival function对theta的偏导
def DlnsDtheta(lbd, theta, b, t):
	up = lbd * np.power(t, 1-theta) * (1 - (1 - theta) * np.log(t))
	down = -1 * (1 - theta) * (1 - theta)
	return up / down

#log形式的survival function对b的偏导
def DlnsDb(lbd, theta, b, t):
	return -1 * t

#使用梯度下降法对参数进行优化
def GradDes(cd, ncd, lbd, theta, b, lr1, lr2, lr3):
	gradlbd = 0
	gradtheta = 0
	gradb = 0
	for item in cd:
		gradlbd += DlnhDlbd(lbd, theta, b, item) * cd[item] + DlnsDlbd(lbd, theta, b, item) * cd[item]
		gradtheta += DlnhDtheta(lbd, theta, b, item) * cd[item] + DlnsDtheta(lbd, theta, b, item) * cd[item]
		gradb += DlnhDb(lbd, theta, b, item) * cd[item] + DlnsDb(lbd, theta, b, item) * cd[item]
	for item in ncd:
		gradlbd += DlnsDlbd(lbd, theta, b, item) * ncd[item]
		gradtheta += DlnsDtheta(lbd, theta, b, item) * ncd[item]
		gradb += DlnsDb(lbd, theta, b, item) * ncd[item]
	newlbd = lbd + gradlbd * lr1
	newtheta = theta + gradtheta * lr2
	newb = b + gradb * lr3
	return newlbd, newtheta, newb


fr = open('../../dataset/aweme/aweme_whole_iet_train_half.text', 'r')
data = fr.readlines()
fr.close()
#fr.close()
#fr = open('../../../Bytedance/Data/aweme_churn_iet_100to500.text', 'r')
#data.extend(fr.readlines())
#统计真实数据中流失的用户（使用概率密度函数）和未流失的用户（使用survival function）
cdic = {}
ncdic = {}
n = len(data)
for i in range(n):
	temp = data[i][:-1].split('\t')
	if temp[0] == '1':
		if cdic.has_key(int(temp[1])):
			cdic[int(temp[1])] += int(temp[2])
		else:
			cdic[int(temp[1])] = int(temp[2])
	else:
		if ncdic.has_key(int(temp[1])):
			ncdic[int(temp[1])] += int(temp[2])
		else:
			ncdic[int(temp[1])] = int(temp[2])
cnt = 0
#下面即为优化得到的一组理想参数
lbd = -0.0885247
theta = 0.0272774
b = 0.08951
lastObj = LnObj(cdic, ncdic, lbd, theta, b)
#迭代优化参数
while cnt < total:
	lbd, theta, b = GradDes(cdic, ncdic, lbd, theta, b, alpha1, alpha2, alpha3)
	newObj = LnObj(cdic, ncdic, lbd, theta, b)
	delta = newObj - lastObj
	print 'Step ' + str(cnt) + ': ' + str(newObj) + ' (' + str(delta) + ' increased)(' + str(lbd) + ' ' + str(theta) + ' ' + str(b) + ')'
	if delta <= threshold:
		break
	cnt += 1
	lastObj = newObj
print 'Lambda: ' + str(lbd)
print 'Theta: ' + str(theta)
print 'B: ' + str(b)

