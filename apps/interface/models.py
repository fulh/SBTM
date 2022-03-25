from django.db import models
from smart_selects.db_fields import GroupedForeignKey
from django.contrib.auth.models import User
from users.models import UserProfile
# Create your models here.

class Project(models.Model):
	id = models.AutoField(primary_key=True)
	name =  models.CharField('项目名称',max_length=32,unique=True,null=False)
	proj_owner = models.CharField('项目负责人',max_length=32)
	test_owner = models.CharField('测试负责人',max_length=32)
	dev_owner = models.CharField('开发负责人',max_length=32)
	desc = models.TextField('描述',max_length=120)
	create_time = models.DateTimeField('创建时间',auto_now_add=True)
	update_time = models.DateTimeField('创建时间',auto_now=True,null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '项目信息表'
		verbose_name_plural = verbose_name


# 模块
class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('模块名称', max_length=50, null=False)
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    test_owner = models.CharField('测试负责人', max_length=50, null=False)
    desc = models.CharField('简要描述', max_length=100, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '模块信息表'
        verbose_name_plural = '模块信息表'


# 测试用例
class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    case_name = models.CharField('用例名称', max_length=50, null=False)  # 如 register
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    belong_module = GroupedForeignKey(Module, "belong_project", on_delete=models.CASCADE, verbose_name='所属模块')
    request_data = models.CharField('请求数据', max_length=1024, null=False, default='')
    uri = models.CharField('接口地址', max_length=1024, null=False, default='')
    assert_key = models.CharField('断言内容', max_length=1024, null=True)
    maintainer = models.CharField('编写人员', max_length=1024, null=False, default='')
    extract_var = models.CharField('提取变量表达式', max_length=1024, null=True)  # 示例：userid||userid": (\d+)
    request_method = models.CharField('请求方式', max_length=1024, null=True)
    status = models.IntegerField(null=True, help_text="0：表示有效，1：表示无效，用于软删除")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='责任人', null=True)

    def __str__(self):
        return self.case_name

    class Meta:
        verbose_name = '测试用例表'
        verbose_name_plural = '测试用例表'
