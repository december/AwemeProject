import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

userdic_fol = {}
userdic_fan = {}

prefix = '../../../Bytedance/Data/aweme_'
suffix = '_pol.text'

print 'Begin to read activeness of followers.'
fr = open(prefix+'active_common_day_sample'+suffix1, 'r')
data = fr.readlines()
data.sort()
fr.close()
start = 0
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
	if not actdic_fol.has_key(name):
		start = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')
		startdic_fol[name] = start
		if not userdic_fol.has_key(name):
			userdic_fol[name] = temp[2]
		actdic_fol[name] = {}
		for j in range(window):
			actdic_fol[name][j] = 1
	else:
		current = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')	
		delta = (current - start).days
		for j in range(delta, delta+window):
			if actdic_fol[name].has_key(j):
				actdic_fol[name][j] += 1
			else:
				actdic_fol[name][j] = 1

fr = open(prefix+'active'+suffix2, 'r')
data = fr.readlines()
data.sort()
fr.close()
start = 0
n = len(data)
for i in range(n):
	if i > 0 and data[i] == data[i-1]:
		continue	
	temp = data[i].split('\t')
	name = temp[0] + ':' + temp[1]
	if temp[2] == 'null\n' or temp[2] > '20180826':
		continue	
	if not actdic_fan.has_key(name):
		start = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')
		startdic_fan[name] = start
		if not userdic_fan.has_key(name):
			userdic_fan[name] = temp[2]			
		actdic_fan[name] = {}
		for j in range(window):
			actdic_fan[name][j] = 1
	else:
		current = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')	
		delta = (current - start).days
		for j in range(delta, delta+window):
			if actdic_fan[name].has_key(j):
				actdic_fan[name][j] += 1
			else:
				actdic_fan[name][j] = 1

print 'Begin to read edge dynamics.'
fr = open(prefix+'edge'+suffix1, 'r')
data = fr.readlines()
data.sort()
fr.close()
n = len(data)
social = 0
content = 0
start = 0
for i in range(n):
	temp = data[i].split('\t')
	name = temp[0] + ':' + temp[1]
	if temp[2] == 'null' or temp[2] > '20180826':
		continue
	if not edgedic_fol.has_key(name):
		edgedic_fol[name] = {}
		social = int(temp[3]) - int(temp[4])
		content = int(temp[5]) - int(temp[6])
		if not startdic_fol.has_key(name):
			continue
		start = startdic_fol[name]
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')
		tl = list()
		tl.append(social)
		tl.append(content)
		delta = (current - start).days		
		edgedic_fol[name][delta] = tl 
	else:
		social += int(temp[3]) - int(temp[4])
		content += int(temp[5]) - int(temp[6])
		tl = list()
		tl.append(social)
		tl.append(content)
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')		
		delta = (current - start).days		
		edgedic_fol[name][delta] = tl 

fr = open(prefix+'edge'+suffix2, 'r')
data = fr.readlines()
data.sort()
fr.close()
n = len(data)
social = 0
content = 0
start = 0
for i in range(n):
	temp = data[i].split('\t')
	name = temp[0] + ':' + temp[1]
	if temp[2] == 'null' or temp[2] > '20180826':
		continue
	if not edgedic_fan.has_key(name):
		edgedic_fan[name] = {}
		social = int(temp[3]) - int(temp[4])
		content = int(temp[5]) - int(temp[6])
		if not startdic_fan.has_key(name):
			continue
		start = startdic_fan[name]
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')	
		tl = list()
		tl.append(social)
		tl.append(content)
		delta = (current - start).days		
		edgedic_fan[name][delta] = tl 
	else:
		social += int(temp[3]) - int(temp[4])
		content += int(temp[5]) - int(temp[6])
		tl = list()
		tl.append(social)
		tl.append(content)
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')		
		delta = (current - start).days					
		edgedic_fan[name][delta] = tl 

print 'Begin to read posting dynamics.'
fr = open(prefix+'post'+suffix1, 'r')
data = fr.readlines()
data.sort()
fr.close()
start = 0
n = len(data)
for i in range(n):
	temp = data[i].split('\t')
	name = temp[0] + ':' + temp[1]
	if temp[2] > '20180826':
		continue
	if not postdic_fol.has_key(name):
		if not startdic_fol.has_key(name):
			continue
		start = startdic_fol[name]
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')
		postdic_fol[name] = {}
		delta = (current - start).days
		postdic_fol[name][delta] = int(temp[3])
	else:
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')		
		delta = (current - start).days		
		postdic_fol[name][delta] = int(temp[3])

fr = open(prefix+'post'+suffix2, 'r')
data = fr.readlines()
data.sort()
fr.close()
start = 0
n = len(data)
for i in range(n):
	temp = data[i].split('\t')
	name = temp[0] + ':' + temp[1]
	if temp[2] > '20180826':
		continue	
	if not postdic_fan.has_key(name):
		if not startdic_fan.has_key(name):
			continue
		start = startdic_fan[name]
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')
		postdic_fan[name] = {}
		delta = (current - start).days		
		postdic_fan[name][delta] = int(temp[3])
	else:
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')		
		delta = (current - start).days		
		postdic_fan[name][delta] = int(temp[3])				

