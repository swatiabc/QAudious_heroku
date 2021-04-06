from django.shortcuts import render

# Create your views here.
def profile_page(request):
    return render(request,"profile.html")