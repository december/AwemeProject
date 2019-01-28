import sys
import numpy as np
import matplotlib as plt
import datetime

def WriteIt(info):
	#if info[3] == 10:
	#	return True
	#return False
	return True

suffix = 'train'
fr = open('/home/windxrz/toutiao/baseline/sample/sample_'+suffix+'.csv', 'r')
data = fr.readlines()
#data.sort()
fr.close()
cdlist = {}
ncdlist = {}
lastid = ''
lastinfo = ''
curtime = 0
n = len(data)
for i in range(1, n):
	temp = data[i][:-1].split('\t')
	time = int(temp[-2])
	if temp[7] == 'True':
		if cdlist.has_key(time):
			cdlist[time] += 1
		else:
			cdlist[time] = 1
		continue
	if i == n - 1 or temp[0] != data[i+1][:-1].split('\t')[0]:
		if ncdlist.has_key(time):
			ncdlist[time] += 1
		else:
			ncdlist[time] = 1
	
fw = open('../../dataset/aweme/aweme_whole_iet_'+suffix+'.text', 'w')
keys = sorted(cdlist.keys())
for k in keys:
	fw.write('1\t'+str(k)+'\t'+str(cdlist[k])+'\n') #whether churn, time, popularity
keys = sorted(ncdlist.keys())
for k in keys:
	fw.write('0\t'+str(k)+'\t'+str(ncdlist[k])+'\n') #whether churn, time, popularity
fw.close()

print('Finished writing part.')

