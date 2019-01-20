import sys
import numpy as np
import matplotlib as plt
import datetime

suffix = '10to50'
cdlist = list() #churn time
ncdlist = list() #non churn time
for i in range(6): #social_rate_fol, social_rate_fan, social_number_fol, content_number_fol, social_number_fan, content_number_fan
	cdlist.append({})
	ncdlist = append({})
namelist = ['social_rate_fol', 'social_rate_fan', 'social_number_fol', 'content_number_fol', 'social_number_fan', 'content_number_fan']
colorlist = ['k', 'b', 'g', 'm', 'y', 'r', 'c']

def plotDB(idx, numberlist, label):
	name = namelist[idx]
	pdfx = list()
	pdfy = list()
	cdfx = list()
	cdfy = list()
	ccdfx = list()
	ccdfy = list()
	for i in numberlist:
		times = sorted(cdlist[idx][i].keys())
		pdfx.append(np.array(times))
		cdfx.append(np.array(times))
		popnum = list()
		for time in times:
			popnum.append(cdlist[idx][i][time])
		popcum = list()
		n = len(pop)
		s = 0
		for j in range(n):
			s += popnum[i]
			popcum.append(s)
		pdfy.append(np.array(popnum) * 1.0 / s)
		cdfy.append(np.array(popcum) * 1.0 / s)
		tempdic = {}
		newtimes = sorted(ncdlist[idx][i].keys())
		j = 0
		k = 0
		m = len(newtimes)
		s = 0
		while j < n or k < m:
			if k >= m:
				while j < n:
					s += cdlist[idx][i][times[j]]
					tempdic[times[j]] = s
					j += 1
				break
			if j >= n:
				while k < m:
					s += cdlist[idx][i][newtimes[k]]
					tempdic[newtimes[k]] = s
					k += 1
				break
			if times[j] < newtimes[k]:
				s += cdlist[idx][i][times[j]]
				tempdic[times[j]] = s
				j += 1
			if times[j] > newtimes[k]:
				s += cdlist[idx][i][newtimes[k]]
				tempdic[newtimes[k]] = s
				k += 1
			if times[j] == newtimes[k]:
				s += cdlist[idx][i][times[j]] + cdlist[idx][i][newtimes[k]]
				tempdic[times[j]] = s
				j += 1
				k += 1
		tempkey = sorted(tempdic.keys())
		tempnum = list()
		for temp in tempkey:
			tempnum.append(tempkey[temp])
		ccdfx.append(np.array(tempkey))
		ccdfy.append(1 - np.array(tempnum) * 1.0 / s)
	length = len(numberlist)
	#PDF
	for i in range(length):
		plt.plot(pdfx[i], pdfy[i], colorlist[i], label=label[i])
	plt.xlabel('Churn Time')
	plt.ylabel('PDF')
	plt.legend()
	plt.xscale('log')
	plt.yscale('log')
	plt.savefig('../../../fig/churn_time_pdf_loglog_'+name+'_'+suffix+'.png')
	plt.cla()
	#CDF
	for i in range(length):
		plt.plot(cdfx[i], cdfy[i], colorlist[i], label=label[i])
	plt.xlabel('Churn Time')
	plt.ylabel('CDF')
	plt.legend()
	plt.xscale('log')
	plt.yscale('log')
	plt.savefig('../../../fig/churn_time_cdf_loglog_'+name+'_'+suffix+'.png')
	plt.cla()
	#CCDF
	for i in range(length):
		plt.plot(ccdfx[i], ccdfy[i], colorlist[i], label=label[i])
	plt.xlabel('Churn Time')
	plt.ylabel('CCDF')
	plt.legend()
	plt.xscale('log')
	plt.yscale('log')
	plt.savefig('../../../fig/churn_time_ccdf_loglog_'+name+'_'+suffix+'.png')
	plt.cla()		

fr = open('../../../data/aweme_churn_iet_'+suffix+'.text', 'r')
data = fr.readlines()
#data.sort()
fr.close()
n = len(data)
for i in range(n):
	temp = data[i][:-1].split('\t')
	temp = [float(k) for k in temp]
	if temp[0] == 1:
		if not cdlist[int(temp[1])].has_key(temp[2]):
			cdlist[int(temp[1])][temp[2]] = {}
		cdlist[int(temp[1])][temp[2]][temp[3]] = temp[4]
	else:
		if not ncdlist[int(temp[1])].has_key(temp[2]):
			ncdlist[int(temp[1])][temp[2]] = {}
		ncdlist[int(temp[1])][temp[2]][temp[3]] = temp[4]


