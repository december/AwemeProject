import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

def returnType(a, b):
	a = int(a)
	b = int(b)
	# Many fans and little followers
	if (a == 1 or a == 4 or a == 7) and (b == 3 or b == 6 or b == 9):
		return 0
	# Many followers and little fans
	if (b == 1 or b == 4 or b == 7) and (a == 3 or a == 6 or a == 9):
		return 1
	# Others
	return -1

fr = open('../aweme_edge_common_day_sample.text', 'r')
data = fr.readlines()
data.sort()
fr.close()
result = list()
n = len(data)
for i in range(n):
	temp = data[i].split('\t')
	cluster = returnType(temp[1], temp[2])
	if cluster < 0:
		continue
	line = temp[0] + '\t' + str(cluster) + '\t' + temp[3] + '\t' + temp[4] + '\t' + temp[5] + '\t' + temp[6] + '\t' + temp[7] + '\n'
	result.append(line)

fw = open('../aweme_edge_common_day_sample_pol.text', 'w')
for line in result:
	fw.write(line)
fw.close()

'''
fr = open('../aweme_active_common_day_sample.text', 'r')
data = fr.readlines()
data.sort()
fr.close()
result = list()
n = len(data)
for i in range(n):
	temp = data[i].split('\t')
	cluster = returnType(temp[1], temp[2])
	if cluster < 0:
		continue
	line = temp[0] + '\t' + str(cluster) + '\t' + temp[3] + '\n'
	result.append(line)

fw = open('../aweme_active_common_day_sample_pol.text', 'w')
for line in result:
	fw.write(line)
fw.close()
'''
fr = open('../aweme_post_common_day_sample.text', 'r')
data = fr.readlines()
data.sort()
fr.close()
result = list()
n = len(data)
for i in range(n):
	temp = data[i].split('\t')
	cluster = returnType(temp[1], temp[2])
	if cluster < 0:
		continue
	line = temp[0] + '\t' + str(cluster) + '\t' + temp[3] + '\t' + temp[4] + '\n'
	result.append(line)

fw = open('../aweme_post_common_day_sample_pol.text', 'w')
for line in result:
	fw.write(line)
fw.close()

