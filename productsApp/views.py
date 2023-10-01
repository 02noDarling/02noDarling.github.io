from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Product


# Create your views here.
@require_http_methods(['GET','POST'])
def products(request, productName):
    if productName == '家用机器人':
        productName = 'robot'
    elif productName == '智能监控':
        productName = 'monitor'
    elif productName == '人脸识别解决方案':
        productName = 'face'
    submenu=productName
    if productName == 'robot':
        productName = '家用机器人'
    elif productName == 'monitor':
        productName = '智能监控'
    elif productName == 'face':
        productName = '人脸识别解决方案'
    # if request.method == "POST":
    #     keyword = request.POST.get('keyword')
    #     productList = Product.objects.filter(title__contains=keyword)
    #     productName= 'robot'
    # else:
    #     productList = Product.objects.all().filter(
    #         productType=productName).order_by('-publishDate')
    productList = Product.objects.all().filter(
        productType=productName).order_by('-publishDate')

    p = Paginator(productList, 2)
    if p.num_pages <= 1:
        pageData = ''
    else:
        page = int(request.GET.get('page', 1))
        productList = p.page(page)
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:
            right = page_range[page:page + 2]
            print(total_pages)
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            right = page_range[page:page + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        pageData = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }

    return render(
        request, 'productList.html', {
            'active_menu': 'products',
            'sub_menu': submenu,
            'productName': productName,
            'productList': productList,
            'pageData': pageData,
        })


def productDetail(request, id):
    product = get_object_or_404(Product, id=id)
    product.views += 1
    product.save()
    return render(request, 'productDetail.html', {
        'active_menu': 'products',
        'product': product,
    })

def search(request):
    keyword=request.GET.get('keyword')
    productList=Product.objects.filter(title__contains=keyword)
    productName="关于"+"\""+keyword+"\""+"的搜索结果"
    # p = Paginator(productList, 2)
    # if p.num_pages <= 1:
    #     pageData = ''
    # else:
    #     page = int(request.GET.get('page', 1))
    #     productList = p.page(page)
    #     left = []
    #     right = []
    #     left_has_more = False
    #     right_has_more = False
    #     first = False
    #     last = False
    #     total_pages = p.num_pages
    #     page_range = p.page_range
    #     if page == 1:
    #         right = page_range[page:page + 2]
    #         print(total_pages)
    #         if right[-1] < total_pages - 1:
    #             right_has_more = True
    #         if right[-1] < total_pages:
    #             last = True
    #     elif page == total_pages:
    #         left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
    #         if left[0] > 2:
    #             left_has_more = True
    #         if left[0] > 1:
    #             first = True
    #     else:
    #         left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
    #         right = page_range[page:page + 2]
    #         if left[0] > 2:
    #             left_has_more = True
    #         if left[0] > 1:
    #             first = True
    #         if right[-1] < total_pages - 1:
    #             right_has_more = True
    #         if right[-1] < total_pages:
    #             last = True
    #     pageData = {
    #         'left': left,
    #         'right': right,
    #         'left_has_more': left_has_more,
    #         'right_has_more': right_has_more,
    #         'first': first,
    #         'last': last,
    #         'total_pages': total_pages,
    #         'page': page,
    #     }
    return render(
        request, 'productList.html', {
            'active_menu': 'products',
            'productName': productName,
            'productList': productList,
        })
