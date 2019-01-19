import sys
import numpy as np
import matplotlib as plt
import datetime

suffix = '10to50'
enddate = datetime.datetime.strptime('20180826', '%Y%m%d')
idset = set()
churnset = set()
cdlist = list()
ncdlist = list()
for i in range(6): #social_rate_fol, social_rate_fan, social_number_fol, content_number_fol, social_number_fan, content_number_fan
	cdlist.append({})
	ncdlist = append({})
idset = set()
fr = open('../../data/aweme_active_iet_'+suffix+'.text', 'r')
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
			if curtime[j] != 0 and lastinfo[j] > 0:
				if not cdlist.has_key(lastinfo[j]):
					cdlist[lastinfo[j]] = {}
				if cdlist[j][lastinfo[j]].has_key(curtime[j]):
					cdlist[j][lastinfo[j]][curtime[j]] += 1
				else:
					cdlist[j][lastinfo[j]][curtime[j]] = 1
				curtime[j] = 0
		lastinfo = [0, 0, 0, 0, 0, 0]
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

	if int(temp[2]) >= 30:
		for j in range(6):
			if curtime
			if curinfo[j] == lastinfo[j]:
				if not ncdlist[j].has_key()


		if srfol == lastsrfol:
			if ncdlist[0].has_key(ctime[0]):
				ncdlist[0][ctime[0]] += 1
			else:
				ncdlist[0][ctime[0]] = 1
		else:
			if cdlist[0].has_key(ctime[0]):
				cdlist[0][ctime[0]] += 1
			else:
				cdlist[0][ctime[0]] = 1
	


