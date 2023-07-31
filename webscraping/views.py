from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse

from .script.index import get_trending, get_subjects, get_subject

# Page
def home(request):
    
    return render(request, 'templates/webscraping/index.html', {'trending': trending})

# API 
def trending(request):
    trending = get_trending()
    data = {"data": trending}
    return JsonResponse(data)

# API
def subjects(request):
    subjects, urls = get_subjects()
    data = {"data": subjects, 'urls': urls}

    return JsonResponse(data)

# Page
def subject_page(request, subject):


    return render(request, 'templates/webscraping/subject.html')

# API
def subject(request, pk):
    books, name = get_subject(pk)
    data = {'data': books, 'subject': name}

    return JsonResponse(data)