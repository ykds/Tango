
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse

from registration.backends.simple.views import RegistrationView
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserProfileForm
from datetime import datetime


# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context = {'categories':category_list, 'page_list': page_list}

    visitor_cookie_handler(request)
    context['visits'] = request.session['visits']
    return render(request, 'rango/index.html', context=context)


def abount(request):
    return render(request, 'rango/abount.html')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'rango/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(category__slug=self.kwargs.get('slug')).order_by('-views') # = Page.objects.filter(category=category)
        context.update({
            'pages': pages,
        })
        return context


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect('rango:index')
    return render(request, 'rango/add_category.html', context={'form': form})

@login_required
def like_category(request):
    category_id = None
    likes = 0
    if request.method == 'GET':
        category_id = request.GET['category_id']
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        category.likes += 1
        category.save()
        likes = category.likes
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)
    return render(request, 'rango/cats.html', {'cats': cat_list})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'slug': category_name_slug}))
        else:
            print(form.errors)
    context = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context)


class MyRegistrationVIew(RegistrationView):
    # 注册成功跳转
    def get_success_url(self, user=None):
        return reverse('rango:register_profile')

# 记录页面浏览数
def track_url(request):
    page_id = None
    if request.method == 'GET':
         page_id = request.GET.get('page_id')
    if page_id:
        try:
            page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('rango:index'))
        page.views += 1
        if page.first_visit == None:
            page.first_visit = page.last_visit = datetime.now()
        page.last_visit = datetime.now()
        page.save()
        return redirect(page.url)
    return redirect(reverse('rango:index'))

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse("rango:index"))
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'rango/profile_registration.html', context=context)


class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'rango/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        userprofile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})
        context.update({
            'selecteduser': user,
            'userprofile': userprofile,
            'form': form
        })
        return context

@login_required
def update_profile(request, username):
    user = get_object_or_404(User, username=username)
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    # 指定instance参数， 则使用已存在的对象来生成form对象，而不会生成新的对象
    form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
    if form.is_valid():
        form.save()
        return redirect('rango:profile', user.pk)


class ListProfiles(ListView):
    model = UserProfile
    template_name = 'rango/list_profiles.html'
    context_object_name = 'profiles'



def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits