import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

window = 30

edgedic_fol = {}
postdic_fol = {}
actdic_fol = {}

edgedic_fan = {}
postdic_fan = {}
actdic_fan = {}

userdic_fol = {}
userdic_fan = {}

startdic_fol = {}
startdic_fan = {}

enddic_fol = {}
enddic_fan = {}

prefix = '../../../Bytedance/Data/aweme_'
suffix1 = '_follow_day_sample.text'
suffix2 = '_fans_day_sample.text'

print 'Begin to read activeness.'
fr = open(prefix+'active'+suffix1, 'r')
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
	name = temp[0] + ':' + temp[1]
	if temp[2] == 'null\n' or temp[2] > '20180826':
		continue
	if not actdic_fol.has_key(name):
		start = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')
		startdic_fol[name] = start
		enddic_fol[name] = (end - start).days
		if not userdic_fol.has_key(name):
			userdic_fol[name] = temp[2]
		actdic_fol[name] = {}
		for j in range(window):
			if j > enddic_fol[name]:
				break
			actdic_fol[name][j] = 1
	else:
		current = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')	
		delta = (current - start).days
		for j in range(delta, delta+window):
			if j > enddic_fol[name]:
				break
			if actdic_fol[name].has_key(j):
				actdic_fol[name][j] += 1
			else:
				actdic_fol[name][j] = 1

fr = open(prefix+'active'+suffix2, 'r')
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
	name = temp[0] + ':' + temp[1]
	if temp[2] == 'null\n' or temp[2] > '20180826':
		continue	
	if not actdic_fan.has_key(name):
		start = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')
		startdic_fan[name] = start
		enddic_fan[name] = (end - start).days
		if not userdic_fan.has_key(name):
			userdic_fan[name] = temp[2]			
		actdic_fan[name] = {}
		for j in range(window):
			if j > enddic_fan[name]:
				break			
			actdic_fan[name][j] = 1
	else:
		current = datetime.datetime.strptime(str(int(temp[2])), '%Y%m%d')	
		delta = (current - start).days
		for j in range(delta, delta+window):
			if j > enddic_fan[name]:
				break			
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
		if int(temp[3]) == 0:
			continue
		for j in range(delta, delta+window):
			if j > enddic_fol[name]:
				break
			postdic_fol[name][delta] = 1
	else:
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')		
		delta = (current - start).days
		if int(temp[3]) == 0:
			continue
		for j in range(delta, delta+window):
			if j > enddic_fol[name]:
				break
			if postdic_fol[name].has_key(j):
				postdic_fol[name][j] += 1
			else:
				postdic_fol[name][j] = 1

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
		if int(temp[3]) == 0:
			continue
		for j in range(delta, delta+window):
			if j > enddic_fan[name]:
				break
			postdic_fan[name][delta] = 1
	else:
		current = datetime.datetime.strptime(temp[2], '%Y%m%d')		
		delta = (current - start).days		
		if int(temp[3]) == 0:
			continue
		for j in range(delta, delta+window):
			if j > enddic_fan[name]:
				break
			if postdic_fan[name].has_key(j):
				postdic_fan[name][j] += 1
			else:
				postdic_fan[name][j] = 1				

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
	ax1.set_yscale('log', nonposy='clip')
	plt.savefig('../../../Bytedance/Figs/active_dynamics/fol_act/'+k+'_log.png')
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
	ax1.set_yscale('log', nonposy='clip')
	plt.savefig('../../../Bytedance/Figs/active_dynamics/fol_post/'+k+'_log.png')	
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
	ax1.set_yscale('log', nonposy='clip')
	plt.savefig('../../../Bytedance/Figs/active_dynamics/fans_act/'+k+'_log.png')	
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
	ax1.set_yscale('log', nonposy='clip')
	plt.savefig('../../../Bytedance/Figs/active_dynamics/fans_post/'+k+'_log.png')	
	plt.cla()
	plt.close(fig)
