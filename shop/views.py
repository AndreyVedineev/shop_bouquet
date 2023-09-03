import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from shop.forms import FlowersForm, VersionForm
from shop.models import Flowers, Blog, Versions


class FlowersListView(ListView):
    paginate_by = 3
    model = Flowers

    extra_context = {
        'title': 'Букеты - интернет магазин'
    }

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['page_obj'] = Flowers.objects.filter(employee=self.request.user)
    #     return context_data


class FlowersCreateView(LoginRequiredMixin, CreateView):
    model = Flowers
    form_class = FlowersForm
    success_url = reverse_lazy('shop:flowers_list/')
    login_url = reverse_lazy('shop:flowers_list/')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        Formset = inlineformset_factory(Flowers, Versions, form=VersionForm, extra=1)
        if self.request.method == "POST":
            context_data['formset'] = Formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = Formset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.employee = self.request.user
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class FlowersUpdateView(UpdateView):
    model = Flowers
    form_class = FlowersForm
    success_url = reverse_lazy('shop:flowers_list/')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        Formset = inlineformset_factory(Flowers, Versions, form=VersionForm, extra=1)
        if self.request.method == "POST":
            context_data['formset'] = Formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = Formset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.employee = self.request.user
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class FlowersDetailView(DetailView):
    model = Flowers


class FlowersDeleteView(DeleteView):
    model = Flowers
    success_url = reverse_lazy('shop:flowers_list/')


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


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('name', 'content', 'is_published', 'image')
    success_url = reverse_lazy('shop:blog_list/')
    login_url = reverse_lazy('shop:blog_list/')

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
        context_data['page_obj'] = Blog.objects.all()
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
    fields = ('name', 'content', 'is_published', 'image')

    # как вернуть на редактирование статьи

    success_url = reverse_lazy('shop:blog_list/')

    # def get_success_url(self):
    #     return reverse('shop:blog_update/', args=[self.object.pk])


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
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True
    blog_item.save()
    return redirect(reverse('shop:blog_list/'))
