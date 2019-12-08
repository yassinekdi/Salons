from django.shortcuts import render

def first(request):
    return render(request,'Calendar/calendar.html')
