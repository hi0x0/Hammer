#!/usr/bin/python2.7
#coding:utf-8

from dummy import *

info = {
	'NAME':'Crawl Href Links',
	'AUTHOR':'yangbh',
	'TIME':'20140725',
	'WEB':'',
	'DESCRIPTION':'web爬虫',
	'VERSION':'1.0',
	'RUNLEVEL':1
}

opts = {
	'url':'http://testasp.vulnweb.com',	#'target ip'
	'timeout':3000,			#'pulgin run max time'
	'max_depth':5,
	'max_count':500,
	'time':6*3600,
	'headers':'',
	'cookies':'',
	'ssl_verify':False,
	'same_host':True,
	'same_domain':True,
	'keyword':'',
}

# opts = [
# 	['url','http://testasp.vulnweb.com','target url'],
# 	['timeout',3000,'pulgin run max time'],
# 	['max_depth',5,'crawler max depth'],
# 	['max_count',500,'crawler max count'],
# 	['concurrency',20,'threads'],
# 	['timeout',10,'each request timeout'],
# 	['time',6*3600,'crawler max count'],
# 	['headers',None,'http request headers'],
# 	['cookies',None,'http cookies'],
# 	['ssl_verify',False,''],
# 	['same_host',True,''],
# 	['same_domain',True,''],
# 	['keyword',None,''],
# ]

def Assign(services):
	if services.has_key('url'):
		return True
	return False

def Audit(services):
	url = services['url']
	args = Strategy(url=url,max_depth=5,max_count=500,concurrency=20,
		timeout=10,time=6*3600,headers=None,cookies=None,ssl_verify=False,
		same_host=True,same_domain=True,keyword=None)
	crawler = Crawler(args)
	crawler.start()
	# pprint([i for i in crawler.visitedHrefs]+[i for i in crawler.unvisitedHrefs])
	# print 'saving hrefs to file'
	logger('saving hrefs to file')
	crawler.saveAllHrefsToFile()
	# print 'saving paths to file'
	logger('saving paths to file')
	crawler.saveAllPaths()
	# print 'saving extensions to file'
	logger('saving extensions to file')
	crawler.saveAllFileExtensions()

# ----------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------
if __name__=='__main__':
	url='http://www.leesec.com'
	if len(sys.argv) ==  2:
		url = sys.argv[1]
	services = {'url':url}
	pprint(Audit(services))
	pprint(services)