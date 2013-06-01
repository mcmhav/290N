#!/bin/bash
# Run clean and startup


echo "***Resets all servers"
./mtask.py -s reset.sh -i ../supakey.pem -t ../conf/hosts.txt 

echo "***Starts all servers" 
./mtask.py -s startup.sh -i ../supakey.pem -t ../conf/hosts.txt -o m ip-10-250-48-111 --as-array z ../conf/zookeepers.txt --as-array n ../conf/nodes.txt 
echo "***Done"