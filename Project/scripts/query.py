#!/usr/bin/python
import sys
import argparse
import os
import subprocess
import signal
import logging
import xml.dom.minidom as minidom
#from multiprocessing import Process, Queue
import multiprocessing as mp
import time
import timeit
#from xml.dom.minidom import parse, parseString
#import xml.etree.ElementTree as ET

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
logging.basicConfig(filename='query.log',level=logging.DEBUG, format='%(asctime)s:: %(message)s')

parser = argparse.ArgumentParser(description='Automated query.')
parser.add_argument('-n', type=str, default="54.214.64.252")
parser.add_argument('-b', type=str, default=1)
args = parser.parse_args()

#arg ='http://' + args.n + ':8983/solr/collection1/select?q=' + 

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

#q = Queue()
total = 0
c = 0
reset = 50
pool = mp.Pool(processes=200)
startTime = time.time()
for w in words: 
	#curl is bottleneck, run in parallel, which makes queries semi-random
	p = pool.apply_async(getWordValues, (w,c))
	
	#p.terminate()
	#time.sleep(2)
	#q.put(p)
	#p.join()
	#p.terminate()

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
		#while not p.ready():
		#	time.sleep(5)
		#p.terminate()	
		print "done waiting"
		c = 0
		startTime = time.time()
		

