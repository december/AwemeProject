import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

ietdic = {}
fr = open('../../../data/aweme_active_day_100to500.text', 'r')
data = fr.readlines()
data.sort()
fr.close()
result = list()
n = len(data)
lastid = ''
for i in range(n-1):
	temp = data[i][:-1].split('\t')
	newtemp = data[i+1][:-1].split('\t')
	if newtemp[0] == temp[0]:
		before = datetime.datetime.strptime(temp[1], '%Y%m%d')
		after = datetime.datetime.strptime(newtemp[1], '%Y%m%d')
		ietdic[data[i][:-1]] = (after - before).days

fw = open('../../../data/aweme_active_iet_100to500.text', 'w')
sortkey = sorted(ietdic.keys())
for key in sortkey:
	fw.write(key+'\t'+str(ietdic[key])+'\n')
fw.close()