print 'Begin to draw followers.'
for k in edgedic_fol:
	#Social:y1 Content:y2
	x = list()
	y1 = list()
	y2 = list()
	#Post
	z1 = list()
	w1 = list()
	#Active
	z2 = list()
	w2 = list()

	keylist = sorted(edgedic_fol[k].keys())
	for d in keylist:
		x.append(d)
		y1.append(edgedic_fol[k][d][0])
		y2.append(edgedic_fol[k][d][1])

	x = np.array(x)
	y1 = np.array(y1)
	y2 = np.array(y2)	

	if not actdic_fol.has_key(k):
		continue

	keylist = sorted(actdic_fol[k].keys())
	lastd = 1000
	for d in keylist:
		if lastd + 1 < d:
			for i in range(lastd+1, d):
				z2.append(i)
				w2.append(0)
		lastd = d		
		z2.append(d)
		w2.append(actdic_fol[k][d])

	z2 = np.array(z2)	
	w2 = np.array(w2)

	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.grid()
	plt.title(userdic_fol[k])
	ax1.plot(x, y1, marker='.', c='b', label='Social')
	ax1.plot(x, y2, marker='.', c='g', label='Content')
	ax1.set_xlabel('Days')
	ax1.set_ylabel('Pop')
	plt.legend(loc=1)
	ax2.plot(z2, w2, marker='.', c='r', label='Active')
	ax2.set_ylabel('Activeness')
	plt.legend(loc=2)
	plt.savefig('../../../Bytedance/Figs/active_dynamics/fol_act/'+k+'.png')
	plt.cla()
	plt.close(fig)

	if not postdic_fol.has_key(k):
		continue

	keylist = sorted(postdic_fol[k].keys())
	lastd = 1000
	for d in keylist:
		if lastd + 1 < d:
			for i in range(lastd+1, d):
				z1.append(i)
				w1.append(0)
		lastd = d		
		z1.append(d)
		w1.append(postdic_fol[k][d])

	z1 = np.array(z1)
	w1 = np.array(w1)

	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.grid()
	plt.title(userdic_fol[k])
	ax1.plot(x, y1, marker='.', c='b', label='Social')
	ax1.plot(x, y2, marker='.', c='g', label='Content')
	ax1.set_xlabel('Days')
	ax1.set_ylabel('Pop')
	plt.legend(loc=1)
	ax2.plot(z1, w1, marker='.', c='r', label='Post')
	ax2.set_ylabel('Posts')
	plt.legend(loc=2)
	plt.savefig('../../../Bytedance/Figs/active_dynamics/fol_post/'+k+'.png')
	plt.cla()
	plt.close(fig)

print 'Begin to draw fans.'
for k in edgedic_fan:
	#Social:y1 Content:y2
	x = list()
	y1 = list()
	y2 = list()
	#Post
	z1 = list()
	w1 = list()
	#Active
	z2 = list()
	w2 = list()

	keylist = sorted(edgedic_fan[k].keys())
	for d in keylist:
		x.append(d)
		y1.append(edgedic_fan[k][d][0])
		y2.append(edgedic_fan[k][d][1])

	x = np.array(x)
	y1 = np.array(y1)
	y2 = np.array(y2)	

	if not actdic_fan.has_key(k):
		continue

	keylist = sorted(actdic_fan[k].keys())
	lastd = 1000
	for d in keylist:
		if lastd + 1 < d:
			for i in range(lastd+1, d):
				z2.append(i)
				w2.append(0)
		lastd = d
		z2.append(d)
		w2.append(actdic_fan[k][d])

	z2 = np.array(z2)	
	w2 = np.array(w2)

	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.grid()
	plt.title(userdic_fan[k])
	ax1.plot(x, y1, marker='.', c='b', label='Social')
	ax1.plot(x, y2, marker='.', c='g', label='Content')
	ax1.set_xlabel('Days')
	ax1.set_ylabel('Pop')
	plt.legend(loc=1)
	ax2.plot(z2, w2, marker='.', c='r', label='Active')
	ax2.set_ylabel('Activeness')
	plt.legend(loc=2)
	plt.savefig('../../../Bytedance/Figs/active_dynamics/fans_act/'+k+'.png')
	plt.cla()
	plt.close(fig)

	if not postdic_fan.has_key(k):
		continue

	keylist = sorted(postdic_fan[k].keys())
	lastd = 1000
	for d in keylist:
		if lastd + 1 < d:
			for i in range(lastd+1, d):
				z1.append(i)
				w1.append(0)
		lastd = d		
		z1.append(d)
		w1.append(postdic_fan[k][d])

	z1 = np.array(z1)
	w1 = np.array(w1)

	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.grid()
	plt.title(userdic_fan[k])
	ax1.plot(x, y1, marker='.', c='b', label='Social')
	ax1.plot(x, y2, marker='.', c='g', label='Content')
	ax1.set_xlabel('Days')
	ax1.set_ylabel('Pop')
	plt.legend(loc=1)
	ax2.plot(z1, w1, marker='.', c='r', label='Post')
	ax2.set_ylabel('Posts')
	plt.legend(loc=2)
	plt.savefig('../../../Bytedance/Figs/active_dynamics/fans_post/'+k+'.png')
	plt.cla()
	plt.close(fig)
