class GlobalVar(object):
	"""Store global var."""
	count = 1
	process_num = 1
	local_gevent_num = 1
	aweight_gevent_num = 1

	# Your User Agent
	local_user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
	local_headers = {
	    'Host': 'www.zhihu.com',
	    'Connection': 'keep-alive',
	    'Pragma': 'no-cache',
	    'Cache-Control': 'no-cache',
	    'Accept': '*/*',
	    'Origin': 'https://www.zhihu.com',
	    'X-Requested-With': 'XMLHttpRequest',
	    'User-Agent': local_user_agent,
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'Accept-Encoding': 'gzip, deflate',
	    'Accept-Language': 'zh-CN,zh;q=0.8',
	}
	local_cookies = {
		# Your Cookies
	}
	local_proxies = None

	# Your User Agent
	aweight_user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
	aweight_headers = {
	    'Host': 'www.zhihu.com',
	    'Connection': 'keep-alive',
	    'Pragma': 'no-cache',
	    'Cache-Control': 'no-cache',
	    'Accept': '*/*',
	    'Origin': 'https://www.zhihu.com',
	    'X-Requested-With': 'XMLHttpRequest',
	    'User-Agent': aweight_user_agent,
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'Accept-Encoding': 'gzip, deflate',
	    'Accept-Language': 'zh-CN,zh;q=0.8',
	}
	aweight_cookies = {
		# Your Cookies
	}
	aweight_proxies = {
		# Your proxies
	}

def get_count():
	return GlobalVar.count

def get_and_add_count():
	GlobalVar.count = GlobalVar.count + 1
	return GlobalVar.count - 1

def get_process_num():
	return GlobalVar.process_num

def get_local_gevent_num():
	return GlobalVar.local_gevent_num

def get_aweight_gevent_num():
	return GlobalVar.aweight_gevent_num
		
def get_local():
	return GlobalVar.local_headers, GlobalVar.local_cookies, GlobalVar.local_proxies

def get_aweight():
	return GlobalVar.aweight_headers, GlobalVar.aweight_cookies, GlobalVar.aweight_proxies