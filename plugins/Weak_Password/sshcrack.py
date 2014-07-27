#!/usr/bin/python2.7
#coding:utf-8
import os
import socket
import paramiko
import threading
import sys
import time
from dummy import *

info = {
	'NAME':'SSH Weak Password',
	'AUTHOR':'yangbh',
	'TIME':'20140716',
	'WEB':''
}

ret = ''
def ssh2(ip,port,username,passwd,lock):  
	global ret
	printinfo = 'ssh://%s:%s@%s:%d' % (username,passwd,ip,port)
	printinfo += os.linesep
	flg = False
	for i in range(5):
		try:  
			ssh = paramiko.SSHClient()  
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
			ssh.connect(ip,port,username,passwd,timeout=5) 
			#print 'login success'
			printinfo +=  'login success' + os.linesep
			ssh.close()
			flg = True
			break

		except paramiko.AuthenticationException,e:  
			#print 'paramiko.AuthenticationException',e
			printinfo +=  'paramiko.AuthenticationException:\t' + str(e) + os.linesep
			break
		except socket.timeout,e:
			#print 'socket.timeout',e
			printinfo +=  'socket.timeout:\t' + str(e) + os.linesep
			break
		except socket.error,e:
			#print 'socket.error',e
			printinfo +=  'socket.error:\t' + str(e) + os.linesep
			break
		except paramiko.SSHException,e:
			#print 'paramiko.SSHException',e
			printinfo +=  'paramiko.SSHException:\t' + str(e) + os.linesep
			time.sleep(1)
		ssh.close()

	lock.acquire()
	print printinfo
	if flg:
		ret += printinfo
	lock.release()

	return (flg, printinfo)

def getPortByService(services,scname):
	try:
		ret = []
		for eachport in services['port_detail'].keys():
			if services['port_detail'][eachport]['name'] == scname:
				ret.append(eachport)
				#break
		print ret
		return ret
	except KeyError,e:
		print 'KeyError:\t', e

def Audit(services):
	retinfo = {}
	output = ''
	if services.has_key('ip') and services.has_key('ports'):
		# get ssh port
		ssh_port  = 0
		if 22 in services['ports']:
			# name maybe tcpwrapped
			if services['port_detail'][22]['name'] == 'ssh':
				ssh_port = 22

		else:
			ports = getPortByService(services,'ssh')
			if ports and len(ports):
				ssh_port = ports[0]
		if ssh_port == 0:
			return (None,output)

		# get username
		commonpwd = []
		#pwdfile = '../../lib/db/temp.txt'
		pwdfile = LIBDIR+'/db/temp.txt'

		fp = open(pwdfile,'r')
		for eachline in fp:
			tp =  eachline.replace('\r','')
			tp =  tp.replace('\n','')
			if tp != '':
				commonpwd.append(tp)
		print 'commonpwd:\t',commonpwd
		#sys.exit(0)

		#usernames = ['root','test','rootroot','admin','administrator']
		usernames=['root','test']
		# get each username's password

		#  threads
		lock = threading.Lock()
		threads = []
		ip = services['ip']
		maxthreads = 20

		for eachname in usernames:
			for eachpwd in commonpwd:
				th = threading.Thread(target=ssh2,args=(ip,ssh_port,eachname,eachpwd,lock))
				threads.append(th)

		i = 0
		while i<len(threads):
			if i+maxthreads >len(threads):
				numthreads = len(threads) - i
			else:
				numthreads = maxthreads
			print 'threads:',i,' - ', i + numthreads

			# start threads
			for j in range(numthreads):
				threads[i+j].start()

			# wait for threads
			for j in range(numthreads):
				threads[i+j].join()

			i += maxthreads

	# else:
	# 	output += 'plugin does not run' + os.linesep

	if ret != '':
		retinfo = {'level':'high','content':ret}

	return (retinfo,output)
# ----------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------
if __name__=='__main__': 
	services={'ip':'10.202.18.81','ports':[80,8080],'port_detail':{22:{'name':'ssh'}}}
	pprint(Audit(services))
	pprint(services)