from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def science(request):
    return render(request, 'science.html', {'active_menu': 'science'})
