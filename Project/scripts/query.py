#!/usr/bin/python
import sys
import argparse
import os
import subprocess
import signal
import logging
import xml.dom.minidom as minidom
import multiprocessing as mp
import time
import timeit

def readWords():
	f = open('../conf/words.txt', 'r')
	words = []
	for line in f:
		words.append(line.replace("\n", ""))
	f.close()
	return words

def signal_handler(signal, frame):
    print '\nExit!'
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)
logging.basicConfig(filename='../query.log',level=logging.DEBUG, format='%(asctime)s:: %(message)s')

parser = argparse.ArgumentParser(description='Automated query.')
parser.add_argument('-n', type=str, default="54.245.45.15")
parser.add_argument('-b', type=str, default=1)
args = parser.parse_args()

words = readWords()



document = """\
<response hc="a3">
	<lst name="responseHeader">
		<string>martin</string>
		<int name="status">0</int>
		<int name="QTime">1</int>
	</lst>
</response>
"""


def getWordValues(w, c):
	arg = 'http://' + args.n + ':8983/solr/collection1/select?q=' + w
	pipe = target=subprocess.Popen(["curl " + arg],
				stdin=subprocess.PIPE, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE, 
				shell=True)

	temp = pipe.communicate(input='data_to_write')[0]
	response = minidom.parseString(temp)
	status = response.childNodes[0].childNodes[1].childNodes[0].firstChild.nodeValue
	qtime = response.childNodes[0].childNodes[1].childNodes[1].firstChild.nodeValue
	query = w
	numFound = response.childNodes[0].childNodes[2].getAttribute('numFound')

	values = [status, qtime, query, numFound]
	logging.info(values)

total = 0
c = 0
reset = 200
pool = mp.Pool(processes=200)
startTime = time.time()
for w in words: 
	p = pool.apply_async(getWordValues, (w,c))

	c = c + 1
	total = total + 1
	if c == reset:
		print total
		#p.wait()    # could be the best, didn't do the trick		
		pool.close() # to no crash computer with too many procs
		pool.join()
		pool = mp.Pool(processes=200)
		timeTaken = time.time() - startTime
		
		logging.info([timeTaken, reset])
		print "done waiting"
		c = 0
		startTime = time.time()
		

