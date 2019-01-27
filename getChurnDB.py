import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

suffix = '50to100'
cdlist = list() #churn time
ncdlist = list() #non churn time
for i in range(6): #social_rate_fol, social_rate_fan, social_number_fol, content_number_fol, social_number_fan, content_number_fan
	cdlist.append({})
	ncdlist.append({})
namelist = ['social_rate_fol', 'social_rate_fan', 'social_number_fol', 'content_number_fol', 'social_number_fan', 'content_number_fan']
colorlist = ['k', 'b', 'g', 'm', 'y', 'r', 'c']

def plotDB(idx, numberlist, label, mode):
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
		n = len(popnum)
		s = 0
		for j in range(n):
			s += popnum[j]
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
					s += ncdlist[idx][i][newtimes[k]]
					tempdic[newtimes[k]] = s
					k += 1
				break
			if times[j] < newtimes[k]:
				s += cdlist[idx][i][times[j]]
				tempdic[times[j]] = s
				j += 1
				continue
			if times[j] > newtimes[k]:
				s += ncdlist[idx][i][newtimes[k]]
				tempdic[newtimes[k]] = s
				k += 1
				continue
			if times[j] == newtimes[k]:
				s += cdlist[idx][i][times[j]] + ncdlist[idx][i][newtimes[k]]
				tempdic[times[j]] = s
				j += 1
				k += 1
		tempkey = sorted(tempdic.keys())
		tempnum = list()
		for temp in tempkey:
			tempnum.append(tempdic[temp])
		ccdfx.append(np.array(tempkey))
		ccdfy.append(1 - np.array(tempnum) * 1.0 / s)
	length = len(numberlist)
	#PDF
	if mode == 'loglog':
		plt.xscale('log')
	if mode != 'linear':
		plt.yscale('log')
		plt.ylim(1e-4, 1e-1)		
	for i in range(length):
		plt.plot(pdfx[i], pdfy[i], colorlist[i], label=label[i])
	plt.xlabel('Churn Time')
	plt.ylabel('PDF')
	plt.legend()	
	plt.savefig('../../../Bytedance/churn_iet_distribution/PDF/churn_time_'+mode+'_'+name+'_'+suffix+'.png')
	plt.cla()
	#CDF
	if mode == 'loglog':
		plt.xscale('log')
	if mode != 'linear':
		plt.yscale('log')
		#plt.ylim(1e-4, 1e-1)		
	for i in range(length):
		plt.plot(cdfx[i], cdfy[i], colorlist[i], label=label[i])
	plt.xlabel('Churn Time')
	plt.ylabel('CDF')
	plt.legend()
	plt.savefig('../../../Bytedance/churn_iet_distribution/CDF/churn_time_'+mode+'_'+name+'_'+suffix+'.png')
	plt.cla()
	#CCDF
	if mode == 'loglog':
		plt.xscale('log')
	if mode != 'linear':
		plt.yscale('log')
		#plt.ylim(1e-4, 1e-1)	
	for i in range(length):
		plt.plot(ccdfx[i], ccdfy[i], colorlist[i], label=label[i])
	plt.xlabel('Churn Time')
	plt.ylabel('CCDF')
	plt.legend()		
	plt.savefig('../../../Bytedance/churn_iet_distribution/CCDF/churn_time_'+mode+'_'+name+'_'+suffix+'.png')
	plt.cla()		

fr = open('../../../Bytedance/Data/aweme_churn_iet_'+suffix+'.text', 'r')
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


