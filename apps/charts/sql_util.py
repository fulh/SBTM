# coding=utf-8
import traceback
import threading
import pymysql

db = pymysql.connect(host="10.88.3.214", user="root", password="123456",db="zentao", charset="utf8",init_command='SET NAMES UTF8',use_unicode=True)

class SQLTool:
	def __init__(self):
		self.cursor = "Initial Status"
		self.cursor = db.cursor()
		if self.cursor == "Initial Status":
			raise Exception("Can't connect to Database server!")

	# def is_connected(self):
	# 	"""Check if the server is alive"""
	# 	try:
	# 		self.conn.ping(reconnect=True)
	# 		print
	# 		"db is connecting"
	# 	except:
	# 		traceback.print_exc()
	# 		self.conn = self.to_connect()
	# 		print
	# 		"db reconnect"


	def select_test(self, sqlstr):
		lock = threading.Lock()
		lock.acquire()
		db.ping(reconnect=True)
		cur = db.cursor()
		cur.execute(sqlstr)
		# lock.release()
		List = cur.fetchall()
		self.description = cur.description
		cur.close()
		lock.release()
		return List


	# 返回元组套元组数据
	def select(self, sqlstr):
		lock = threading.Lock()
		lock.acquire()
		db.ping(reconnect=True)
		cur = db.cursor()
		cur.execute(sqlstr)
		# lock.release()
		List = cur.fetchall()
		iTotal_length = len(List)
		self.description = cur.description
		cur.close()
		lock.release()
		return List, iTotal_length


	# 返回列表套字典数据
	def select_include_name(self, sqlstr):
		cur = db.cursor()
		cur.execute(sqlstr)
		index = cur.description
		List = cur.fetchall()
		iTotal_length = len(List)
		result = []
		for res in List:
			row = {}
			for i in range(len(index) ):
				row[index[i][0]] = res[i]
			result.append(row)
		cur.close()
		return result, iTotal_length


	# 执行sql语句
	def executesql(self, sqlstr):
		cur = db.cursor()
		r = cur.execute(sqlstr)
		db.commit()
		cur.close()
		return r


	# 插入数据
	def insert(self, sql, param):
		cur = self.cursor
		n = cur.execute(sql, param)
		db.commit()
		cur.close()
		return n


	def release(self):
		return 0