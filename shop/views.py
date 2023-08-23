import json

from django.shortcuts import render


def home(request):
    print(request)
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
