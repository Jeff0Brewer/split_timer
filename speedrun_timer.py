import sys
import os
import time
from datetime import datetime
from datetime import timedelta

if len(sys.argv) < 2:
	print('syntax: python script_path save_path')
	exit()

directory = sys.argv[1]
split_names = open(directory + 'splits.txt', 'r').read().split('\n')
name_len = 0
for name in split_names:
	name_len = max(name_len, len(name))
name_len += 1
for i in range(len(split_names)):
	for j in range(name_len - len(split_names[i])):
		split_names[i] += ' '
best = []
if os.path.exists(directory + 'best.txt'):
	best = open(directory + 'best.txt', 'r').read().split('\n')
	for i in range(len(best)):
		best[i] = best[i].split(':')
		if len(best[i]) > 1:
			best[i] = timedelta(0,float(best[i][2]),0,0,int(best[i][1]),int(best[i][0]))
		else:
			best.remove(best[i])
for i in range(len(split_names) - len(best)):
	best.append(timedelta(seconds = 36000))

R = '\033[0;31m';
G = '\033[0;32m';
B = '\033[0;34m';
W = '\033[0;37m';

def write(s):
	os.system('clear')
	sys.stdout.write('\r')
	sys.stdout.write(s)
	sys.stdout.flush()
def format_delta(a):
	sec = abs(a.total_seconds())
	if sec < 60:
		return str(round(a.total_seconds(), 3))
	if sec < 600:
		return str(a)[3:11]
	if sec < 3600:
		return str(a)[2:11]
	return str(a)[0:11]
def format_total(a):
	return str(a)[0:11]
def format_time(a):
	return a.strftime('%-I:%M:%S %p')
def get_input():
	try:
		in_ = int(raw_input())
	except ValueError:
		in_ = -1
	return in_


start_t = datetime.now()
pause_total = start_t - start_t
pause_start = start_t
pause_state = 0;
splits = []
def tick():
	global start_t
	global pause_total
	global pause_start
	global pause_state
	global splits

	pause_text = ['pause', 'resume']
	split_text = [B + 'IN PROGRESS' + W, R + 'PAUSED' + W]
	sign_text = [R + '+', G + '-']

	s = ''
	s += G + 'start time:' + W + ' ' + format_time(start_t) + '\n\n'
	s += ''
	best_seconds = 0
	for i in range(len(split_names)):
		s += split_names[i] + G + '| '
		if i < len(splits):
			best_seconds += best[i].total_seconds()
			sec = splits[i].total_seconds() - best_seconds
			st = 1
			if sec > 0 and abs(sec) > .001:
				st = 0
			s += W + format_total(splits[i])
			if(abs(sec) < 3600):
				s += G + ' | ' + sign_text[st] + format_delta(timedelta(seconds = abs(sec))) + W
		if i == len(splits):
			s += split_text[pause_state]
		s += W + '\n'
	s += '\n' + G + '1:' + W + ' split, ' + G + '2:' + W + ' ' + pause_text[pause_state] + ', ' + G + '3:' + W + ' restart, ' + G + '8:' + W + ' delete split, ' + G + '9:' + W + ' save, ' + G + '0:' + W + ' quit\n'
	write(s)

	in_ = get_input()
	if in_ == 1 and len(splits) < len(split_names):
		if pause_state == 1:
			t = datetime.now()
			pause_total += t - pause_start
			pause_start = t
		splits.append(datetime.now() - (start_t + pause_total))
	if in_ == 2:
		pause_state = (pause_state + 1) % 2
		if pause_state == 0:
			pause_total += datetime.now() - pause_start
		else:
			pause_start = datetime.now()
	if in_ == 3:
		write(W + 'restart and clear memory?\n' + G + '0:' + W +' no ' + G + '1:' + W + ' yes\n')
		if get_input() == 1:
			start_t = datetime.now();
			pause_total = start_t - start_t
			pause_state = 0
			splits = [];
	if in_ == 8 and len(splits) > 0:
		write(W + 'delete last split?\n' + G + '0:' + W +' no ' + G + '1:' + W + ' yes\n')
		if get_input() == 1:
			splits.pop()
	if in_ == 9:
		s = ''
		for i in range(len(splits)):
			s += split_names[i] + ': ' + format_total(splits[i]) + '\n'
		f = open(directory + datetime.now().strftime('%m_%d_%y_%H_%M_%S.txt'), 'w')
		f.write(s)
		f.close()
		s = ''
		write(W + 'commit times to personal best file?\n' + G + '0:' + W +' no ' + G + '1:' + W + ' yes\n')
		if get_input() == 1:
			base = 0
			for i in range(len(best)):
				if(i < len(splits)):
					level = splits[i].total_seconds() - base
					if level < best[i].total_seconds():
						best[i] = timedelta(seconds = level)
					base = splits[i].total_seconds()
				s += format_total(best[i]) + '\n'
			f = open(directory + 'best.txt', 'w')
			f.write(s)
			f.close()
	if in_ == 0:
		sys.stdout.write(W)
		exit()
	tick()
tick()



