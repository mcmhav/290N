#!/bin/bash
rm *.log
cd ~/solr-4.3.0/build/solr
killall java
rm -rf zoo_data
rm -rf collection1/data/*
