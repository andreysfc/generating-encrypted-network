#!/usr/bin/env bash
# Capture Script 
# Author: Andrey Ferriyan <andrey@sfc.wide.ad.jp>
#
# v1.1

CURRENTDATE=`date +"%A_%Y-%m-%d_%H%M"`
INTERFACE=ens160

sudo tcpdump -i ${INTERFACE} -n not arp and not icmp and not icmp6 and not stp and not port 64000 -w ${CURRENTDATE}.pcap
