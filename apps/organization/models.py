#-*-coding:utf-8 -*-，
from django.db import models

from datetime import datetime

from django.db import models


class CityDict(models.Model):
    name = models.CharField('城市',max_length=20)
    desc = models.CharField('描述',max_length=200)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural= verbose_name
    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    ORG_CHOICES = (
        ("pxjg", u"培训机构"),
        ("gx", u"高校"),
        ("gr", u"个人"),
    )
    name = models.CharField('机构名称',max_length=50)
    desc = models.TextField('机构描述')
    category = models.CharField(max_length=20, choices=ORG_CHOICES, verbose_name=u"机构类别", default="pxjg")
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    image = models.ImageField('封面图',upload_to='org/%Y%m',max_length=100)
    address = models.CharField('机构地址',max_length=150,)
    city = models.ForeignKey(CityDict,verbose_name='所在城市',on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='新增时间')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        #获取机构的教师数
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name='所属机构',on_delete=models.CASCADE)
    name = models.CharField('教师名',max_length=50)
    work_years = models.IntegerField('工作年限',default=0)
    work_company = models.CharField('就职公司',max_length=50)
    work_position = models.CharField('公司职位',max_length=50)
    points = models.CharField('教学特点',max_length=50)
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    add_time = models.DateTimeField(default=datetime.now)

    # def go_to(self):
    #     from django.utils.safestring import mark_safe
    #     return mark_safe("<a href='http://wwww.baidu.com'>跳转</a>")
    #
    # go_to.short_description = "跳转"

    # 显示新的一列为链接
    def qianshou(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='signNotice/%s''>签收</a>" % self.id)  # content.id是当前记录对应的ID

    qianshou.short_description = '操作'

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name



    def __str__(self):
        return "[{0}]的教师: {1}".format(self.org, self.name)


