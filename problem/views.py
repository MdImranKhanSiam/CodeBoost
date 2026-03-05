from django.shortcuts import render

# Create your views here.


def problems(request):
    
    context = {
        
    }

    return render(request, 'home/problems.html', context)