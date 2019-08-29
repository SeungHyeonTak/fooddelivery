from django.shortcuts import render, get_object_or_404
from .models import *


def category_list(request):
    categorys = Category.objects.all()
    return render(request, 'food/category_list.html', {
        'categorys': categorys,
    })


def category_detail(request, pk):
    cate_detail = get_object_or_404(Category, pk=pk)
    return render(request, 'food/category_detail.html', {
        'cate_detail': cate_detail,
    })


def shop_detail(request, pk):
    shop_detail = get_object_or_404(Shop, pk=pk)
    return render(request, 'food/shop_detail.html', {
        'shop_detail': shop_detail,
    })