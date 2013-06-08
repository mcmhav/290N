#!/usr/bin/python
import sys
import argparse
import os
import subprocess
import signal
import logging
import multiprocessing as mp

parser = argparse.ArgumentParser(description='Understand query.')
parser.add_argument('-f', type=str, default="query.log")
parser.add_argument('-b', type=str, default=1)
args = parser.parse_args()

#[status, qtime, query, numFound]
def readWords():
	f = open('../log/' + args.f, 'r')
	words = []
	qtimeTot = 0
	numFoundTot = 0
	rtime = 0
	ctot = 0
	for line in f:
		tmp = line[26:].replace('[','').replace(']', '')
		temp2 = tmp.split(',')

		if (len(temp2) == 2):
			rtime += float(temp2[0])
		elif (float(temp2[0][2:][:-1])==0):
			temp2[0] = temp2[0][2:][:-1]
			qtimeTot += float(temp2[1][3:][:-1])
			temp2[2] = temp2[2][2:][:-1]
			numFoundTot += float(temp2[3][3:][:-2])
			ctot += 1
		else:
			ctot += 1	
		
	f.close()
	words = [qtimeTot,numFoundTot,rtime,ctot]
	return words

words = readWords()
tot = words[3]
print words
print words[0]/tot, "\t\ttotQueryTime/totWords"
print words[1]/tot, "\t\ttotFound/totWords \t- \tavg response"
print words[2]/tot, "\t\trtime/totWords"
print words[0]
print (words[3]/words[2])*1000, "\t\tquerys/sec"


