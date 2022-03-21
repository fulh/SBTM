#-*-coding:utf-8 -*-，

import xadmin

from .models import EmailVerifyRecord,Banner
from charts.models import Progress,BarCharts
from xadmin import views

from xadmin.views.base import CommAdminView
from course.models import Course,Lesson,Video,CourseResource,CourseOrg
from operation.models import UserAsk,CourseComments,UserFavorite,UserMessage,UserCourse
from charts.models import Progress,BarCharts


# 创建xadmin的最基本管理器配置，并与view绑定
# class BaseSetting(object):
#     # 开启主题功能
#     enable_themes = True
#     use_bootswatch = False

# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '后台管理界面'
    # 修改footer
    site_footer = '测试试验平台'
    # 收起菜单
    menu_style = 'accordion'

    # def get_site_menu(self):
    #     return (
    #         {'title': '测试统计', 'icon': 'fa fa-arrows','menus': (
    #                 {'title': '进度统计', 'icon':'fa fa-area-chart','url': self.get_model_url(Progress, 'changelist')},
    #                 {'title': '缺陷统计','icon':'fa fa-bug','url': self.get_model_url(BarCharts, 'changelist')},
    #             {'title': '课程信息', 'url': self.get_model_url(Course, 'changelist')},
    #             {'title': '章节信息', 'url': self.get_model_url(Lesson, 'changelist')},
    #             {'title': '视频信息', 'url': self.get_model_url(Video, 'changelist')},
    #             {'title': '课程资源', 'url': self.get_model_url(CourseResource, 'changelist')},
    #             # {'title': '课程评论', 'url': self.get_model_url(CourseOrg, 'changelist')},
    #         )},
    #         {'title': '机构管理', 'menus': (
    #             {'title': '所在城市', 'url': self.get_model_url(UserAsk, 'changelist')},
    #             # {'title': '机构讲师', 'url': self.get_model_url(CourseComments, 'changelist')},
    #             # {'title': '机构信息', 'url': self.get_model_url(UserFavorite, 'changelist')},
    #         )},
    #
    #     )
    def get_site_menu(self):
        return [
            {
                'title': 'Bug统计',
                'icon': 'fa fa-area-chart',
                'menus': (
                    {
                        'title': 'Bug表',
                        'icon': 'fa fa-area-chart',
                        'url':self.get_model_url(Course, 'changelist'),  # 自定义跳转列表

                    },)
            }

        ]



#xadmin中这里是继承object，不再是继承admin
class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 搜索的字段
    search_fields = ['code', 'email', 'send_type']
    # 过滤
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url','index', 'add_time']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url','index', 'add_time']




xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)

# 将基本配置管理与view绑定
# xadmin.site.register(views.BaseAdminView,BaseSetting)

# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)