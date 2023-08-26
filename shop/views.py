import json

from django.core.paginator import Paginator
from django.shortcuts import render

from shop.models import Flowers


def home(request):
    bouquets_list = Flowers.objects.all()
    # Постраничная разбивка с 3 букетами на страницу
    paginator = Paginator(bouquets_list, 3)
    page_numer = request.GET.get('page', 1)
    bouquets_obj = paginator.get_page(page_numer)
    print(bouquets_obj.object_list)

    context = {
        'object_list': bouquets_obj.object_list,
        'title': '<Букеты - интернет магазин>',
        'bouquets': bouquets_obj,
    }
    return render(request, 'shop/home.html', context)


def contacts(request):
    # в переменной request хранится информация о методе, который отправлял пользователь,
    # а также передается информация, которую заполнил пользователь

    if request.method == 'POST':
        data = {}
        name = request.POST.get('name')
        email = request.POST.get('phone')
        message = request.POST.get('message')
        data = {
            'name': name,
            'email': email,
            'message': message
        }

        with open('data_massage.json', 'a', encoding='utf-8') as fp:
            json.dump(data, fp)
    return render(request, 'shop/contacts.html')


def detail_info(request, pk):
    item = Flowers.objects.get(pk=pk)
    cat = item.category
    pr = item.price
    img = item.Imag
    context = {
        'title': f'Букет -  {item.name}',
        'category': cat,
        'price': pr,
        'img': img
    }
    print(context)
    return render(request, 'shop/detail_info.html', context)
