# -*- coding:utf-8 -*

from pymongo import MongoClient

client = MongoClient()
db = client.zhihu
coll = db.user_info

def insert_data(data):
	coll.insert_one(data)