import json

from django.shortcuts import render

from shop.models import Flowers, Category


def home(request):
    context = {
        'object_list': Flowers.objects.all()[:8],
        'title': '<Букеты - интернет магазин>'
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
    context = {
        'title': f'Букет -  {item.name}',
        'category': cat,
        'price' : pr
    }
    print(context)
    return render(request, 'shop/detail_info.html', context)
