import sys
import numpy as np
import matplotlib as plt
import datetime

suffix = '100to500'
enddate = datetime.datetime.strptime('20180826', '%Y%m%d')
idset = set()
churnset = set()
cdlist = list() #churn time
ncdlist = list() #non churn time
for i in range(6): #social_rate_fol, social_rate_fan, social_number_fol, content_number_fol, social_number_fan, content_number_fan
	cdlist.append({})
	ncdlist.append({})
idset = set()
fr = open('../../../data/aweme_active_iet_'+suffix+'.text', 'r')
data = fr.readlines()
#data.sort()
fr.close()
n = len(data)
lastid = ''
lastdate = ''
lastinfo = [-1, -1, 0, 0, 0, 0] #social_rate_fol, social_rate_fan, social_number_fol, content_number_fol, social_number_fan, content_number_fan
curtime = [0, 0, 0, 0, 0, 0] #social_rate_fol, social_rate_fan, social_number_fol, content_number_fol, social_number_fan, content_number_fan
for i in range(n):
	temp = data[i][:-1].split('\t')
	if lastid != temp[0]:
		for j in range(6):
			if curtime[j] != 0 and lastinfo[j] >= 0:
				if not lastinfo[j] in ncdlist[j]:
					ncdlist[j][lastinfo[j]] = {}
				if curtime[j] in ncdlist[j][lastinfo[j]]:
					ncdlist[j][lastinfo[j]][curtime[j]] += 1
				else:
					ncdlist[j][lastinfo[j]][curtime[j]] = 1
				curtime[j] = 0
		lastinfo = [-1, -1, 0, 0, 0, 0]
		curtime = [0, 0, 0, 0, 0, 0]
		lastid = temp[0]
	totalfol = int(temp[3]) + int(temp[4])
	totalfan = int(temp[5]) + int(temp[6])
	if not temp[0] in idset:
		if totalfol >= 10 or totalfan >= 10:
			idset.add(temp[0])
		else:
			continue
	if temp[0] in churnset:
		continue
	curinfo = [-1, -1, 0, 0, 0, 0]
	if totalfol > 0:
		curinfo[0] = round(int(temp[3]) * 1.0 / totalfol, 2)
	if totalfan > 0:
		curinfo[1] = round(int(temp[5]) * 1.0 / totalfan, 2)
	for j in range(2, 6):
		curinfo[j] = int(temp[j+1])
	if temp[2][-1] == 'e':
		iet = int(temp[2][:-1])
	else:
		iet = int(temp[2])
	if iet >= 30:
		for j in range(6):
			if curtime[j] == 0 or lastinfo[j] < 0:
				continue
			if curinfo[j] == lastinfo[j]:
				if not lastinfo[j] in cdlist[j]:
					cdlist[lastinfo[j]] = {}
				if curtime[j] in cdlist[lastinfo[j]]:
					cdlist[lastinfo[j]][curtime[j]] += 1
				else:
					cdlist[lastinfo[j]][curtime[j]] = 1
			else:
				if not lastinfo[j] in ncdlist[j]:
					ncdlist[lastinfo[j]] = {}
				if curtime[j] in ncdlist[lastinfo[j]]:
					ncdlist[lastinfo[j]][curtime[j]] += 1
				else:
					ncdlist[lastinfo[j]][curtime[j]] = 1
		lastinfo = [-1, -1, 0, 0, 0, 0]
		curtime = [0, 0, 0, 0, 0, 0]
		churnset.add(temp[0])
	else:
		for j in range(6):
			if curinfo[j] == lastinfo[j] and lastinfo[j] >= 0:
				curtime[j] += iet
			if curinfo[j] != lastinfo[j]:
				if curtime[j] != 0 and lastinfo[j] >= 0:
					if not lastinfo[j] in ncdlist[j]:
						ncdlist[lastinfo[j]] = {}
					if curtime[j] in ncdlist[lastinfo[j]]:
						ncdlist[lastinfo[j]][curtime[j]] += 1
					else:
						ncdlist[lastinfo[j]][curtime[j]] = 1
				curtime[j] = iet
		lastinfo = curinfo
	
fw = open('../../../data/aweme_churn_iet_'+suffix+'.text', 'w')
for i in range(6):
	keys = sorted(cdlist[i].keys())
	for k in keys:
		newkeys = sorted(cdlist[i][k].keys())
		for nk in newkeys:
			fw.write('1\t'+str(i)+'\t'+str(k)+'\t'+str(nk)+'\t'+str(cdlist[i][k][nk])+'\n') #whether churn, type, number, time, popularity
for i in range(6):
	keys = sorted(ncdlist[i].keys())
	for k in keys:
		newkeys = sorted(ncdlist[i][k].keys())
		for nk in newkeys:
			fw.write('0\t'+str(i)+'\t'+str(k)+'\t'+str(nk)+'\t'+str(ncdlist[i][k][nk])+'\n') #whether churn, type, number, time, popularity
fw.close()
print('Finished writing part.')

