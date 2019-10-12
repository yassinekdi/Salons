from django.shortcuts import render
from django.http import HttpResponse
from Account.models import Account
from django.db.models import Q


def ProfilePage(request):

        user = request.user
        context={'profile_page': user}
        return render(request,'Attendees/profile_page.html', context)


def Profiles(request,slug):
    user = Account.objects.filter(slug__icontains=slug)[0]
    context = {'profile_page': user}
    return render(request, 'Attendees/profile_page.html', context)

def searchpage(request):

    if request.method=='POST':
        query = request.POST['q']
        users = Account.objects.filter(Q(last_name__icontains=query) | Q(first_name__icontains=query))
        if len(users)>0:
            context = {'users': users}
            return render(request,'Attendees/Ids.html', context)
        else:
            return HttpResponse("{} doesn't exist".format(query))
    #
    return render(request,'Attendees/Ids.html')
