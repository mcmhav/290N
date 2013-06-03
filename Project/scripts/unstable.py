#!/usr/bin/python
#
# This script makes the servernode unstable, and may shut down
# It waits for a certain amount of time and checks if it needs to change state 
#


import sys, time, signal
from subprocess import call
from random import *



import argparse
import logging



def signal_handler(signal, frame):
    call (['sudo', '/etc/init.d/networking', 'start'])
    print '\nExit!'
    sys.exit(0)

#
# Main
#
signal.signal(signal.SIGINT,signal_handler)

parser = argparse.ArgumentParser(prog = 'Unstable-solr', description = 'Makes a node unstable and likely to shut down')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-i', '--interval', nargs='?', type=int, help = 'Specifies the amount of time between each', required=True)
parser.add_argument('-d', '--prob-shutdown', nargs='?', type=int, help ='Specifies the probability of a shuting down', required=True)
parser.add_argument('-u', '--prob-start', nargs='?', type=int, help = 'Specifies the probability of starting', required=True)
parser.add_argument('-t', '--time', nargs='?', help = 'Specifies the time in minutes the script is supposed to run', required=True)

args = parser.parse_args()
print args


logging.basicConfig(filename='unstable.log',level=logging.DEBUG, format='%(asctime)s:: %(message)s')


DOWN = 0
RUNNING = 1

state = RUNNING

starttime = time.time()


while ((time.time() - starttime )< args.time * 60):

    # Wait for interval time +- 20%
    time.sleep(randint(args.interval - args.interval/5, args.interval + args.interval/5 ) )

    faith = randint(0,100)
    if (state == RUNNING and faith <= args.prob_shutdown):
        print "Shuting down..."
        logging.info("Shutting down")

        call (['sudo', '/etc/init.d/networking', 'stop'])
        state = DOWN
        
    elif (state == DOWN and faith <= args.prob_start):
        print "Starting up"
        logging.info("Starting up")

        # Place startup script here
        call (['sudo', '/etc/init.d/networking', 'start'])
        

        state = RUNNING 



call (['sudo', '/etc/init.d/networking', 'start'])
        




