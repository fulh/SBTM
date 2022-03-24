import xadmin
from xadmin import views
from .sql_util import SQLTool
from xadmin.views.base import CommAdminView


from .barbase import bar_base, charts_base, bar_test, bar_Liquid, bar_two, progress_bar,bugTrend_bar
from .models import Progress,BarCharts
from charts import sqlfile


class ProgressAdmin(object):
	# list_display = []
	object_list_template = "test1.html"
	# model_icon = 'fa fa-quora'
	model_icon = 'fa fa-arrows'
	# model_icon = 'fa fa-area-chart'
	# model_icon = 'fa fa-chart'

	def get_context(self):
		context = CommAdminView.get_context(self)
		bugTrend_bar_charts = bugTrend_bar(sqlfile.bugEveryTrend).render_embed()
		progress_bar_charts = progress_bar(sqlfile.public_list).render_embed()
		reproduction_bar_charts = progress_bar(sqlfile.reproduction_list).render_embed()
		fattenone_bar_charts = progress_bar(sqlfile.fattenone_list).render_embed()
		purchaseAndsale_bar_charts = progress_bar(sqlfile.purchaseAndsale_list).render_embed()
		purchaseAndsaleapp_bar_charts = progress_bar(sqlfile.purchaseAndsaleapp_list).render_embed()
		fattenoneapp_bar_charts = progress_bar(sqlfile.fattenoneapp_list).render_embed()
		fattentwo_bar_charts = progress_bar(sqlfile.fattentwo_list).render_embed()
		fattentwoapp_bar_charts = progress_bar(sqlfile.fattentwoapp_list).render_embed()

		context.update(
			{"progress_bar_charts": progress_bar_charts, "reproduction_bar_charts": reproduction_bar_charts,
			 "fattenone_bar_charts": fattenone_bar_charts,
			 "purchaseAndsale_bar_charts": purchaseAndsale_bar_charts,
			 "purchaseAndsaleapp_bar_charts": purchaseAndsaleapp_bar_charts,
			 "fattenoneapp_bar_charts": fattenoneapp_bar_charts, "fattentwo_bar_charts": fattentwo_bar_charts,
			 "fattentwoapp_bar_charts": fattentwoapp_bar_charts,
			 "bugTrend_bar_charts": bugTrend_bar_charts}
		)
		return context


class BarChartsAdmin(object):
	# list_display = []
	# 设置需要跳转的页面 index1.html，这个页面需要在template
	object_list_template = "index1.html"
	# 设置图标，这个图标
	model_icon ='fa fa-bug'

	def get_context(self):
		context = CommAdminView.get_context(self)
		dic_list = {"公共": "12", "繁殖": "1", "育肥": "2", "购销": "3"}
		dicResult = SQLTool().select_test("select  line,  AVG(number)as num from zt_progress  GROUP BY line")
		dic_lista = {}
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

		context.update(
			{"charts_public": charts_public, "charts_reproduction": charts_reproduction,
			 "charts_fatten": charts_fatten, "charts_purchaseAndsale": charts_purchaseAndsale,
			 "liquid_public": liquid_public, "liquid_reproduction": liquid_reproduction,
			 "liquid_fatten": liquid_fatten,
			 "liquid_purchaseAndsale": liquid_purchaseAndsale,
			 "two_bar": two_bar,
			 # "two_today_bar":two_today_bar,
			 "dic_lista": dic_lista}
		)
		return context


xadmin.site.register(Progress, ProgressAdmin)
xadmin.site.register(BarCharts, BarChartsAdmin)
