import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

suffix = '100to500'

ietdic = {}
fr = open('../../../data/aweme_active_day_'+suffix+'.text', 'r')
data = fr.readlines()
data.sort()
fr.close()
n = len(data)
lastid = ''
for i in range(n-1):
	temp = data[i][:-1].split('\t')
	newtemp = data[i+1][:-1].split('\t')
	if temp[1] == 'null\n' or temp[1] > '20180826':
		continue
	if newtemp[1] == 'null\n' or newtemp[1] > '20180826':
		continue	
	if newtemp[0] == temp[0]:
		before = datetime.datetime.strptime(temp[1], '%Y%m%d')
		after = datetime.datetime.strptime(newtemp[1], '%Y%m%d')
		ietdic[data[i][:-1]] = str((after - before).days)
ietkey = sorted(ietdic.keys())
print 'Finished acitve part.'

foldic = {}
fr = open('../../../data/aweme_edge_follow_day_'+suffix+'.text', 'r')
data = fr.readlines()
data.sort()
fr.close()
n = len(data)
lastid = ''
social = 0
content = 0
for i in range(n):
	temp = data[i][:-1].split('\t')
	if temp[1] == 'null\n' or temp[1] > '20180826':
		continue	
	if temp[0] == lastid:
		social += int(temp[2]) - int(temp[3])
		content += int(temp[4]) - int(temp[5])
	else:
		social = int(temp[2]) - int(temp[3])
		content = int(temp[4]) - int(temp[5])
	foldic[temp[0]+'\t'+temp[1]] = str(social) + '\t' + str(content)
	lastid = temp[0]
folkey = sorted(foldic.keys())
print 'Finished follow part.'

fandic = {}
fr = open('../../../data/aweme_edge_fans_day_'+suffix+'.text', 'r')
data = fr.readlines()
data.sort()
fr.close()
n = len(data)
lastid = ''
social = 0
content = 0
for i in range(n):
	temp = data[i][:-1].split('\t')
	if temp[1] == 'null\n' or temp[1] > '20180826':
		continue	
	if temp[0] == lastid:
		social += int(temp[2]) - int(temp[3])
		content += int(temp[4]) - int(temp[5])
	else:
		social = int(temp[2]) - int(temp[3])
		content = int(temp[4]) - int(temp[5])
	fandic[temp[0]+'\t'+temp[1]] = str(social) + '\t' + str(content)
	lastid = temp[0]		
fankey = sorted(fandic.keys())
print 'Finished fans part.'

posdic = {}
fr = open('../../../data/aweme_post_day_'+suffix+'.text', 'r')
data = fr.readlines()
data.sort()
fr.close()
n = len(data)
lastid = ''
posted = 0
for i in range(n):
	temp = data[i][:-1].split('\t')
	if temp[1] == 'null\n' or temp[1] > '20180826':
		continue	
	if temp[0] == lastid:
		posted += int(temp[2])
	else:
		posted = int(temp[2])
	posdic[temp[0]+'\t'+temp[1]] = str(posted)
	lastid = temp[0]
poskey = sorted(posdic.keys())
print 'Finished post part.'

folpos = 0
folend = len(folkey)
fanpos = 0
fanend = len(fankey)
pospos = 0
posend = len(poskey)
for key in ietkey:
	curid = key.split('\t')[0]
	while folpos < folend:
		newid = folkey[folpos].split('\t')[0]
		if newid > curid:
			ietdic[key] += '\t0\t0'
			break
		if newid == curid:
			if folkey[folpos] <= key:
				if folpos + 1 == folend or folkey[folpos+1] > key:
					ietdic[key] += '\t' + foldic[folkey[folpos]]
					break
				else:
					folpos += 1
			else:
				ietdic[key] += '\t0\t0'
				break
		if newid < curid:
			folpos += 1
	while fanpos < fanend:
		newid = fankey[fanpos].split('\t')[0]
		if newid > curid:
			ietdic[key] += '\t0\t0'
			break
		if newid == curid:
			if fankey[fanpos] <= key:
				if fanpos + 1 == fanend or fankey[fanpos+1] > key:
					ietdic[key] += '\t' + fandic[fankey[fanpos]]
					break
				else:
					fanpos += 1
			else:
				ietdic[key] += '\t0\t0'
				break
		if newid < curid:
			fanpos += 1
	while pospos < posend:
		newid = poskey[pospos].split('\t')[0]
		if newid > curid:
			ietdic[key] += '\t0'
			break
		if newid == curid:
			if poskey[pospos] <= key:
				if pospos + 1 == posend or poskey[pospos+1] > key:
					ietdic[key] += '\t' + posdic[poskey[pospos]]
					break
				else:
					pospos += 1
			else:
				ietdic[key] += '\t0'
				break
		if newid < curid:
			pospos += 1			
print 'Finished arranging part.'

fw = open('../../../data/aweme_active_iet_'+suffix+'.text', 'w')
for key in ietkey:
	fw.write(key+'\t'+ietdic[key]+'\n')
fw.close()
print 'Finished writing part.'
