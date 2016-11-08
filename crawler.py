# -*- coding:utf-8 -*-

import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()

import requests
import win_inet_pton
from queue import check_url, re_crawl_url
from lxml import html
from db import insert_data
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import logging
logging.basicConfig(
				level=logging.INFO,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='log/crawler.log',
                filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-7s %(message)s')
console.setFormatter(formatter)
# 屏蔽requests的INFO输出
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

from config import get_and_add_count


class ZhihuCrawler(object):
	"""Crawl Zhihu."""

	def __init__(self, url, headers, cookies, proxies, option):
		self.url = url
		self.headers = headers
		self.cookies = cookies
		self.proxies = proxies
		self.option = option.capitalize()

	def crawl(self):
		time1 = time.time()
		content = self.download()
		if not content:
			return
		url_list = self.parse(content)
		if not url_list:
			return
		# 如果已经被封IP了则break
		if url_list == 'break':
			return 'break'
		for target_url in url_list:
			check_url(target_url)
		self.output()
		time2 = time.time()
		mes = '%-7s Success %d: %-7.4fs %s'%(self.option,get_and_add_count(),time2-time1,self.user_name)
		logging.info(mes.replace(' s ','s ',1))

	def download(self):
		'''Download followees, answers and topics, return a dict.'''

		# 还没考虑ajax！

		followees_url = self.url + '/followees'
		answers_url = self.url + '/answers'
		topics_url = self.url + '/topics'
		try:
			print '%-7s Downloading %s'%(self.option,self.url)
			r_followees = requests.get(followees_url, headers=self.headers, cookies=self.cookies, proxies=self.proxies, verify=False, timeout=10)
			r_topics = requests.get(topics_url, headers=self.headers, cookies=self.cookies, proxies=self.proxies, verify=False, timeout=10)
			r_answers = requests.get(answers_url, headers=self.headers, cookies=self.cookies, proxies=self.proxies, verify=False, timeout=10)
		except Exception as e:
			# 输出错误信息
			logging.warning('%-7s Fail to Download: %s, Message: %s'%(self.option,self.url, e))
			re_crawl_url(self.url)
			return

		if r_followees.status_code != 200 or r_topics.status_code != 200 or r_answers.status_code != 200:
			# 输出错误信息
			logging.error('%-7s Bad StatusCode: %s, followees: %d, topics: %d, answers: %d'%(self.option,self.url, r_followees.status_code, r_topics.status_code, r_answers.status_code))
			return
		content = {'followees': r_followees.text, 'answers': r_answers.text, 'topics': r_topics.text}
		print '%-7s Success to Download: %s'%(self.option,self.url)
		return content

	def _process_xpath_source(self, source):
		if source:
			return source[0]
		else:
			return ''

	def parse(self, content):
		'''Parse followees, answers and topics, return url_list'''

		self.user_name = ''
		self.user_gender = ''
		self.user_location = ''
		self.user_followees = ''
		self.user_followers = ''
		self.user_be_agreed = ''
		self.user_be_thanked = ''
		self.user_education_school = ''
		self.user_education_subject = ''
		self.user_employment = ''
		self.user_employment_extra = ''
		self.user_bio = ''
		self.user_content = ''
		self.user_topics_num = ''
		self.user_topics = []
		self.user_questions_num = ''
		self.user_answers_num = ''
		self.user_answers = []
		self.user_articles_num = ''
		self.user_favorites_num = ''

		try:
			tree_followees = html.fromstring(content['followees'])
			tree_topics = html.fromstring(content['topics'])
			tree_answers = html.fromstring(content['answers'])
		except Exception as e:
			logging.error('%-7s Fail to Parse: %s, Message: %s'%(self.option,self.url, e))
			# 输出html文件以debug
			# f_followees = open('html/'+self.url[29:]+'_followees'+'.html', 'w')
			# f_followees.write(content['followees'].encode('utf-8'))
			# f_followees.close()
			# f_topics = open('html/'+self.url[29:]+'_topics'+'.html', 'w')
			# f_topics.write(content['topics'].encode('utf-8'))
			# f_topics.close()
			# f_answers = open('html/'+self.url[29:]+'_answers'+'.html', 'w')
			# f_answers.write(content['answers'].encode('utf-8'))
			# f_answers.close()
			return

		# parse the html via lxml
		# parse tree_followees
		self.user_name = self._process_xpath_source(
			tree_followees.xpath("//a[@class='name']/text()"))
		self.user_location = self._process_xpath_source(
			tree_followees.xpath("//span[@class='location item']/@title"))
		self.user_gender = self._process_xpath_source(
			tree_followees.xpath("//span[@class='item gender']/i/@class"))
		if "female" in self.user_gender and self.user_gender:
			self.user_gender = "female"
		else:
			self.user_gender = "male"
		self.user_employment = self._process_xpath_source(
			tree_followees.xpath("//span[@class='employment item']/@title"))
		self.user_employment_extra = self._process_xpath_source(
			tree_followees.xpath("//span[@class='position item']/@title"))
		self.user_education_school = self._process_xpath_source(
			tree_followees.xpath("//span[@class='education item']/@title"))
		self.user_education_subject = self._process_xpath_source(
			tree_followees.xpath("//span[@class='education-extra item']/@title"))

		# 如果无法读到关注信息则会报超过list长度的错，可借此判断IP是否被封
		try:
			self.user_followees = tree_followees.xpath(
				"//div[@class='zu-main-sidebar']//strong")[0].text
			self.user_followers = tree_followees.xpath(
				"//div[@class='zu-main-sidebar']//strong")[1].text
			self.user_questions_num = tree_followees.xpath(
				"//div[@class='profile-navbar clearfix']//span[@class='num']")[0].text
			self.user_answers_num = tree_followees.xpath(
				"//div[@class='profile-navbar clearfix']//span[@class='num']")[1].text
			self.user_articles_num = tree_followees.xpath(
				"//div[@class='profile-navbar clearfix']//span[@class='num']")[2].text
			# 加入机构账号的判断
			if self.url[22:25] == 'org':
				pass
			else:
				self.user_favorites_num = tree_followees.xpath(
					"//div[@class='profile-navbar clearfix']//span[@class='num']")[3].text
			# parse topics num
			user_topics_num_temp = tree_topics.xpath("//span[@class='zm-profile-section-name']/text()")[0]
			self.user_topics_num = user_topics_num_temp[7:-1]
		except:
			logging.error('%-7s IP Forbidden %s'%(self.option,self.url))
			re_crawl_url(self.url)
			# 输出html文件以debug
			f_followees = open('html/'+self.url[29:]+'_followees'+'.html', 'w')
			f_followees.write(content['followees'].encode('utf-8'))
			f_followees.close()
			f_topics = open('html/'+self.url[29:]+'_topics'+'.html', 'w')
			f_topics.write(content['topics'].encode('utf-8'))
			f_topics.close()
			f_answers = open('html/'+self.url[29:]+'_answers'+'.html', 'w')
			f_answers.write(content['answers'].encode('utf-8'))
			f_answers.close()
			return 'break'

		self.user_be_agreed = self._process_xpath_source(tree_followees.xpath(
			"//span[@class='zm-profile-header-user-agree']/strong/text()"))
		self.user_be_thanked = self._process_xpath_source(tree_followees.xpath(
			"//span[@class='zm-profile-header-user-thanks']/strong/text()"))
		self.user_bio = self._process_xpath_source(
			tree_followees.xpath("//span[@class='bio']/@title"))
		self.user_content = self._process_xpath_source(
			tree_followees.xpath("//span[@class='content']/text()"))

		# parse tree from topics, return a list
		self.user_topics = tree_topics.xpath("//div[@class='zm-profile-section-main']//strong/text()")

		# parse tree from answers, return a list
		self.user_answers = tree_answers.xpath("//div[@class='zm-item']//a[@class='question_link']/text()")

		# parse url from followees
		url_list = tree_followees.xpath("//span[@class='author-link-line']/a/@href")
		return url_list

	def output(self):
		'''Store data to MongoDB.'''

		data = {
			'user_url': self.url,
			'user_name': self.user_name,
			'user_gender': self.user_gender,
			'user_location': self.user_location,
			'user_followees': self.user_followees,
			'user_followers': self.user_followers,
			'user_be_agreed': self.user_be_agreed,
			'user_be_thanked': self.user_be_thanked,
			'user_education_school': self.user_education_school,
			'user_education_subject': self.user_education_subject,
			'user_employment': self.user_employment,
			'user_employment_extra': self.user_employment_extra,
			'user_bio': self.user_bio,
			'user_content': self.user_content,
			'user_topics': self.user_topics,
			'user_answers': self.user_answers,
			'user_topics_num': self.user_topics_num,
			'user_questions_num': self.user_questions_num,
			'user_answers_num': self.user_answers_num,
			'user_articles_num': self.user_articles_num,
			'user_favorites_num': self.user_favorites_num
		}

		insert_data(data)
