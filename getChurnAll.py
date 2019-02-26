import sys
import numpy as np
import matplotlib as plt
import datetime

def WriteIt(info):
	#if info[3] == 10:
	#	return True
	#return False
	return True

#统计每个用户每段状态不变的持续时间和流失情况，用于训练累加模型、累乘模型和Social-Content Mixture Model
suffix = 'train_half'
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
	#记录四种不同类型边的数量，作为当前的状态
	info = temp[2] + '\t' + temp[3] + '\t' + temp[4] + '\t' + temp[5]
	if lastid != temp[0]:
		if curtime != 0 and lastinfo != '' and lastid != '' and WriteIt(lastinfo):
			if not ncdlist.has_key(lastinfo):
				ncdlist[lastinfo] = {}
			if ncdlist[lastinfo].has_key(curtime):
				ncdlist[lastinfo][curtime] += 1
			else:
				ncdlist[lastinfo][curtime] = 1
		lastid = temp[0]
		lastinfo = info
		curtime = int(temp[1])
	else:
		#状态不变则加上登录的时间间隔
		if lastinfo == info:
			curtime += int(temp[1])
		#状态发生变化，则从下一次登录开始重新计算
		else:
			if curtime != 0 and lastinfo != '' and lastid != '' and WriteIt(lastinfo):
				if not ncdlist.has_key(lastinfo):
					ncdlist[lastinfo] = {}
				if ncdlist[lastinfo].has_key(curtime):
					ncdlist[lastinfo][curtime] += 1
				else:
					ncdlist[lastinfo][curtime] = 1
			lastinfo = info
			curtime = int(temp[1])
	if temp[7] == 'True':
		if curtime != 0 and lastinfo != '' and lastid != '' and WriteIt(lastinfo):
			if not cdlist.has_key(lastinfo):
				cdlist[lastinfo] = {}
			if cdlist[lastinfo].has_key(curtime):
				cdlist[lastinfo][curtime] += 1
			else:
				cdlist[lastinfo][curtime] = 1
		lastid = ''
		lastinfo = ''
		curtime = 0

#输出统计结果
fw = open('../../dataset/aweme/aweme_status_iet_'+suffix+'.text', 'w')
keys = sorted(cdlist.keys())
for k in keys:
	newkeys = sorted(cdlist[k].keys())
	for nk in newkeys:
		fw.write('1\t'+str(k)+'\t'+str(nk)+'\t'+str(cdlist[k][nk])+'\n') #whether churn, social_fol, content_fol, social_fan, content_fan, time, popularity
keys = sorted(ncdlist.keys())
for k in keys:
	newkeys = sorted(ncdlist[k].keys())
	for nk in newkeys:
		fw.write('0\t'+str(k)+'\t'+str(nk)+'\t'+str(ncdlist[k][nk])+'\n') #whether churn, social_fol, content_fol, social_fan, content_fan, time, popularity
fw.close()

print('Finished writing part.')

