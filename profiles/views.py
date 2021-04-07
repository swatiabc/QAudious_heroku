from django.shortcuts import render

# Create your views here.
def profile_page(request):
    if request.user.is_authenticated:
        return render(request,"profile.html")
    else:
        return render(request,"signin_home.html")