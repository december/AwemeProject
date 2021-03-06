import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

window = 30

edgedic = {}
postdic = {}
actdic = {}
userdic = {}
startdic = {}
enddic = {}

prefix = '../../../Bytedance/Data/aweme_'
suffix = '_common_day_sample_pol.text'

print 'Begin to read activeness.'
fr = open(prefix+'active'+suffix, 'r')
data = fr.readlines()
data.sort()
fr.close()
start = 0
end = datetime.datetime.strptime('20180826', '%Y%m%d')
n = len(data)
for i in range(n):
	if i > 0 and data[i] == data[i-1]:
		continue
	temp = data[i].split('\t')
	if len(temp) < 2:
		continue
	name = temp[0] + ':' + temp[1]
	if temp[2] == 'null\n' or temp[2] > '20180826':
		continue
	if not actdic.has_key(name):
		start = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')
		startdic[name] = start
		enddic[name] = (end - start).days
		if not userdic.has_key(name):
			userdic[name] = temp[2]		
		actdic[name] = {}
		for j in range(window):
			if j > enddic[name]:
				break			
			actdic[name][j] = 1
	else:
		current = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')	
		delta = (current - start).days
		for j in range(delta, delta+window):
			if j > enddic[name]:
				break			
			if actdic[name].has_key(j):
				actdic[name][j] += 1
			else:
				actdic[name][j] = 1

print 'Begin to read edge dynamics.'
fr = open(prefix+'edge_common_day_sample_fans_pol.text', 'r')
#fr = open(prefix+'edge'+suffix, 'r')
data = fr.readlines()
data.sort()
fr.close()
n = len(data)
social = 0
content = 0
start = 0
for i in range(n):
	temp = data[i].split('\t')
	if len(temp) < 2:
		continue	
	name = temp[0] + ':' + temp[1]
	if temp[2] == 'null' or temp[2] > '20180826':
		continue
	if not edgedic.has_key(name):
		edgedic[name] = {}
		social = int(temp[3]) - int(temp[4])
		content = int(temp[5]) - int(temp[6])
		if not startdic.has_key(name):
			continue
		start = startdic[name]
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')
		tl = list()
		tl.append(social)
		tl.append(content)
		delta = (current - start).days		
		edgedic[name][delta] = tl 
	else:
		social = int(temp[3]) - int(temp[4])
		content = int(temp[5]) - int(temp[6])
		tl = list()
		tl.append(social)
		tl.append(content)
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')		
		delta = (current - start).days		
		edgedic[name][delta] = tl

print 'Begin to read posting dynamics.'
fr = open(prefix+'post'+suffix, 'r')
data = fr.readlines()
data.sort()
fr.close()
start = 0
n = len(data)
for i in range(n):
	temp = data[i].split('\t')
	if len(temp) < 2:
		continue
	if temp[2] > '20180826':
		continue			
	name = temp[0] + ':' + temp[1]
	if not postdic.has_key(name):
		if not startdic.has_key(name):
			continue
		start = startdic[name]
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')
		postdic[name] = {}
		delta = (current - start).days
		postdic[name][delta] = int(temp[3])
	else:
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')		
		delta = (current - start).days		
		postdic[name][delta] = int(temp[3])			

