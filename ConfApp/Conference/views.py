from django.shortcuts import render, redirect
from .forms import Conf_registration, Theme_formset
from .models import Conference, Theme

def entry(request):
    return render(request,'Conference/Entry.html')



def new_conf(request):
    form = Conf_registration()
    theme_form = Theme_formset()
    context = {'form': form,
               'theme_forms': theme_form }


    if request.POST:
        form = Conf_registration(request.POST)
        theme_form = Theme_formset(request.POST)
        if form.is_valid() and theme_form.is_valid():
            print('FORMS ARE VALID')
            name_conf = form.cleaned_data.get('name')
            website_conf = form.cleaned_data.get('conf_webpage')
            start_date = form.cleaned_data.get("starting_date")
            finish_date = form.cleaned_data.get("finishing_date")
            new_conference = Conference.objects.create(name=name_conf, website=website_conf, start_date=start_date,
                                                       finish_date=finish_date)
            new_conference.superusers.add(request.user)
            new_conference.users.add(request.user)

            # Themes
            for themes in theme_form:
                title = themes.cleaned_data.get('theme_title')
                if title is not None:
                    new_theme = Theme.objects.create(title=title)
                    new_conference.themes.add(new_theme)
                    print('CREATED!')

            return redirect('homepage')
    return render(request, 'Conference/new_conf.html', context)
