from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from shop.forms import FlowersForm, VersionForm
from shop.models import Flowers, Blog, Versions, Category
from shop.serives import write_json_message, get_category_cache


class CategoryListView(ListView):
    model = Category

    extra_context = {
        'title': 'Список категорий'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_category_cache(context)
        return context


class FlowersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'shop.view_flowers'
    paginate_by = 3
    model = Flowers

    extra_context = {
        'title': 'Букеты - интернет магазин'
    }

    def get_queryset(self):
        """
        Выводит только созданные или измененные user-ом букеты
        :return: queryset
        """
        queryset = super().get_queryset().filter(employee_id=self.request.user.pk, )

        return queryset


class FlowersCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Flowers
    form_class = FlowersForm
    permission_required = 'shop.add_flowers'
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


class FlowersUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'shop.change_flowers'
    model = Flowers
    form_class = FlowersForm
    success_url = reverse_lazy('shop:flowers_list/')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        content_type = ContentType.objects.get_for_model(Flowers)
        permission = Permission.objects.get(
            codename="set_published",
            content_type=content_type,
        )

        # user.user_permissions.add(perm_object)
        # print(user.has_perm('shop.change_flowers'))

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


class FlowersDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Flowers
    success_url = reverse_lazy('shop:flowers_list/')
    permission_required = 'shop.delete_flowers'


def contacts(request):
    # в переменной request хранится информация о методе, который отправлял пользователь,
    # а также передается информация, которую заполнил пользователь

    if request.method == 'POST':
        # data = {}
        name = request.POST.get('name')
        email = request.POST.get('phone')
        message = request.POST.get('message')
        data = {
            'name': name,
            'email': email,
            'message': message
        }
        # сервисная
        write_json_message(data)
    return render(request, 'shop/contacts.html')


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('name', 'content', 'is_published', 'image')
    success_url = reverse_lazy('shop:blog_list/')

    # login_url = reverse_lazy('shop:blog_list/')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()
        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
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


@permission_required('shop.change_flowers')
def toggle_activity_fl(request, pk):
    flowers_item = get_object_or_404(Flowers, pk=pk)
    if flowers_item.is_published:
        flowers_item.is_published = False
    else:
        flowers_item.is_published = True
    flowers_item.save()
    return redirect(reverse('shop:flowers_list/'))
