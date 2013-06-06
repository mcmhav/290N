#!/bin/bash

ip-10-250-70-39
./mtask.py -s startup.sh -i ../supakey.pem -t ../conf/hosts.txt -o m ip-10-250-70-39 --as-array z ../conf/zookeepers.txt --as-array n ../conf/nodes.txt
