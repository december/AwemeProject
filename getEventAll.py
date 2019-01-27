import sys
import numpy as np
import matplotlib as plt
import datetime

def WriteIt(info):
	#if info[3] == 10:
	#	return True
	#return False
	return True

suffix = 'sample'
fr = open('/home/windxrz/toutiao/baseline/cleaned_data/aweme_active_iet_'+suffix+'.csv', 'r')
data = fr.readlines()
#data.sort()
fr.close()

lendic = {} #id to length
statusdic = {} #id to time to status
churndic = {} #time to churn id to status
n = len(data)
for i in range(1, n):
	temp = data[i][:-1].split('\t')
	info = temp[2] + '\t' + temp[3] + '\t' + temp[4] + '\t' + temp[5]
	if lendic.has_key(temp[0]):
		lendic[temp[0]] = max(lendic[temp[0]], int(temp[8]))
	else:
		lendic[temp[0]] = int(temp[8])
	if not statusdic.has_key(temp[0]):
		statusdic[temp[0]] = {}
	statusdic[temp[0]][int(temp[9])] = info
	if temp[7] == 'True':
		if not churndic.has_key(int(temp[8])):
			churndic[int(temp[8])] = {}
		churndic[int(temp[8])][temp[0]] = info

itemlist = list()
times = sorted(churndic.keys())
for t in times:
	for k in churndic[t]:
		s = str(t) + '\t1\t' + churndic[t][k] + '\n' #time, whether churn, social_fol, content_fol, social_fan, content_fan
		itemlist.append(s)
	for item in statusdic:
		if lendic[item] < t:
			continue
		pos = t
		while pos >= 0:
			if statusdic[item].has_key(pos):
				s = str(t) + '\t0\t' + statusdic[item][pos] + '\n'
				itemlist.append(s)
				break
			pos -= 1

fw = open('../../dataset/aweme/aweme_status_event_'+suffix+'.text', 'w')
for item in itemlist:
	fw.write(item)
fw.close()

print('Finished writing part.')

