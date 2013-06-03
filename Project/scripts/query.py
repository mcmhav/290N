#!/usr/bin/python
import sys
import argparse
import os
import subprocess
import signal
import logging
import xml.dom.minidom as minidom
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

parser = argparse.ArgumentParser(description='Automated query.')
parser.add_argument('-n', type=str, default="54.214.179.147")
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

for w in words:
	arg = 'http://' + args.n + ':8983/solr/collection1/select?q=' + w
	temp = os.popen("curl " + arg).read()
	#temp = document
	response = minidom.parseString(temp)


#	Could be used, but the xml setup is pretty static, sooo :P
#	for node in response.getElementsByTagName('int'):
#		if node.getAttribute('name') == "status":
#			status = node.firstChild.nodeValue
	
	status = response.childNodes[0].childNodes[1].childNodes[0].firstChild.nodeValue
	qtime = response.childNodes[0].childNodes[1].childNodes[1].firstChild.nodeValue
	query = w
	numFound = response.childNodes[0].childNodes[2].getAttribute('numFound')

	values = [status, qtime, query, numFound]
	print values
	sys.exit(0)

#print words

#http://ec2-54-214-179-147.us-west-2.compute.amazonaws.com:8983/solr/collection1/select?q=*:*
#'http://' + args.n + ':8983/solr/collection1/select?q=*:*'

# to log

# rsponse tid
# respnse amount
# what we searcvhed fpor serach word
# response code?????!!?!?!

