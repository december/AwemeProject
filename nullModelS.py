import os 
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import sys
import scipy as sp
import numpy as np
import tensorflow as tf

alpha1 = 1e-11
alpha2 = 1e-10
alpha3 = 1e-13
total = 100000
threshold = 0.00001

def NullModelH(lbd, theta, b, t):
	return lbd / np.power(t, theta) + b

def NullModelS(lbd, theta, b, t):
	exp =  -1 * lbd * np.power(t, 1-theta) / (1 - theta) - b * t
	return np.exp(exp)

#Lambda: 0.002490702411067944
#Theta: 0.7280549135780887
#B: 0.0006135536130181019

