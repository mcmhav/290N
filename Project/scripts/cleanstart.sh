#!/bin/bash
# Run clean and startup


echo "***Resets all servers"
./mtask.py -r -s reset.sh -i ../supakey.pem -t ../conf/hosts.txt 

echo "***Starts all servers" 
./start.sh
echo "***Done"