#10 to 50
if suffix == '10to50':
	#plotDB(0, [0.0,0.2,0.4,0.6,0.8,1.0], ['0','0.2','0.4','0.6','0.8','1'], 'loglog')
	#plotDB(1, [0.0,0.2,0.4,0.6,0.8,1.0], ['0','0.2','0.4','0.6','0.8','1'], 'loglog')
	#plotDB(2, [0,10,20,30,40,50], ['0','10','20','30','40','50'], 'loglog')
	#plotDB(3, [0,100,200,300,400,500], ['0','100','200','300','400','500'], 'loglog')
	plotDB(4, [0,4,8,12,16,20], ['0','4','8','12','16','20'], 'loglog')
	#plotDB(5, [0,10,20,30,40,50], ['0','10','20','30','40','50'], 'loglog')
	#plotDB(0, [0.0,0.2,0.4,0.6,0.8,1.0], ['0','0.2','0.4','0.6','0.8','1'], 'semilog')
	#plotDB(1, [0.0,0.2,0.4,0.6,0.8,1.0], ['0','0.2','0.4','0.6','0.8','1'], 'semilog')
	#plotDB(2, [0,10,20,30,40,50], ['0','10','20','30','40','50'], 'semilog')
	#plotDB(3, [0,100,200,300,400,500], ['0','100','200','300','400','500'], 'semilog')
	plotDB(4, [0,4,8,12,16,20], ['0','4','8','12','16','20'], 'semilog')
	#plotDB(5, [0,10,20,30,40,50], ['0','10','20','30','40','50'], 'semilog')
#50 to 100
if suffix == '50to100':
	plotDB(0, [0.0,0.1,0.2,0.3,0.4,0.5,0.6], ['0','0.1','0.2','0.3','0.4','0.5','0.6'], 'loglog')
	plotDB(1, [0.0,0.1,0.2,0.3,0.4,0.5,0.6], ['0','0.1','0.2','0.3','0.4','0.5','0.6'], 'loglog')
	plotDB(2, [0,10,20,30,40,50,60], ['0','10','20','30','40','50','60'], 'loglog')
	plotDB(3, [0,100,200,300,400,500], ['0','100','200','300','400','500'], 'loglog')
	plotDB(4, [0,10,20,30,40,50,60], ['0','10','20','30','40','50','60'], 'loglog')
	plotDB(5, [0,15,30,45,60,75,90], ['0','15','30','45','60','75','90'], 'loglog')
	plotDB(0, [0.0,0.1,0.2,0.3,0.4,0.5,0.6], ['0','0.1','0.2','0.3','0.4','0.5','0.6'], 'semilog')
	plotDB(1, [0.0,0.1,0.2,0.3,0.4,0.5,0.6], ['0','0.1','0.2','0.3','0.4','0.5','0.6'], 'semilog')
	plotDB(2, [0,10,20,30,40,50,60], ['0','10','20','30','40','50','60'], 'semilog')
	plotDB(3, [0,100,200,300,400,500], ['0','100','200','300','400','500'], 'semilog')
	plotDB(4, [0,10,20,30,40,50,60], ['0','10','20','30','40','50','60'], 'semilog')
	plotDB(5, [0,15,30,45,60,75,90], ['0','15','30','45','60','75','90'], 'semilog')	
#100 to 500
if suffix == '100to500':
	plotDB(0, [0.0,0.1,0.2,0.3,0.4,0.5,0.6], ['0','0.1','0.2','0.3','0.4','0.5','0.6'], 'loglog')
	plotDB(1, [0.0,0.1,0.2,0.3,0.4,0.5,0.6], ['0','0.1','0.2','0.3','0.4','0.5','0.6'], 'loglog')
	plotDB(2, [0,15,30,45,60,75,90], ['0','15','30','45','60','75','90'], 'loglog')
	plotDB(3, [0,100,200,300,400,500], ['0','100','200','300','400','500'], 'loglog')
	plotDB(4, [0,10,20,30,40,50,60], ['0','10','20','30','40','50','60'], 'loglog')
	plotDB(5, [0,100,200,300,400,500], ['0','100','200','300','400','500'], 'loglog')
	plotDB(0, [0.0,0.1,0.2,0.3,0.4,0.5,0.6], ['0','0.1','0.2','0.3','0.4','0.5','0.6'], 'semilog')
	plotDB(1, [0.0,0.1,0.2,0.3,0.4,0.5,0.6], ['0','0.1','0.2','0.3','0.4','0.5','0.6'], 'semilog')
	plotDB(2, [0,15,30,45,60,75,90], ['0','15','30','45','60','75','90'], 'semilog')
	plotDB(3, [0,100,200,300,400,500], ['0','100','200','300','400','500'], 'semilog')
	plotDB(4, [0,10,20,30,40,50,60], ['0','10','20','30','40','50','60'], 'semilog')
	plotDB(5, [0,100,200,300,400,500], ['0','100','200','300','400','500'], 'semilog')

