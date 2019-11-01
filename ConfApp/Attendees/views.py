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
    my_account_id = request.user.id
    if request.method=='POST':
        query = request.POST['q']
        users = Account.objects.filter(Q(last_name__icontains=query) | Q(first_name__icontains=query))
        discussion_slug1 = [sorted([my_account_id,elt.id]) for elt in users]
        discussion_slug2 = ['s'+''.join([str(elt[0]), str(elt[1])]) for elt in discussion_slug1]
        # other_user_slug = [elt.id for elt in users]

        if len(users)>0:
            context = {'users': zip(users,discussion_slug2)}
            return render(request,'Attendees/Ids.html', context)
        else:
            return HttpResponse("{} doesn't exist".format(query))
    #
    return render(request,'Attendees/Ids.html')