print 'Begin to draw.'
for k in edgedic:
	#Social:y1 Content:y2
	x = list()
	y1 = list()
	y2 = list()
	logy1 = list()
	logy2 = list()
	#Post
	z1 = list()
	w1 = list()
	#Active
	z2 = list()
	w2 = list()

	keylist = sorted(edgedic[k].keys())
	lastd = 1000
	for d in keylist:
		if lastd + 1 < d:
			for i in range(lastd+1, d):
				x.append(i)
				y1.append(0)
				y2.append(0)
				logy1.append(0)
				logy2.append(0)				
		lastd = d	
		x.append(d)
		y1.append(edgedic[k][d][0])
		y2.append(edgedic[k][d][1])
		if edgedic[k][d][0] > 0:
			logy1.append(np.log2(edgedic[k][d][0]+1))
		if edgedic[k][d][0] == 0:
			logy1.append(0)
		if edgedic[k][d][0] < 0:
			logy1.append(-np.log2(-edgedic[k][d][0]+1))
		if edgedic[k][d][1] > 0:
			logy2.append(np.log2(edgedic[k][d][1]+1))
		if edgedic[k][d][1] == 0:
			logy2.append(0)
		if edgedic[k][d][1] < 0:
			logy2.append(-np.log2(-edgedic[k][d][1]+1))		

	x = np.array(x)
	y1 = np.array(y1)
	y2 = np.array(y2)
	logy1 = np.array(logy1)
	logy2 = np.array(logy2)

	if not actdic.has_key(k):
		continue

	keylist = sorted(actdic[k].keys())
	lastd = 1000
	for d in keylist:
		if lastd + 1 < d:
			for i in range(lastd+1, d):
				z2.append(i)
				w2.append(0)
		lastd = d		
		z2.append(d)
		w2.append(actdic[k][d])

	z2 = np.array(z2)	
	w2 = np.array(w2)

	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.grid()
	plt.title(userdic[k])
	ax1.plot(x, y1, marker='.', c='b', label='Social')
	ax1.plot(x, y2, marker='.', c='g', label='Content')
	ax1.set_xlabel('Days')
	ax1.set_ylabel('Pop')
	plt.legend(loc=1)
	ax2.plot(z2, w2, marker='.', c='r', label='Active')
	ax2.set_ylabel('Activeness')
	plt.legend(loc=2)
	if k[-1] == '0':
		plt.savefig('../../../Bytedance/Figs/pol_active_dynamics_rate_fans/fans_act/'+k+'.png')
	if k[-1] == '1':
		plt.savefig('../../../Bytedance/Figs/pol_active_dynamics_rate_fans/fol_act/'+k+'.png')
	plt.cla()
	plt.close(fig)

	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.grid()
	plt.title(userdic[k])
	ax1.plot(x, logy1, marker='.', c='b', label='Social')
	ax1.plot(x, logy2, marker='.', c='g', label='Content')
	ax1.set_xlabel('Days')
	ax1.set_ylabel('LogPop')
	plt.legend(loc=1)
	ax2.plot(z2, w2, marker='.', c='r', label='Active')
	ax2.set_ylabel('Activeness')
	plt.legend(loc=2)	
	if k[-1] == '0':
		plt.savefig('../../../Bytedance/Figs/pol_active_dynamics_rate_fans/fans_act/'+k+'_log.png')
	if k[-1] == '1':
		plt.savefig('../../../Bytedance/Figs/pol_active_dynamics_rate_fans/fol_act/'+k+'_log.png')		
	plt.cla()
	plt.close(fig)

	if not postdic.has_key(k):
		continue

	keylist = sorted(postdic[k].keys())
	lastd = 1000
	for d in keylist:
		if lastd + 1 < d:
			for i in range(lastd+1, d):
				z1.append(i)
				w1.append(0)
		lastd = d		
		z1.append(d)
		w1.append(postdic[k][d])

	z1 = np.array(z1)
	w1 = np.array(w1)

	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.grid()
	plt.title(userdic[k])
	ax1.plot(x, y1, marker='.', c='b', label='Social')
	ax1.plot(x, y2, marker='.', c='g', label='Content')
	ax1.set_xlabel('Days')
	ax1.set_ylabel('Pop')
	plt.legend(loc=1)
	ax2.plot(z1, w1, marker='.', c='r', label='Post')
	ax2.set_ylabel('Posts')
	plt.legend(loc=2)
	if k[-1] == '0':
		plt.savefig('../../../Bytedance/Figs/pol_active_dynamics_rate_fans/fans_post/'+k+'.png')
	if k[-1] == '1':
		plt.savefig('../../../Bytedance/Figs/pol_active_dynamics_rate_fans/fol_post/'+k+'.png')
	plt.cla()
	plt.close(fig)

	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.grid()
	plt.title(userdic[k])
	ax1.plot(x, logy1, marker='.', c='b', label='Social')
	ax1.plot(x, logy2, marker='.', c='g', label='Content')
	ax1.set_xlabel('Days')
	ax1.set_ylabel('LogPop')
	plt.legend(loc=1)
	ax2.plot(z1, w1, marker='.', c='r', label='Post')
	ax2.set_ylabel('Posts')
	plt.legend(loc=2)	
	if k[-1] == '0':
		plt.savefig('../../../Bytedance/Figs/pol_active_dynamics_rate_fans/fans_post/'+k+'_log.png')
	if k[-1] == '1':
		plt.savefig('../../../Bytedance/Figs/pol_active_dynamics_rate_fans/fol_post/'+k+'_log.png')	
	plt.cla()
	plt.close(fig)
