import os 
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import sys
import scipy as sp
import numpy as np
import tensorflow as tf

def LogNormal(x, u, s):
	p = 1.0 / x / s / np.sqrt(np.pi * 2)
	p /= np.exp((np.log(x) - u) ** 2 / 2 / (s ** 2))
	return p

def SelfExciting():
