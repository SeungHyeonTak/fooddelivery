from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView
from .models import Category, Shop, Review, Order, Item, OrderItem
from .forms import ReviewForm, OrderForm, PayForm
from secret import *


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
    print(shop_detail.category)
    return render(request, 'food/shop_detail.html', {
        'shop_detail': shop_detail,
        'naver_map': naver_map,
    })


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        self.shop = get_object_or_404(Shop, pk=self.kwargs['pk'])

        review = form.save(commit=False)
        review.shop = self.shop
        review.author = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return self.shop.get_absolute_url()


review_new = ReviewCreateView.as_view()


@login_required
def order_new(request, shop_pk):
    item_qs = Item.objects.filter(shop__pk=shop_pk, id__in=request.GET.keys())

    quantity_dict = request.GET.dict()
    quantity_dict = {int(k): int(v) for k, v in quantity_dict.items()}

    item_order_list = []
    for item in item_qs:
        quantity = quantity_dict[item.pk]
        order_item = OrderItem(quantity=quantity, item=item)  # 사용자 주소&전화번호 받아오기
        item_order_list.append(order_item)

    amount = sum(order_item.amount for order_item in item_order_list)
    instance = Order(name='배달주문건', amount=amount)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=instance)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for order_item in item_order_list:
                order_item.order = order
            OrderItem.objects.bulk_create(item_order_list)

            return redirect('food:order_pay', shop_pk, str(order.merchant_uid))
    else:
        form = OrderForm(instance=instance)

    return render(request, 'food/order_form.html', {
        'item_order_list': item_order_list,
        'form': form,
    })


@login_required
def order_pay(request, shop_pk, merchant_uid):
    order = get_object_or_404(Order, user=request.user, merchant_uid=merchant_uid, status='ready')

    if request.method == 'POST':
        form = PayForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PayForm(instance=order)

    return render(request, 'food/order_pay.html', {
        'form': form,
    })


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')
