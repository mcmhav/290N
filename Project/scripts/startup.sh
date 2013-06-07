#!/bin/bash

APP_NAME="Supa Startup Server"
VERSION=0.1
AUTHORS="Martin Havig <mchcake@gmail.com>"

help_startup() 
{
	echo "Usage: $0 [options]"
	echo "Options:"
	echo -e " -h \t\t\tDisplays this help file"
	echo -e " -v \t\t\tPrints the applications version number and authors"
	echo -e " -m \tmaster host\tSpecifies master host ip"
	echo -e " -z \t\"h1 h2 ..\"\tSpecifies zookeper host ip's"
	echo -e " -n \t\"h1 h2 ..\"\tSpecifies node ip's"
	exit 1
}	

#
# version_mtask
#

version_startup() 
{
	echo "$APP_NAME"
	echo "Version: $VERSION"
	echo "Authors: $AUTHORS"
	exit 0
}

while getopts hvm:z:n: opt
do
	case $opt in 
		h) help_startup;;
		v) version_startup;;
		m) master=$OPTARG;;
		z) zook=( $OPTARG );;
		n) zoo=( $OPTARG );;
		?) help_startup;;
	esac
done

self="$HOSTNAME"
SHARDS=5


killall java
cd solr-4.3.0/build

containsElement () {
  for N in ${@:1}; do [[ "$N" == "$self" ]] && return 1; done
  return 0
}

for N in ${zook[@]}
do
	zookP="$N.us-west-2.compute.internal:9983,$zookP"
done

zookP="$zookP$master.us-west-2.compute.internal:9983"

#check if master
if [ "$self" = "$master" ] 
then 
	echo "$self found in master" >> ~/startup.log
	echo "java -Dbootstrap_confdir=./solr/collection1/conf -Dcollection.configName=myconf -DzkRun=$self.us-west-2.compute.internal:9983 -DzkHost=$zookP -DnumShards=$SHARDS -jar start.jar" >> ~/startup.log
	screen -dmS "node" java -Dbootstrap_confdir=./solr/collection1/conf -Dcollection.configName=myconf -DnumShards=$SHARDS -DzkRun=$self.us-west-2.compute.internal:9983 -DzkHost=$zookP -jar start.jar
	exit 0
fi

#check if zookeeper
containsElement "${zook[@]}"
if [ $? = 1 ] 
then 
	echo "$self found zookeeper" >> ~/startup.log
	echo "java -DzkRun=$self.us-west-2.compute.internal:9983 -DzkHost=$zookP -jar start.jar" >> ~/startup.log
	screen -dmS "node" java -DzkRun=$self.us-west-2.compute.internal:9983 -DzkHost=$zookP -jar start.jar
	exit 0
fi

#check if zoo
containsElement "${zoo[@]}"
if [ $? = 1 ] 
then 
	echo "$self found in zoo" >> ~/startup.log
	echo "java -Djetty.port=7574 -DzkHost=$zookP -jar start.jar" >> ~/startup.log
	screen -dmS "node" java -DzkHost=$zookP -jar start.jar
	exit 0
fi

echo "Couldn't find myself" >> ~/startupk.log