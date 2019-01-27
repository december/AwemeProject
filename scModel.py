import os 
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import sys
import scipy as sp
import numpy as np
import tensorflow as tf

alpha = [1e-11, 1e-11, 1e-11, 1e-11, 1e-11, 1e-11, 1e-11] 
total = 10000
threshold = 0.0001

def LogNormal(x, u, s):
	p = 1.0 / x / s / np.sqrt(np.pi * 2)
	p /= np.exp((np.log(x) - u) ** 2 / 2 / (s ** 2))
	return p

def Gx(k, x):
	return (np.power(x[0], k[0]) + np.power(x[1], k[1])) * (np.power(x[2], k[2]) + np.power(x[3], k[3]))

def LnScModelH(a, b, theta, k, x, t):
	result = Gx(k, x)
	return np.log(a * result / np.power(t, theta) + b)

def LnScModelS(a, b, theta, k, x, t):
	result = Gx(k, x)
	exponent = -1 * a * result * np.power(t, 1 - theta) / (1 - theta) - b * t
	return exponent

def LnObj(cd, ncd, lbd, theta):
	obj = 0
	for item in cd:
		obj += LnScModelH(lbd, theta, item) * cd[item]
		obj += LnScModelS(lbd, theta, item) * cd[item]
	for item in ncd:
		obj += LnScModelS(lbd, theta, item) * ncd[item]
	return obj

def DlnhDa(a, b, theta, k, x, t):
	result = Gx(k, x)
	return result / (a * result + np.power(t, theta) * b)

def DlnhDb(a, b, theta, k, x, t):
	result = Gx(k, x)
	return np.power(t, theta) / (a * result + b * np.power(t, theta))

def DlnhDk(a, b, theta, k, x, t):
	result = list()
	for i in range(4):
		s = a / np.power(t, theta)
		up = s * np.power(x[i], k[i]) * np.log(x[i])
		if i > 1:
			s *= (np.power(x[0], k[0]) + np.power(x[1], k[1]))
			down = s * (np.power(x[2], k[2]) + np.power(x[3], k[3])) + b
		else:
			s *= (np.power(x[2], k[2]) + np.power(x[3], k[3]))
			down = s * (np.power(x[0], k[0]) + np.power(x[1], k[1])) + b
		result.append(up / down)
	return result

def DlnhDtheta(a, b, theta, k, x, t):
	result = Gx(k, x)
	return -1 * a * result * np.log(t) / (a * r + b * np.power(t, theta))

def DlnsDa(a, b, theta, k, x, t):
	result = Gx(k, x)
	return -1 * result * np.power(t, 1 - theta) / (1 - theta)

def DlnsDb(a, b, theta, k, x, t):
	return -1 * t

def DlnsDk(a, b, theta, k, x, t):
	result = list()
	for i in range(4):
		s = a * np.power(t, 1 - theta) / (1 - theta)
		if i > 1:
			s *= (np.power(x[0], k[0]) + np.power(x[1], k[1]))
		else:
			s *= (np.power(x[2], k[2]) + np.power(x[3], k[3]))
		result.append(-1 * s * np.power(x[i], k[i]) * np.log(x[i]))
	return result

def DlnsDtheta(a, b, theta, k, x, t):
	result = Gx(k, x)
	r1 = a * result * np.power(t, 1 - theta) * np.log(t) / (1 - theta)
	r2 = a * result * np.power(t, 1 - theta) / (1 - theta) / (1 - theta)
	return r1 - r2

def GradDes(cd, ncd, p, lr):
	grad = list()
	for i in range(7):
		grad.append(0) #a, b, theta, k1, k2, k3, k4
	for item in cd:
		grad[0] += DlnhDa(p[0], p[1], p[2], p[3:])

		grad[0] += DhDlbd(lbd) * cd[item] + DsDlbd(theta, item) * cd[item]
		gradtheta += DhDtheta(item) * cd[item] + DsDtheta(lbd, theta, item) * cd[item]
	for item in ncd:
		gradlbd += DsDlbd(theta, item) * ncd[item]
		gradtheta += DsDtheta(lbd, theta, item) * ncd[item]
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
	if temp[1] != '3' or int(temp[2]) != 100:
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
lbd = 0.0002
theta = 0.6
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

