from django.shortcuts import render
from django.core.paginator import Paginator
from .models import ReadDetail


# Create your views here.
def read_info(request):
    read_info = ReadDetail.objects.all()
    paginator = Paginator(read_info, 10)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    pages = paginator.get_page(page_num)
    currentr_page_num = pages.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {}
    context['pages'] = pages
    context['page_range'] = page_range
    context['read_info'] = pages.object_list
    return render(request, 'read_statistics/read_info.html', context)
