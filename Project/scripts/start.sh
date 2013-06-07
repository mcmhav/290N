#!/bin/bash

./mtask.py -s startup.sh -i ../supakey.pem -t ../conf/hosts.txt -o m ip-10-245-123-187 --as-array z ../conf/zookeepers.txt --as-array n ../conf/nodes.txt
