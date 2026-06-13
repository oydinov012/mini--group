from django.http import HttpResponse

def home_page(request):
    return HttpResponse("<h1>Fintechhub mini group 16!</h1>")