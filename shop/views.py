import json

from django.shortcuts import render

from shop.models import Flowers


def home(request):
    print(f'Я - {request}')
    fl = Flowers.objects.all()[:5]
    print(fl)
    return render(request, 'shop/home.html')


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
