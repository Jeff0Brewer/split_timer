import sys
import os
import time
from datetime import datetime

if len(sys.argv) < 2:
	print('syntax: python script_path save_path')
	exit()

directory = sys.argv[1]
split_names = open(directory + 'splits.txt', 'r').read().split('\n')
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
	return str(a)[0:7]
def format_time(a):
	return a.strftime('%-I:%M:%S %p')


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

	s = ''
	s += G + 'start time:' + W + ' ' + format_time(start_t) + '\n\n'
	s += ''
	for i in range(len(split_names)):
		s += split_names[i] + ': '
		if i < len(splits):
			s += G + format_delta(splits[i]) + W
		if i == len(splits):
			s += split_text[pause_state]
		s += '\n'
	s += '\n' + G + '1:' + W + ' split, ' + G + '2:' + W + ' ' + pause_text[pause_state] + ', ' + G + '3:' + W + ' restart, ' + G + '8:' + W + ' delete split, ' + G + '9:' + W + ' save, ' + G + '0:' + W + ' quit\n'
	write(s)

	try:
		i = int(raw_input())
	except ValueError:
		i = -1
	if i == 1 and pause_state == 0 and len(splits) < len(split_names):
		splits.append(datetime.now() - (start_t + pause_total))
	if i == 2:
		pause_state = (pause_state + 1) % 2
		if pause_state == 0:
			pause_total += datetime.now() - pause_start
		else:
			pause_start = datetime.now()
	if i == 3:
		start_t = datetime.now();
		pause_total = start_t - start_t
		pause_state = 0
		splits = [];
	if i == 8 and len(splits) > 0:
		splits.pop()
	if i == 9:
		f = open(directory + datetime.now().strftime('%m_%d_%y_%H_%M_%S.txt'), 'w')
		s = ''
		for i in range(len(splits)):
			s += split_names[i] + ': ' + format_delta(splits[i]) + '\n'
		f.write(s)
		f.close()
	if i == 0:
		exit()
	tick()
tick()



