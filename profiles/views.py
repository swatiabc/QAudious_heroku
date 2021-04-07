from django.shortcuts import render

# Create your views here.
def profile_page(request):
    if request.user.is_authenticated:
        return render(request,"profile.html")
    else:
        return render(request,"signin_home.html")


def contact_page(request):
    return render(request,"contact.html")

def about_page(request):
    return render(request,"about.html")

def mentor_page(request):
    return render(request,"mentor.html")