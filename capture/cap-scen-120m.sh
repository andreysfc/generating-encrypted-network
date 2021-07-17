#!/usr/bin/env bash
# Capture Script with duration 
# Author: Andrey Ferriyan 
#
# v1.1

CURRENTDATE=`date +"%A_%Y-%m-%d_%H%M"`
INTERFACE=ens160
DURATION=120m

sudo timeout ${DURATION} sudo tcpdump -i ${INTERFACE} -n not arp and not icmp and not icmp6 and not stp and not port 64000 -w ${CURRENTDATE}.pcap
