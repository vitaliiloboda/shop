import random
from django.db.models import Q
# from django.core import cache
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from basketapp.models import Basket
from mainapp.models import Product, ProducCategory
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'categories'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProducCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)

        return links_menu

    return ProducCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category_item = cache.get(key)
        if category_item is None:
            category_item = get_object_or_404(ProducCategory, pk=pk)
            cache.set(key, category_item)
        return category_item
    return get_object_or_404(ProducCategory, pk=pk)


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return None


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related('category')[:3]
    return products_list

@never_cache
def index(request):
    is_home = Q(category__name='дом')
    is_office = Q(category__name='офис')
    context = {
        'title': 'Главная',
        # 'products': Product.objects.all()[:4],
        'products': Product.objects.filter(
            is_home | is_office
        ),
        # 'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': 'Контакты',
        # 'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)


# class ProductsListView(ListView):
#     template_name = 'mainapp/products_list.html'
#     model = Product
#     paginate_by = 2
#
#     def _get_links_menu(self):
#         return ProducCategory.objects.filter(is_active=True)
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         category_pk = self.kwargs.get('pk')
#         if category_pk and category_pk > 0:
#             queryset = queryset.filter(category__pk=category_pk)
#         return queryset
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, **kwargs)
#         category_pk = self.kwargs.get('pk')
#         context_data['links_menu'] = self._get_links_menu()
#         context_data['title'] = 'Продукты'
#         if category_pk is None:
#             hot_product = get_hot_product()
#             same_products = get_same_products(hot_product)
#             context = {
#                 'links_menu': self._get_links_menu(),
#                 'title': 'Продукты',
#                 'hot_product': hot_product,
#                 'same_products': same_products,
#             }
#             rendered_string = render_to_string('mainapp/products_list.html', context=context)
#             return HttpResponse(self.request, rendered_string)
#
#         elif category_pk == 0:
#             context_data['category'] = {
#                 'name': 'все',
#                 'pk': 0
#             }
#         else:
#             context_data['category'] = ProducCategory.objects.get(pk=category_pk)
#         return context_data

@cache_page(3600)
def products(request, pk=None, page=1):
    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0
            }
        else:
            category_item = get_category(pk)
            products_list = Product.objects.filter(category__pk=pk)

        # page = request.GET.get('p', 1)
        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links_menu,
            'title': 'Продукты',
            'category': category_item,
            'products': products_paginator,
            # 'basket': get_basket(request.user)
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'links_menu': links_menu,
        'title': 'Продукты',
        'hot_product': hot_product,
        'same_products': same_products,
        # 'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    links_menu = get_links_menu()

    context = {
        'product': get_object_or_404(Product, pk=pk),
        # 'basket': get_basket(request.user),
        'links_menu': links_menu,
    }

    return render(request, 'mainapp/product.html', context)
