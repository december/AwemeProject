import os 
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import sys
import scipy as sp
import numpy as np
import tensorflow as tf

def Gx(k, x):
	return np.power(x[0], k[0]) + np.power(x[1], k[1]) + np.power(x[2], k[2]) + np.power(x[3], k[3])

def ScModelH(a, b, theta, k, x, t):
	result = Gx(k, x)
	lbd = a * result / np.power(t, theta) + b
	if lbd <= 0:
		print lbd
		print str(a) + ' ' + str(result) + ' ' + str(np.power(t, theta)) + ' ' + str(b)
	return a * result / np.power(t, theta) + b

def ScModelS(a, b, theta, k, x, t):
	result = Gx(k, x)
	exponent = -1 * a * result * np.power(t, 1 - theta) / (1 - theta) - b * t
	return np.exp(exponent)

# A: 0.0012115077635310397
# B: 0.00030893494535618414
# Theta: 0.0885776605879018
# K1: -0.664604554378142
# K2: -0.8717329487084687
# K3: -1.214133479923143
# K4: -2.7769966202842813
