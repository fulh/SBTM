# coding=utf-8
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from .barbase import bar_base, charts_base, bar_test, bar_Liquid, bar_two, progress_bar,bugTrend_bar
from django.shortcuts import render
from .sql_util import SQLTool
from .table import table




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

sql = """select IFNULL(number,0) as anumber,IFNULL(name,"没有选择模块") as module,c.id FROM (
            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                    zt_module as a  where a.root='{0}' and a.deleted='0'  and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}' and zb.project='51'
            GROUP BY zm.car) as a 
            LEFT JOIN(select name,id from zt_module where root='{0}' and parent='0' and deleted='0' ) as b
            on a.car = b.id

            union

            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                    zt_module as a  where a.root='{0}' and a.deleted='0' and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product = '{0}' and zb.project='51'
            GROUP BY zm.car) as a 
            RIGHT  JOIN(select name as modulename ,id from zt_module where root='{0}' and parent='0' and deleted='0' and (type='bug' or type='story')) as b
            on a.car = b.id
            ) as c  
            group by module
            """

sqlmodulesum = """
	SELECT count(1) as value,zp.name,zp.id,zb.status FROM zt_bug zb
    LEFT JOIN zt_product zp
    on zb.product=zp.id
    where zp.line='{}' and zb.project='51' 
    GROUP BY zp.name,zb.status
    """

sqlmodule = """
    select name from zt_module where id= '{}'
    """

sqlproduct = """select name from  zt_product where id ='{}'"""

sqldate = """
     SELECT
        COUNT( 1 ) AS number,
        DATE_FORMAT( openedDate, '%Y-%m-%d' ) AS datenumber,
        DATE_FORMAT( openedDate, '%Y-%m-%d' ) AS id 
    FROM
        zt_bug 
    WHERE
        project = '51' 
        AND DATE_FORMAT( openedDate, '%Y-%m-%d' ) >= '2022-2-22'  and WeekDay(openedDate)   between 0 and 4
    GROUP BY
        DATE_FORMAT( openedDate, '%Y-%m-%d' ) 
    ORDER BY
        openedDate
    
    
 """

sqltoday = """
            select IFNULL(number,0) as anumber,IFNULL(name,"无") as module,c.id FROM (
            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                   zt_module as a  where a.root='{0}' and a.deleted='0'  and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}' and zb.project='51' and DATE_FORMAT(zb.openedDate,'%Y-%m-%d') = CURDATE()
            GROUP BY zm.car) as a 
            LEFT JOIN(select name,id from zt_module where root={0} and parent='0' and deleted='0' ) as b
            on a.car = b.id


            union

            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                    zt_module as a  where a.root='{0}' and a.deleted='0' and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}' and zb.project='51' and DATE_FORMAT(zb.openedDate,'%Y-%m-%d') = CURDATE()
            GROUP BY zm.car) as a 
            RIGHT  JOIN(select name as modulename ,id from zt_module where root='{0}' and parent='0' and deleted='0' and (type='bug' or type='story') ) as b
            on a.car = b.id
            ) as c 
            ORDER BY module
"""
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
sqlmoduletoday = """
select IFNULL(number,0) as anumber,IFNULL(name,"无") as module,c.id FROM (
            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                   zt_module as a  where a.root='{0}' and a.deleted='0'  and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}' and zb.project='51' and DATE_FORMAT(zb.openedDate,'%Y-%m-%d') = CURDATE()
            GROUP BY zm.car) as a 
            LEFT JOIN(select name,id from zt_module where root=22 and parent='0' and deleted='0' ) as b
            on a.car = b.id


            union

            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                    zt_module as a  where a.root='{0}' and a.deleted='0' and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}'and zb.project='51' and DATE_FORMAT(zb.openedDate,'%Y-%m-%d') = CURDATE()
            GROUP BY zm.car) as a 
            RIGHT  JOIN(select name as modulename ,id from zt_module where root='{0}' and parent='0' and deleted='0' and (type='bug' or type='story') ) as b
            on a.car = b.id
            ) as c  
            ORDER BY module
            """
progresssql = """
        select AVG(number)as num,SUBSTRING_INDEX( SUBSTRING_INDEX(`NAME`, '-', 2) ,'-',-1) AS name from zt_progress  where line ='{0}'
"""

projectsql = """select number from zt_progress where id ='{0}'"""

twoBugSql = """select count(1)as number,status from zt_bug where project='51' GROUP BY status"""
twoBugtoday = """select count(1)as number,status from zt_bug zb where project='51' and DATE_FORMAT(zb.openedDate, '%Y-%m-%d') = CURDATE() GROUP BY status"""

