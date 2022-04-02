from django.shortcuts import render
from . import  models
# Create your views here.
from django.views import View

def test_case(request):
	if request.method == 'GET':
		models.TestCase.objects.filter()
	return