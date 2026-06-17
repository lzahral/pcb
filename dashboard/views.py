from django.shortcuts import render

# Create your views here.


def index(request):
    print('test')
    return render(request, "dashboard/index.html")

def about_us(request):
    return render(request, "dashboard/about_us.html")

def contact_us(request):
    return render(request, "dashboard/contact_us.html")

def technical_guide(request):
    return render(request, "dashboard/technical_guide.html")