listproduct = """
		select name from zt_product zp
		LEFT JOIN zt_projectproduct zpp
		on zp.id = zpp.product
		where  zp.line='{0}'and zpp.project='51' """


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


# listproduct = """
# 	select a.number,replace(name,'云苍穹-','') AS rep,a.id
#     from (SELECT count(1) as number,zp.name,zp.id FROM zt_bug zb
#     LEFT JOIN zt_product zp
#     on zb.product=zp.id
#     where zp.line='{0}' and zb.project='51'
#     GROUP BY zp.name) as a
#     ORDER BY rep """

class progress(APIView):

	def get(self, request, *args, **kwargs):
		public_list = {"公共云测试计划": ["猪场管理", "物资管理", "猪只变动", "免疫管理", "保健管理", "健康管理", "检测管理", "任务管理", "防非管理"]}
		reproduction_list = {"繁殖云测试计划": ["猪只档案", "引种管理", "新开场管理", "公猪管理", "后备管理", "经产管理", "育种管理", "死淘管理", "猪场关账","繁殖-计划系统"]}
		fattenone_list = {"育肥云测试计划": ["基础资料", "养户管理", "投苗管理", "饲养管理", "上市管理", "结算管理", "成本管理", "免疫保健", "邦养宝-公共组件","育肥-计划系统"]}
		purchaseAndsale_list = {
			"购销云测试计划": ["采购-基础资料", "销售-基础资料", "采购-供应商管理", "销售-客户管理", "销售-行情管理", "采购-采购管理", "销售-交易管理", "销售-安全管理"]}
		fattenoneapp_list = {"邦养宝APP": ["首页", "任务执行", "养户管理", "投苗申请", "饲养管理", "上市管理", "生物安全", "电子耳标", "检测管理", "报表管理"]}
		purchaseAndsaleapp_list = {"邦购销APP": ["首页", "销售管理", "仔猪采购", "种猪采购"]}
		fattentwo_list = {"自养育肥云": ["基础档案", "投苗管理业务流程", "饲养管理业务流程", "物资领用","自养-计划系统"]}
		fattentwoapp_list = {
			"邦育肥APP": ["首页", "投苗管理", "饲养管理", "物资领用", "任务管理", "免疫管理", "保健管理", "新开育肥场", "生物安全", "防疫管理", "上市管理"]}


		#缺陷趋势图
		bugTrend_bar_charts = bugTrend_bar(bugEveryTrend).render_embed()

		progress_bar_charts = progress_bar(public_list).render_embed()
		reproduction_bar_charts = progress_bar(reproduction_list).render_embed()
		fattenone_bar_charts = progress_bar(fattenone_list).render_embed()
		purchaseAndsale_bar_charts = progress_bar(purchaseAndsale_list).render_embed()
		purchaseAndsaleapp_bar_charts = progress_bar(purchaseAndsaleapp_list).render_embed()
		fattenoneapp_bar_charts = progress_bar(fattenoneapp_list).render_embed()
		fattentwo_bar_charts = progress_bar(fattentwo_list).render_embed()
		fattentwoapp_bar_charts = progress_bar(fattentwoapp_list).render_embed()
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
			bar_base(sqlproduct.format(moduleid), sql.format(moduleid), projectsql.format(moduleid),
			         sqltoday.format(moduleid))))


# class ChartView(APIView):
#     def get(self, request, *args, **kwargs):
#         moduleid = (kwargs["moduleid"])
#         # print(json.loads(bar_base(sql.format(moduleid,moduleid,moduleid,moduleid,moduleid,moduleid))))
#         data = JsonResponse(json.loads(bar_base(sql.format(moduleid,moduleid,moduleid,moduleid,moduleid,moduleid),sqlmodule.format(moduleid))))
#         return render(request,"index6.html",data)


class IndexView(APIView):
	def get(self, request, *args, **kwargs):
		return HttpResponse(content=open("./templates/index8.html", encoding="utf-8").read())


class CultivatesView(APIView):
	def get(self, request, *args, **kwargs):
		moduleid = (kwargs["moduleid"])
		return JsonResponse(json.loads(
			bar_base(sqlmodule.format(moduleid), sqlmodulesum.format(moduleid), progresssql.format(moduleid),
			         sqlproducttoday.format(moduleid))))


class ModuleView(APIView):
	def get(self, request, *args, **kwargs):
		data = charts_base(sqldate)
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
