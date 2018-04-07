from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CatForm, LoginForm, SignUpForm, ToyForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, authenticate # we add redirect with auth
import requests

# Create your views here.

from .models import Cat, Toy


def index(request):
	# context = {'cats': cats}
	cats = Cat.objects.all()
	form = CatForm()
	return render(request, 'index.html', {'cats': cats, 'form': form})



def show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    form = ToyForm()
    return render(request, 'show.html', {'cat': cat, 'form': form})


# now that our model dictates our form we can write less code in our post route
def post_cat(request):
	form = CatForm(request.POST)
	if form.is_valid:
		cat = form.save(commit = False)
	cat.user = request.user
	cat.save()
	return HttpResponseRedirect('/')



def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user. is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def like_cat(request):
    cat_id = request.GET.get('cat_id', None)
    likes = 0
    if (cat_id):
        cat = Cat.objects.get(id=int(cat_id))
        if cat is not None:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

def edit_cat(request, cat_id):
    instance = get_object_or_404(Cat, id=cat_id)
    form = CatForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('show', cat_id)
    return render(request, 'edit_cat.html', {'cat':instance, 'form': form})

# django doesn't have a built-in method for delete
#pk = primary key
def delete_cat(request, cat_id):
    if request.method == 'POST':
        instance = Cat.objects.get(pk=cat_id)
        instance.delete()
        return redirect('index')

def create_toy(request, cat_id):
    form = ToyForm(request.POST)
    if form.is_valid():
        try: 
            toy = Toy.objects.get(name=form.data.get('name'))
        except:
            toy = None
        if toy is None:
            toy = form.save()
    #this is basically a find-or-create
        cat = Cat.objects.get(pk=cat_id)
        toy.cats.add(cat)
        return redirect('show_toy', toy.id)
    else: 
        return redirect('show', cat_id)

def show_toy(request, toy_id):
    toy = Toy.objects.get(pk=toy_id)
    cats = toy.cats.all()
    return render(request, 'show_toy.html', {'toy': toy, 'cats': cats})

def api(request):
    payload = {'key': 'Mjk0MTkz'}
    res = requests.get('http://thecatapi.com/api/images/get', params=payload)
    return render(request, 'api.html', {'imageurl': res.url})













