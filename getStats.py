import sys
import numpy as np
import matplotlib as plt
import datetime

enddate = datetime.datetime.strptime('20180826', '%Y%m%d')
fr = open('../../dataset/aweme/aweme_active_iet_100to500.text', 'r')
data = fr.readlines()
#data.sort()
fr.close()
fr = open('../../dataset/aweme/aweme_active_iet_50to100.text', 'r')
data.extend(fr.readlines())
#data.sort()
fr.close()
n = len(data)
totaluser = 0
totalsfol = 0
totalcfol = 0
totalsfan = 0
totalcfan = 0
i = 0
while i < n:
	temp = data[i][:-1].split('\t')
	if i == n - 1 or data[i+1][:-1].split('\t')[0] != temp
		if temp[1] < '20180826':
			totaluser += 1
			totalsfol += int(temp[3])
			totalcfol += int(temp[4])
			totalsfan += int(temp[5])
			totalcfan += int(temp[6])
	else:
		if int(temp[2]) >= 30:
			totaluser += 1
			totalsfol += int(temp[3])
			totalcfol += int(temp[4])
			totalsfan += int(temp[5])
			totalcfan += int(temp[6])
			while i < n and data[i][:-1].split('\t')[0] == temp[0]:
				i += 1
		else:						
			nexttemp = data[i+1][:-1].split('\t')
			if nexttemp[1] >= '20180826':
				totaluser += 1
				totalsfol += int(temp[3])
				totalcfol += int(temp[4])
				totalsfan += int(temp[5])
				totalcfan += int(temp[6])
				while i < n and data[i][:-1].split('\t')[0] == temp[0]:
					i += 1
			else:
				i += 1
print totaluser
print totalsfol
print totalcfol
print totalsfan
print totalcfan

