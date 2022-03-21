import xadmin
from xadmin import views
from .sql_util import SQLTool
from xadmin.views.base import CommAdminView


from .barbase import bar_base, charts_base, bar_test, bar_Liquid, bar_two, progress_bar,bugTrend_bar
from .models import Progress,BarCharts




bugEveryTrend ="""
select td.datenumber,IFNULL(t1.number,0) as opennum,IFNULL(t2.number,0) as closenum,IFNULL(t3.number,0) as resolvednum,IFNULL(t4.number,0) as activatednum   from t_datenumber td 
LEFT JOIN(
     SELECT
        COUNT( 1 ) AS number,
        DATE_FORMAT( openedDate, '%Y-%m-%d' ) AS datenumber
    FROM
        zt_bug 
    WHERE
        project = '51' 
--         AND DATE_FORMAT( openedDate, '%Y-%m-%d' ) <= curdate( )  and WeekDay(openedDate)   between 0 and 5
    GROUP BY
        DATE_FORMAT( openedDate, '%Y-%m-%d' ) 
) as t1
	on td.datenumber = t1.datenumber
	LEFT JOIN(
		 SELECT
				COUNT( 1 ) AS number,
        DATE_FORMAT( closedDate, '%Y-%m-%d' ) AS datenumber
        FROM
        zt_bug 
    WHERE
        project = '51' and deleted='0'
        AND DATE_FORMAT( closedDate, '%Y-%m-%d' )  
    GROUP BY
        DATE_FORMAT( closedDate, '%Y-%m-%d' ) )t2
	on td.datenumber = t2.datenumber
	LEFT JOIN(
			SELECT
				COUNT( 1 ) AS number,
				DATE_FORMAT( resolvedDate, '%Y-%m-%d' ) AS datenumber 
			FROM
				zt_bug 
		WHERE
				project = '51' and deleted='0'
	GROUP BY
				DATE_FORMAT( resolvedDate, '%Y-%m-%d' ))t3
	on td.datenumber = t3.datenumber
	LEFT JOIN (
			SELECT
					COUNT( 1 ) AS number,
					DATE_FORMAT( activatedDate, '%Y-%m-%d' ) AS datenumber 
			FROM
					zt_bug 
			WHERE
					project = '51' 
			AND deleted = '0' 
     GROUP BY
					DATE_FORMAT( activatedDate, '%Y-%m-%d' )
	) as t4
on td.datenumber = t4.datenumber
WHERE  DATE_FORMAT( td.datenumber, '%Y-%m-%d' ) <= curdate( )
ORDER BY datenumber
"""

sqlmodule = """
    select name from zt_module where id= '{}'
    """


sqlmodulesum = """
	SELECT count(1) as value,zp.name,zp.id,zb.status FROM zt_bug zb
    LEFT JOIN zt_product zp
    on zb.product=zp.id
    where zp.line='{}' and zb.project='51' 
    GROUP BY zp.name,zb.status
    """


progresssql = """
        select AVG(number)as num,SUBSTRING_INDEX( SUBSTRING_INDEX(`NAME`, '-', 2) ,'-',-1) AS name from zt_progress  where line ='{0}'
"""



listproduct = """
		select name from zt_product zp
		LEFT JOIN zt_projectproduct zpp
		on zp.id = zpp.product
		where  zp.line='{0}'and zpp.project='51' """

sqlproducttoday = """
    SELECT  IFNULL(btemp.number,0) as number,replace(atemp.name,'云苍穹-','')as name,atemp.id from (
    select zp.id,zp.name from zt_product zp 
    inner JOIN zt_projectproduct as zpp on zp.id =zpp.product
    where zpp.project='51' and zp.line ='{0}') as atemp
    LEFT JOIN
    (

    SELECT
        zp.name,count(1) as number,zp.id
    FROM
        zt_product zp
        inner  JOIN zt_projectproduct zpp ON zp.id = zpp.product
        inner  JOIN zt_bug zb ON zb.product = zp.id 
    WHERE
        zpp.project = '51' 
        AND zp.line = '{0}' 
        AND DATE_FORMAT( zb.openedDate, '%Y-%m-%d' ) = CURDATE( )
        GROUP BY zp.name
        ) as btemp
        on atemp.id = btemp.id
        ORDER BY name
"""


twoBugSql = """select count(1)as number,status from zt_bug where project='51' GROUP BY status"""
twoBugtoday = """select count(1)as number,status from zt_bug zb where project='51' and DATE_FORMAT(zb.openedDate, '%Y-%m-%d') = CURDATE() GROUP BY status"""

