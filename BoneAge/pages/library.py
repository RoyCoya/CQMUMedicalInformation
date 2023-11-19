from django.conf import settings
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from BoneAge.apis.public_func import login_check
from BoneAge.models import Task

# 所有记录
def library(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    tasks = Task.objects.all().order_by('-allocated_datetime')

    current_page_number = request.GET.get('page', 1)
    pages = Paginator(tasks, 15)
    page_numbers = pages.get_elided_page_range(current_page_number)
    tasks = pages.page(current_page_number)
    

    context = {
        'tasks' : tasks,
        'page_numbers' : page_numbers,
        'has_previos' : tasks.has_previous(),
        'has_next' : tasks.has_next(),
    }
    return render(request,'BoneAge/library/library.html',context)