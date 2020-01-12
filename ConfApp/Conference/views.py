from django.shortcuts import render, redirect
from .forms import Conf_registration
from .models import Conference

def entry(request):
    return render(request,'Conference/Entry.html')



def new_conf(request):
    form = Conf_registration()
    context = {'form': form}


    if request.POST:
        form = Conf_registration(request.POST)

        if form.is_valid():
            print('IN FORM IS VALID NEW CONF')
            name_conf = form.cleaned_data.get('name')
            website_conf = form.cleaned_data.get('conf_webpage')
            start_date = form.cleaned_data.get("starting_date")
            finish_date = form.cleaned_data.get("finishing_date")
            new_conference = Conference.objects.create(name=name_conf, website=website_conf, start_date=start_date,
                                                       finish_date=finish_date)
            new_conference.superusers.add(request.user)
            new_conference.users.add(request.user)

            context = {'form': form}
            return redirect('homepage')
    return render(request, 'Conference/new_conf.html', context)
