# -*- coding:utf-8 -*-

from multiprocessing import Pool
import gevent.monkey
gevent.monkey.patch_socket()
import gevent

import time
import logging

from queue import get_url, add_url
import crawler

import config

process_num = config.get_process_num()
local_gevent_num = config.get_local_gevent_num()
aweight_gevent_num = config.get_aweight_gevent_num()
init_count = config.get_count()

# 首次运行时执行此函数
def init():
	# you can chang the initial url
	url = 'https://www.zhihu.com/people/yigu-zhong-kou-wei'
	add_url(url)


def gevent_worker(option):
	if option == 'local':
		headers, cookies, proxies = config.get_local()
	elif option == 'aweight':
		headers, cookies, proxies = config.get_aweight()
	else:
		print 'Option Error!'
		return
	while True:
		url = get_url()
		if not url:
			break
		slave = crawler.ZhihuCrawler(url, headers, cookies, proxies, option)
		r = slave.crawl()
		if r == 'break':
			print time.strftime('%Y/%m/%d %H:%M:%S'), option.capitalize(),'Break'
			break


def process_worker():
	jobs = []
	for x in xrange(0,local_gevent_num):
		jobs.append(gevent.spawn(gevent_worker, 'local'))
	for x in xrange(0,aweight_gevent_num):
		jobs.append(gevent.spawn(gevent_worker, 'aweight'))
	gevent.joinall(jobs)


if __name__ == '__main__':
	# init()
	time1 = time.time()

	# 多进程+协程模式
	# pool = Pool(8)
	# for x in xrange(0,process_num):
	# 	pool.apply_async(process_worker)
	# pool.close()
	# pool.join()

	# 协程模式
	process_worker()

	# # 简单模式
	# gevent_worker()

	time2 = time.time()
	logging.info('Crawl %d people. Takes %fs\n============================================'%(config.get_count()-init_count, (time2-time1)))