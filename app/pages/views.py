from django.shortcuts import render
import datetime

# Create your views here.


def home_view(request, *args, **kwargs):
    print(args, kwargs)
    # print(request.user)
    print(datetime.datetime.now())

    return render(request, 'home.html', {})


def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})


def contact_view(request, *args, **kwargs):
    return render(request, 'contact.html', {})