public_list = {"公共云测试计划": ["猪场管理", "物资管理", "猪只变动", "免疫管理", "保健管理", "健康管理", "检测管理", "任务管理", "防非管理"]}
reproduction_list = {"繁殖云测试计划": ["猪只档案", "引种管理", "新开场管理", "公猪管理", "后备管理", "经产管理", "育种管理", "死淘管理", "猪场关账", "繁殖-计划系统"]}
fattenone_list = {"育肥云测试计划": ["基础资料", "养户管理", "投苗管理", "饲养管理", "上市管理", "结算管理", "成本管理", "免疫保健", "邦养宝-公共组件", "育肥-计划系统"]}
purchaseAndsale_list = {
	"购销云测试计划": ["采购-基础资料", "销售-基础资料", "采购-供应商管理", "销售-客户管理", "销售-行情管理", "采购-采购管理", "销售-交易管理", "销售-安全管理"]}
fattenoneapp_list = {"邦养宝APP": ["首页", "任务执行", "养户管理", "投苗申请", "饲养管理", "上市管理", "生物安全", "电子耳标", "检测管理", "报表管理"]}
purchaseAndsaleapp_list = {"邦购销APP": ["首页", "销售管理", "仔猪采购", "种猪采购"]}
fattentwo_list = {"自养育肥云": ["基础档案", "投苗管理业务流程", "饲养管理业务流程", "物资领用", "自养-计划系统"]}
fattentwoapp_list = {
	"邦育肥APP": ["首页", "投苗管理", "饲养管理", "物资领用", "任务管理", "免疫管理", "保健管理", "新开育肥场", "生物安全", "防疫管理", "上市管理"]}

class ProgressAdmin(object):
	# list_display = []
	object_list_template = "test1.html"
	# model_icon = 'fa fa-quora'
	model_icon = 'fa fa-arrows'
	# model_icon = 'fa fa-area-chart'
	# model_icon = 'fa fa-chart'

	def get_context(self):
		context = CommAdminView.get_context(self)

		bugTrend_bar_charts = bugTrend_bar(bugEveryTrend).render_embed()
		progress_bar_charts = progress_bar(public_list).render_embed()
		reproduction_bar_charts = progress_bar(reproduction_list).render_embed()
		fattenone_bar_charts = progress_bar(fattenone_list).render_embed()
		purchaseAndsale_bar_charts = progress_bar(purchaseAndsale_list).render_embed()
		purchaseAndsaleapp_bar_charts = progress_bar(purchaseAndsaleapp_list).render_embed()
		fattenoneapp_bar_charts = progress_bar(fattenoneapp_list).render_embed()
		fattentwo_bar_charts = progress_bar(fattentwo_list).render_embed()
		fattentwoapp_bar_charts = progress_bar(fattentwoapp_list).render_embed()



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

		charts_public = bar_base(sqlmodule.format(dic_list["公共"]), sqlmodulesum.format(dic_list["公共"]),
		                         progresssql.format(dic_list["公共"]),listproduct.format(dic_list["公共"]),
		                         sqlproducttoday.format(dic_list["公共"])).render_embed()
		charts_reproduction = bar_base(sqlmodule.format(dic_list["繁殖"]), sqlmodulesum.format(dic_list["繁殖"]),
		                               progresssql.format(dic_list["繁殖"]),listproduct.format(dic_list["繁殖"]),
		                               sqlproducttoday.format(dic_list["繁殖"])).render_embed()
		charts_fatten = bar_base(sqlmodule.format(dic_list["育肥"]), sqlmodulesum.format(dic_list["育肥"]),
		                         progresssql.format(dic_list["育肥"]),listproduct.format(dic_list["育肥"]),
		                         sqlproducttoday.format(dic_list["育肥"])).render_embed()
		charts_purchaseAndsale = bar_base(sqlmodule.format(dic_list["购销"]), sqlmodulesum.format(dic_list["购销"]),
		                                  progresssql.format(dic_list["购销"]),listproduct.format(dic_list["购销"]),
		                                  sqlproducttoday.format(dic_list["购销"])).render_embed()
		liquid_public = bar_Liquid(progresssql.format(dic_list["公共"]), "公共").render_embed()
		liquid_reproduction = bar_Liquid(progresssql.format(dic_list["繁殖"]), "繁殖").render_embed()
		liquid_fatten = bar_Liquid(progresssql.format(dic_list["育肥"]), "育肥").render_embed()
		liquid_purchaseAndsale = bar_Liquid(progresssql.format(dic_list["购销"]), "购销").render_embed()
		two_bar = bar_two(twoBugSql, twoBugtoday).render_embed()



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
