from django.shortcuts import render

def index(request):
    """
    View to render the main index/hub page.
    """
    context = {}
    return render(request, 'index.html', context)