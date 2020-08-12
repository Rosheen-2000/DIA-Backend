from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import tools
from . import api
import json


# Create your views here.
def add_data(request):
	tools.add_data()
	return HttpResponse('添加成功')


def my_test(request):
	print(tools.decrypt(tools.encrypt('hgtttttt123321')))
	return HttpResponse('测试成功')


def login(request):
	name = request.POST.get('uname')
	pwd = request.POST.get('pwd')
	# print(name)
	# print(pwd)
	# print(request.method)
	msg, value = api.login(name, pwd)
	# print(result)
	return JsonResponse({'msg': msg, 'token': value})
	# return render(request, 'register.html', )