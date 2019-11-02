from django.shortcuts import render
import json
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .models import Discussion
from Account.models import Account
from datetime import datetime

@login_required
def room(request,disc_slug='last'):

    if disc_slug=='last':
        discs= Discussion.objects.filter(slug__contains=request.user.id)
        disc_slug = discs[len(discs)-1].slug

    # FOR ACTIVE OTHER USER : other active user infos
    this_disc = Discussion.objects.get_or_create(slug= disc_slug)[0]
    tst=[int(elt) for elt in list(disc_slug)[1:] if int(elt)!=request.user.id][0]
    other_user_active = Account.objects.get(id=tst)

    ln_msgs = len(this_disc.messages.all())-1

    if ln_msgs>0:
        other_active_all_msgs = this_disc.messages.all()
        other_active_last_msg = other_active_all_msgs[ln_msgs].content

        other_active_msg_date = str(other_active_all_msgs[ln_msgs].timestamp.day) + ' ' +\
                                str(other_active_all_msgs[ln_msgs].timestamp.strftime('%b'))

    else:
        other_active_last_msg = ''
        time_now = datetime.now()
        other_active_msg_date = str(time_now.day) + ' ' + str(time_now.strftime('%b'))

    other_active_name = other_user_active.first_name + ' '+ other_user_active.last_name



    # FOR CHAT HISTORY: Search for other accounts that discussed with active user
    user_discussions = Discussion.objects.filter(slug__contains=request.user.id)
    Discussions_without_other_active_user = [elt for elt in user_discussions if elt.slug != disc_slug]

    deleting = [elt.delete() for elt in Discussions_without_other_active_user if len(elt.messages.all()) == 0]

    user_discussions_slugs = [elt.slug for elt in Discussions_without_other_active_user]
    other_users_id = [[int(elt) for elt in list(slg)[1:] if int(elt)!=request.user.id][0] for slg in user_discussions_slugs]

    other_users_account = [Account.objects.get(id=elt) for elt in other_users_id]

    nb_msg = [len(elt.messages.all()) for elt in Discussions_without_other_active_user]

    last_msg = [elt.messages.all()[nb-1].content for elt,nb in zip(Discussions_without_other_active_user,nb_msg) if nb > 0]

    last_msg_dates = [str(elt.messages.all()[nb-1].timestamp.day) + ' ' +
                      str(elt.messages.all()[nb-1].timestamp.strftime('%b')) for elt,nb in zip(Discussions_without_other_active_user,nb_msg) if nb >0]
    last_msg_senders = [elt.first_name + ' '+ elt.last_name for elt in other_users_account]


    last_msg.reverse()
    last_msg_senders.reverse()
    last_msg_dates.reverse()
    user_discussions_slugs.reverse()

    this_disc.save()


    return render(request,'messaging/room.html', {
        'room_slug': mark_safe(json.dumps(disc_slug)),
        'user_slug': mark_safe(json.dumps(request.user.slug)),
        'historical_disc_data': zip(last_msg, last_msg_senders, last_msg_dates, user_discussions_slugs),
        'other_active_name': other_active_name,
        'other_active_last_msg': other_active_last_msg,
        'other_active_msg_date': other_active_msg_date,
        })



