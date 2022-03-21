from django.db import models

# Create your models here.
class Progress(models.Model):

	class Meta:
		verbose_name = u"测试进度统计"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.Meta.verbose_name



class BarCharts(models.Model):

	class Meta:
		verbose_name = u"缺陷统计"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.Meta.verbose_name
