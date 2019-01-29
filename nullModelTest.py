import os 
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import sys
import scipy as sp
import numpy as np
import tensorflow as tf

alpha1 = 1e-13
alpha2 = 1e-10
total = 10000
threshold = 0.00001

def LogNormal(x, u, s):
	p = 1.0 / x / s / np.sqrt(np.pi * 2)
	p /= np.exp((np.log(x) - u) ** 2 / 2 / (s ** 2))
	return p

def LnStExpH(lbd, theta, t):
	return np.log(lbd) - theta * np.log(t)	

def LnStExpS(lbd, theta, t):
	return -1 * lbd * np.power(t, 1-theta) / (1 - theta)

def LnObj(cd, ncd, lbd, theta):
	obj = 0
	for item in cd:
		obj += LnStExpH(lbd, theta, item) * cd[item]
		obj += LnStExpS(lbd, theta, item) * cd[item]
	for item in ncd:
		obj += LnStExpS(lbd, theta, item) * ncd[item]
	return obj

def DlnhDlbd(lbd, theta, t):
	return 1.0 / lbd

def DlnhDtheta(lbd, theta, t):
	return -1 * np.log(t)

def DlnsDlbd(lbd, theta, t):
	return -1 * np.power(t, 1-theta) / (1 - theta)

def DlnsDtheta(lbd, theta, t):
	up = lbd * np.power(t, 1-theta) * (1 - (1 - theta) * np.log(t))
	down = -1 * (1 - theta) * (1 - theta)
	return up / down

def GradDes(cd, ncd, lbd, theta, lr1, lr2):
	gradlbd = 0
	gradtheta = 0
	for item in cd:
		gradlbd += DlnhDlbd(lbd, theta, item) * cd[item] + DlnsDlbd(lbd, theta, item) * cd[item]
		gradtheta += DlnhDtheta(lbd, theta, item) * cd[item] + DlnsDtheta(lbd, theta, item) * cd[item]
	for item in ncd:
		gradlbd += DlnsDlbd(lbd, theta, item) * ncd[item]
		gradtheta += DlnsDtheta(lbd, theta, item) * ncd[item]
	newlbd = lbd + gradlbd * lr1
	newtheta = theta + gradtheta * lr2
	return newlbd, newtheta

fr = open('../../../Bytedance/Data/aweme_churn_iet_50to100.text', 'r')
data = fr.readlines()
fr.close()
fr = open('../../../Bytedance/Data/aweme_churn_iet_100to500.text', 'r')
data.extend(fr.readlines())
fr.close()
cdic = {}
ncdic = {}
n = len(data)
for i in range(n):
	temp = data[i][:-1].split('\t')
	if temp[1] != '3' or int(temp[2]) != 240:
		continue
	if temp[0] == '1':
		if cdic.has_key(int(temp[3])):
			cdic[int(temp[3])] += int(temp[4])
		else:
			cdic[int(temp[3])] = int(temp[4])
	else:
		if ncdic.has_key(int(temp[3])):
			ncdic[int(temp[3])] += int(temp[4])
		else:
			ncdic[int(temp[3])] = int(temp[4])
cnt = 0
lbd = 0.00024
theta = -0.65
lastObj = LnObj(cdic, ncdic, lbd, theta)
while cnt < total:
	lbd, theta = GradDes(cdic, ncdic, lbd, theta, alpha1, alpha2)
	newObj = LnObj(cdic, ncdic, lbd, theta)
	delta = newObj - lastObj
	print 'Step ' + str(cnt) + ': ' + str(newObj) + ' (' + str(delta) + ' increased)(' + str(lbd) + ' ' + str(theta) + ')'
	if delta <= threshold:
		break
	cnt += 1
	lastObj = newObj
print 'Lambda: ' + str(lbd)
print 'Theta: ' + str(theta)

