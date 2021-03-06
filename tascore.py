#!/usr/bin/python

# Tascore - v0.1
# Note: This program requires that xdotool is installed; if it is not
# then this will be a big disaster.

import sys
import subprocess
from time import sleep
from datetime import datetime

# A list of processes to track the usage of
processes_to_track = []
tick_count = 0
start_time = datetime.now()

if len(sys.argv) > 1:
	for i in range(1, len(sys.argv)):
		processes_to_track.append(sys.argv[i])	
else:
	#Default values
	processes_to_track.append("Firefox");
	processes_to_track.append("MonoDevelop");
	processes_to_track.append("LibreOffice");
	
# Initialize the dictionary 
processes = {}
for p in processes_to_track:
	processes[p] = 0
processes["Other"] = 0

def get_active_process():
	"""Returns the title of the currently active window"""
	# Call xdotool
	command = "xdotool getwindowfocus getwindowname"
	output = subprocess.Popen(command, stdout=subprocess.PIPE,
		shell=True).stdout;
	# Parse the bytecode into a file and return it
	return output.read().decode('utf-8').strip()

def record_process(process):
	located = False
	for p in processes_to_track:
		if p in process:
			located = True
			processes[p] += 1
			break
	if not located:
		processes["Other"] += 1
	print_activity()

def print_activity():
	clear_output()
	print("=" * 17)
	print(" " * 4, "TASCORE", " " * 4)
	print("=" * 17)
	print("Session started: %s/%s/%s %s:%s:%s" %
		(start_time.day, start_time.month, start_time.year,
		start_time.hour, start_time.minute, start_time.second))
	print("Total log time: " + get_log_time())
	print("")
	for p in processes:
		percent = processes[p] / tick_count
		print(p + ": " + str(percent * 100) + "%")
	for i in range(4):
		print("")


def seconds(delta):
	return int(delta.seconds % 60)

def minutes(delta):
	return int(delta.seconds / 60) % 60

def hours(delta):
	return int(delta.seconds / 3600)


def get_log_time():
	delta = datetime.now() - start_time
	output = ""
	if(delta.days > 0):
		output += str(delta.days) + " days, "
	if(hours(delta) > 0):
		output += str(hours(delta)) + " hours, "
	if(minutes(delta) > 0):
		output += str(minutes(delta)) + " minutes, "
	output += str(seconds(delta)) + " seconds"
	return output


def tick():
	global tick_count
	tick_count += 1
	record_process(get_active_process())

def clear_output():
	for i in range(100):
		print("")

while True:
	tick()
	sleep(1)
