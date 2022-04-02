# coding=utf-8
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from .barbase import bar_base, charts_base, bar_test, bar_Liquid, bar_two, progress_bar,bugTrend_bar
from django.shortcuts import render
from .sql_util import SQLTool
from charts import sqlfile
from .table import table
import time




# Create your views here.


def response_as_json(data):
	json_str = json.dumps(data)
	response = HttpResponse(
		json_str,
		content_type="application/json",
	)
	response["Access-Control-Allow-Origin"] = "*"
	return response


def json_response(data, code=200):
	data = {
		"code": code,
		"msg": "success",
		"data": data,
	}
	return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
	data = {
		"code": code,
		"msg": error_string,
		"data": {}
	}
	data.update(kwargs)
	return response_as_json(data)


JsonResponse = json_response
JsonError = json_error



class progress(APIView):
	def get(self, request, *args, **kwargs):
		#缺陷趋势图
		bugTrend_bar_charts = bugTrend_bar(sqlfile.bugEveryTrend).render_embed()
		progress_bar_charts = progress_bar(sqlfile.public_list).render_embed()
		reproduction_bar_charts = progress_bar(sqlfile.reproduction_list).render_embed()
		fattenone_bar_charts = progress_bar(sqlfile.fattenone_list).render_embed()
		purchaseAndsale_bar_charts = progress_bar(sqlfile.purchaseAndsale_list).render_embed()
		purchaseAndsaleapp_bar_charts = progress_bar(sqlfile.purchaseAndsaleapp_list).render_embed()
		fattenoneapp_bar_charts = progress_bar(sqlfile.fattenoneapp_list).render_embed()
		fattentwo_bar_charts = progress_bar(sqlfile.fattentwo_list).render_embed()
		fattentwoapp_bar_charts = progress_bar(sqlfile.fattentwoapp_list).render_embed()
		return render(request, 'progress.html',
		              {"progress_bar_charts": progress_bar_charts, "reproduction_bar_charts": reproduction_bar_charts,
		               "fattenone_bar_charts": fattenone_bar_charts,
		               "purchaseAndsale_bar_charts": purchaseAndsale_bar_charts,
		               "purchaseAndsaleapp_bar_charts": purchaseAndsaleapp_bar_charts,
		               "fattenoneapp_bar_charts": fattenoneapp_bar_charts, "fattentwo_bar_charts": fattentwo_bar_charts,
		               "fattentwoapp_bar_charts": fattentwoapp_bar_charts,
		               "bugTrend_bar_charts":bugTrend_bar_charts
		               })


class zhengbagn(APIView):
	def get(self, request, *args, **kwargs):
		dic_list = {"公共": "12", "繁殖": "1", "育肥": "2", "购销": "3"}
		dicResult = SQLTool().select_test("select  line,  AVG(number)as num from zt_progress  GROUP BY line")
		dic_lista = {}
		# time.sleep(10)
		for k, v in dic_list.items():
			for a in dicResult:
				if int(a[0]) == int(v):
					dic_lista[k] = "{:.2%}".format(a[1] / 100)
		charts_public = bar_base(sqlfile.sqlmodule.format(dic_list["公共"]), sqlfile.sqlmodulesum.format(dic_list["公共"]),
		                         sqlfile.progresssql.format(dic_list["公共"]),sqlfile.listproduct.format(dic_list["公共"]),
		                         sqlfile.sqlproducttoday.format(dic_list["公共"])).render_embed()
		charts_reproduction = bar_base(sqlfile.sqlmodule.format(dic_list["繁殖"]), sqlfile.sqlmodulesum.format(dic_list["繁殖"]),
		                               sqlfile.progresssql.format(dic_list["繁殖"]),sqlfile.listproduct.format(dic_list["繁殖"]),
		                               sqlfile.sqlproducttoday.format(dic_list["繁殖"])).render_embed()
		charts_fatten = bar_base(sqlfile.sqlmodule.format(dic_list["育肥"]), sqlfile.sqlmodulesum.format(dic_list["育肥"]),
		                         sqlfile.progresssql.format(dic_list["育肥"]),sqlfile.listproduct.format(dic_list["育肥"]),
		                         sqlfile.sqlproducttoday.format(dic_list["育肥"])).render_embed()
		charts_purchaseAndsale = bar_base(sqlfile.sqlmodule.format(dic_list["购销"]), sqlfile.sqlmodulesum.format(dic_list["购销"]),
		                                  sqlfile.progresssql.format(dic_list["购销"]),sqlfile.listproduct.format(dic_list["购销"]),
		                                  sqlfile.sqlproducttoday.format(dic_list["购销"])).render_embed()
		liquid_public = bar_Liquid(sqlfile.progresssql.format(dic_list["公共"]), "公共").render_embed()
		liquid_reproduction = bar_Liquid(sqlfile.progresssql.format(dic_list["繁殖"]), "繁殖").render_embed()
		liquid_fatten = bar_Liquid(sqlfile.progresssql.format(dic_list["育肥"]), "育肥").render_embed()
		liquid_purchaseAndsale = bar_Liquid(sqlfile.progresssql.format(dic_list["购销"]), "购销").render_embed()
		two_bar = bar_two(sqlfile.twoBugSql, sqlfile.twoBugtoday).render_embed()
		# two_today_bar = bar_two(twoBugtoday).render_embed()
		return render(request, 'index.html',
		              {"charts_public": charts_public, "charts_reproduction": charts_reproduction,
		               "charts_fatten": charts_fatten, "charts_purchaseAndsale": charts_purchaseAndsale,
		               "liquid_public": liquid_public, "liquid_reproduction": liquid_reproduction,
		               "liquid_fatten": liquid_fatten,
		               "liquid_purchaseAndsale": liquid_purchaseAndsale,
		               "two_bar": two_bar,
		               # "two_today_bar":two_today_bar,
		               "dic_lista": dic_lista})


class ChartView(APIView):
	def get(self, request, *args, **kwargs):
		moduleid = (kwargs["moduleid"])
		return JsonResponse(json.loads(
			bar_base(sqlfile.sqlproduct.format(moduleid), sqlfile.sql.format(moduleid), sqlfile.projectsql.format(moduleid),
			         sqlfile.sqltoday.format(moduleid))))


class IndexView(APIView):
	def get(self, request, *args, **kwargs):
		return HttpResponse(content=open("./templates/index8.html", encoding="utf-8").read())


class CultivatesView(APIView):
	def get(self, request, *args, **kwargs):
		moduleid = (kwargs["moduleid"])
		return JsonResponse(json.loads(
			bar_base(sqlfile.sqlmodule.format(moduleid), sqlfile.sqlmodulesum.format(moduleid), sqlfile.progresssql.format(moduleid),
			         sqlfile.sqlproducttoday.format(moduleid))))


class ModuleView(APIView):
	def get(self, request, *args, **kwargs):
		data = charts_base(sqlfile.sqldate)
		return JsonResponse(json.loads(data))


sql1_test = """
    select number,name,id from t_test
    """
sql2_test = """
    select dataline,name,id from t_test
"""
sql3_test = """select number1,name,id from t_test"""
sql4_test = """select number2,name,id from t_test"""
sql5_test = """select number3,name,id from t_test"""


class ModuleTestView(APIView):
	def get(self, request, *args, **kwargs):
		data = bar_test(sql2_test, sql1_test, sql3_test, sql4_test, sql5_test)
		return JsonResponse(json.loads(data))

# class LiquidView(APIView):
#     def get(self, request, *args, **kwargs):
#         return JsonResponse(json.loads(liquid_test))
