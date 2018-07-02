from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm
from .Core import Crawler

def index(request):
    if request.method=="POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            SearchResult=Crawler().search(form.cleaned_data['search'],form.cleaned_data['depth'],form.cleaned_data['site'])
            '''SearchResult=[
                {
                    'H':'header',
                    'A':'Link',
                    'P':'Paragraph'
                }
            ]'''
            return render(request,'index.html',{'SearchResult':SearchResult,'Searched':True})


    else:
        form=SearchForm()
        return render(request,'index.html',{'form':form,'Searched':False})