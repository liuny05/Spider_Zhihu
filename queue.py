# -*- coding:utf-8 -*

import redis

url_fresh_list = 'zhihu_url_fresh'
url_has_senn_set = 'zhihu_url_has_seen'

red = redis.Redis(host='localhost', port=6379, db=1)


def add_url(url):
	red.lpush(url_fresh_list, url)


def re_crawl_url(url):
	red.lpush(url_fresh_list, url)


def check_url(url):
	if red.sadd(url_has_senn_set, url):
		red.lpush(url_fresh_list, url)


def get_url():
	return red.rpop(url_fresh_list)