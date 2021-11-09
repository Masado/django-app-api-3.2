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


# def test_view(request, *args, **kwargs):
#     from django.conf import settings
#     if request.method == "POST" and "base_dir" in request.POST:
#         print("ping")
#         base_dir = settings.BASE_DIR
#         print(base_dir)
#         return render(request, 'test.html', {"base_dir": base_dir})
#     return render(request, 'test.html',)
