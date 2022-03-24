from django.contrib import admin

# Register your models here.
# organization/adminx.py

import xadmin

from .models import CityDict, CourseOrg, Teacher
# from .views import Sign_notice






class CityDictAdmin(object):
    '''城市'''

    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    '''机构'''

    list_display = ['name', 'desc', 'click_nums', 'fav_nums','add_time','city' ]
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums','city__name','address','add_time']
    # list_export = None
    list_export = []
    show_bookmarks = False


class TeacherAdmin(object):
    '''老师'''

    list_display = [ 'name','org', 'work_years', 'work_company','qianshou','add_time']
    search_fields = ['org__name', 'name', 'work_years', 'work_company']
    list_filter = ['org__name', 'name', 'work_years', 'work_company','click_nums', 'fav_nums', 'add_time']
    actions = ['change2computed',]

    def change2computed(modeladmin, request, queryset):  # 新建一个批量操作的函数，其中有三个参数：
        # 第一个参数是模型管理类，第二个request是请求，第三个queryset表示你选中的所有记录，这个函数里面会处理所有选中的queryset，所以要在操作之前用搜索或者过滤来选出需要修改的记录
        queryset.update(click_nums=1)  # 改变数据库表中，选中的记录的状态

    change2computed.short_description = 'Change compute state to computed'



    def qianshou_notice(request):
        qs = Teacher.objects.get(id=request)
        qs.fav_nums=3
        qs.save()
    #     # qs = qs.update(fav_nums=3)
    #     # return qs

# xadmin.site.register_view(r'test_view/(\d+)$', Sign_notice, name='test')
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)