from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# In Django, a view is a Python function or class that receives a web request and returns a web response, such as an HTML page, a redirect, or an error page. 
# Views contain the logic for processing the request, interacting with the database (Models), and generating the final content (Templates).


def home_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    # this function return "String of HTML code" as httpResponse
    # return HttpResponse("<h1>Abdullah Abu Bakar<h1/>")
    return render(request, "home.html", {})


def contact_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Contact Page<h1/>")
    return render(request, "contact.html", {})


def about_view(request, *args, **kwargs):
    # return HttpResponse("<h1>About Page<h1/>")
    my_context = {
        "my_name": "Abdullah Abu Bakar",
        "my_phone": 12312,
        "my_html": "<h1>Hello World</h1>",
        "my_list": [21, 102, 12, 14, 16, "Ali"]
    }
    return render(request, "about.html", my_context)


def social_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Social Page<h1/>")
    return render(request, "social.html", {})
