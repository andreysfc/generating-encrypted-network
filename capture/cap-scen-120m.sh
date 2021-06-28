#!/usr/bin/env bash
# Capture Script with duration 
# Author: Andrey Ferriyan <andrey@sfc.wide.ad.jp>
#
# v1.1

CURRENTDATE=`date +"%A_%Y-%m-%d_%H%M"`
INTERFACE=ens160

sudo timeout 120m sudo tcpdump -i ${INTERFACE} -n not arp and not icmp and not icmp6 and not stp and not port 64000 -w ${CURRENTDATE}.pcap
