# coding=utf-8
from .sql_util import SQLTool


def modulebug(sql):
	alist = []
	aindex = ('value', 'name', 'id')
	sqltool = SQLTool()
	data, iTotal_length = sqltool.select(sql)
	for a in data:
		alist.append(dict(zip(aindex, a)))
	return alist

