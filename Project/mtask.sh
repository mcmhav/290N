#!/bin/bash
#
# Script to do the same task on multiple servers
# Author: Vegar Engen
#
#
APP_NAME="Multiserver task"
VERSION=0.1
AUTHORS="Vegar Engen <vegar.engen@gmail.com>"

hosts="hosts.txt"
script="script.sh"
identity="~/.ssh/id_rsa"
#identity="supakey.pem"
#
# help_mtask
#
help_mtask() 
{
	echo "Usage: $0 [options]"
	echo "Options:"
	echo -e " -h \t\tDisplays this help file"
	echo -e " -v \t\tPrints the applications version number and authors"
	echo -e " -l \tfile\tSpecifies host ips"
	echo -e " -s \tscript\tSpecifies the script to run on each server"
	echo -e " -i \tkey\tSpecifies which identity file to use" 
	echo -e " -d \t\tDisplays default values" 
	exit 1
}	

#
# version_mtask
#
version_mtask() 
{
	echo "$APP_NAME"
	echo "Version: $VERSION"
	echo "Authors: $AUTHORS"
	exit 0
}

#
# defaults_mtask
#
defaults_mtask()
{
	echo "Host-file: $hosts"
	echo "Script: $script"
	echo "Identity file: $identity"
	exit 0
}

#
# Main


while getopts hvdl:s:i: opt
do
	case "$opt" in 
		h) help_mtask;;
		v) version_mtask;;
		d) defaults_mtask;;
		l) hosts="$OPTARG";;
		s) script="$OPTARG";;
		i) identity="$OPTARG";;
		?) help_mtask;;
	esac
done


a=0
while read line
do 
	a=$(($a+1));
	scp  -i $identity $script $line:
	ssh -t -i $identity $line <<EOF

		chmod +x $script
		bash $script
		rm $script
		exit
EOF
	echo "$line: done"

done < $hosts

echo "You have ran $script on $a hosts";
