import json

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from shop.models import Flowers, Blog


class FlowersListView(ListView):
    paginate_by = 3
    model = Flowers

    extra_context = {
        'title': 'Букеты - интернет магазин'
    }


# def home(request):
#     bouquets_list = Flowers.objects.all()
#     # Постраничная разбивка с 3 букетами на страницу
#     paginator = Paginator(bouquets_list, 3)
#     page_numer = request.GET.get('page', 1)
#     bouquets_obj = paginator.get_page(page_numer)
#
#     context = {
#         'object_list': bouquets_obj.object_list,
#         'title': '<Букеты - интернет магазин>',
#         'bouquets': bouquets_obj,
#     }
#     return render(request, 'shop/flowers_list.html', context)


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


class FlowersDetailView(DetailView):
    model = Flowers


# def detail_info(request, pk):
#     item = Flowers.objects.get(pk=pk)
#     cat = item.category
#     pr = item.price
#     img = item.Imag
#     context = {
#         'title': f'Букет -  {item.name}',
#         'category': cat,
#         'price': pr,
#         'img': img
#     }
#     return render(request, 'shop/flowers_detail.html', context)


class BlogCreateView(CreateView):
    model = Blog
    fields = ('name', 'content', 'is_publication', 'image')
    success_url = reverse_lazy('shop:blog_list/')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()
        return super().form_valid(form)


class BlogListView(ListView):
    paginate_by = 2
    model = Blog
    # не работает пагинатор
    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print(context_data)
        context_data['page_obj'] = Blog.objects.filter(is_publication=True)
        return context_data


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('name', 'content', 'is_publication', 'image')

    # как вернуть на редактирование статьи

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['pk'] = self.object.pk
    #     return context
    success_url = reverse_lazy('shop:blog_list/')

    # def get_success_url(self):
    #     return reverse('shop:detail_list/', args=[self.object.pk])


def form_valid(self, form):
    if form.is_valid():
        new_blog = form.save()
        new_blog.slug = slugify(new_blog.name)
        new_blog.save()
    return super().form_valid(form)


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('shop:blog_list/')


def toggle_activity(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_publication:
        blog_item.is_publication = False
    else:
        blog_item.is_publication = True
    blog_item.save()
    return redirect(reverse('shop:blog_list/'))
