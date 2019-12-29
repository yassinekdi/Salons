from django.shortcuts import render
import json
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .models import Discussion
from Account.models import Account
from datetime import datetime


@login_required
def room(request,disc_slug='last'):
    print('--- ROOM FUNCTION - MESSAGING -----')

    user_discussionsX = request.user.discussions.all()

    # When the message icon is pressed
    if disc_slug=='last':
        # If there were no previous discussions
        if (len(user_discussionsX) == 0):
            return render(request, 'messaging/room2.html')
        else:
            disc_slug = user_discussionsX[len(user_discussionsX) - 1].slug


    # Get other user in current discussion
    user2_id = [int(elt) for elt in disc_slug.split('n')[1:] if int(elt) != request.user.id][0]
    user2 = Account.objects.get(id=user2_id)

    this_disc,created = Discussion.objects.get_or_create(slug=disc_slug)

    all_msgs = this_disc.messages.all()
    # Updating the 2 users discussions if new discussion
    if created:
        this_disc.save()
        request.user.discussions.add(this_disc)
        request.user.save()

        user2.discussions.add(this_disc)
        user2.save()


    # Need name, date last msg & last msgS with the other user in current discussion
    name_user2_current_discussion = user2.first_name + ' '+ user2.last_name

    ln_msgs_current_discussion = len(this_disc.messages.all())-1

    if ln_msgs_current_discussion>-1:
        history=True
        current_discussion_last_msg = all_msgs[ln_msgs_current_discussion].content

        date_current_discussion = str(all_msgs[ln_msgs_current_discussion].timestamp.day) + ' ' +\
                                str(all_msgs[ln_msgs_current_discussion].timestamp.strftime('%b'))


    else:
        history=False
        current_discussion_last_msg = ''
        time_now = datetime.now()
        date_current_discussion = str(time_now.day) + ' ' + str(time_now.strftime('%b'))

    # For classes in template
    sent_msgs = [request.user.id == elt.sender.id for elt in all_msgs]
    date_msgs = [str(elt.timestamp.hour) + ':' + str(elt.timestamp.minute) + ' | ' + elt.timestamp.strftime(
        '%b') + ' ' + str(elt.timestamp.day) for elt in all_msgs]


    # Other users for other discussions - Need of names of senders, slugs, dates & last messages
    my_other_discussions = request.user.discussions.exclude(slug=disc_slug)
    deleting = [elt.delete() for elt in my_other_discussions if len(elt.messages.all()) == 0]

    my_other_discussions_filtered = request.user.discussions.exclude(slug=disc_slug)

    others_users = [elt.pariticipants.exclude(id=request.user.id)[0] for elt in my_other_discussions_filtered]
    names_other_discussions = [elt.first_name + ' '+ elt.last_name for elt in others_users]
    slugs_other_discussions = [elt.slug for elt in my_other_discussions_filtered]
    nb_msgs = [len(disc.messages.all()) for disc in my_other_discussions_filtered]
    lasts_msgs_other_discussions = [disc.messages.all()[nb-1].content for disc,nb in zip(my_other_discussions_filtered,nb_msgs) if nb > 0]
    date_other_discussions = [str(elt.messages.all()[nb-1].timestamp.day) + ' ' +
                       str(elt.messages.all()[nb-1].timestamp.strftime('%b')) for elt,nb in zip(my_other_discussions_filtered,nb_msgs) if nb >0]

    slugs_other_discussions.reverse()
    lasts_msgs_other_discussions.reverse()
    date_other_discussions.reverse()
    names_other_discussions.reverse()






    context = {'room_slug': mark_safe(json.dumps(disc_slug)),
               'user_slug': mark_safe(json.dumps(request.user.slug)),
               'name_user2_current_discussion': name_user2_current_discussion,
               'current_discussion_last_msg': current_discussion_last_msg,
               'history': history,
               'current_discussion_last_msgS': zip(all_msgs,sent_msgs,date_msgs),
               'date_current_discussion': date_current_discussion,
               'other_discussions': zip(lasts_msgs_other_discussions, names_other_discussions, date_other_discussions,
                                        slugs_other_discussions),
               }
    return render(request, 'messaging/room3.html', context)




    # FOR CHAT HISTORY: Search for other accounts that discussed with active user

    # user_discussions = Discussion.objects.filter(slug__contains=request.user.id)


    # deleting = [elt.delete() for elt in user_discussions if len(elt.messages.all()) == 0]

    # # user_discussions2 to reinitialize user_discussions after deleting
    # user_discussions2 = Discussion.objects.filter(slug__contains=request.user.id)
    # Discussions_without_other_active_user = [elt for elt in user_discussions2 if elt.slug != disc_slug]
    #
    # print('DISCUSSION WITHOUT OTHER ', Discussions_without_other_active_user)
    # user_discussions_slugs = [elt.slug for elt in Discussions_without_other_active_user]
    #
    # other_users_id = [[int(elt) for elt in list(slg)[1:] if int(elt)!=request.user.id][0] for slg in user_discussions_slugs]
    #
    # other_users_account = [Account.objects.get(id=elt) for elt in other_users_id]
    #
    # nb_msg = [len(elt.messages.all()) for elt in Discussions_without_other_active_user]
    #
    # last_msg = [elt.messages.all()[nb-1].content for elt,nb in zip(Discussions_without_other_active_user,nb_msg) if nb > 0]
    #
    # last_msg_dates = [str(elt.messages.all()[nb-1].timestamp.day) + ' ' +
    #                   str(elt.messages.all()[nb-1].timestamp.strftime('%b')) for elt,nb in zip(Discussions_without_other_active_user,nb_msg) if nb >0]
    # last_msg_senders = [elt.first_name + ' '+ elt.last_name for elt in other_users_account]
    #
    #
    # last_msg.reverse()
    # last_msg_senders.reverse()
    # last_msg_dates.reverse()
    # user_discussions_slugs.reverse()
    #
    # return render(request,'messaging/room.html', {
    #     'room_slug': mark_safe(json.dumps(disc_slug)),
    #     'user_slug': mark_safe(json.dumps(request.user.slug)),
    #     'historical_disc_data': zip(last_msg, last_msg_senders, last_msg_dates, user_discussions_slugs),
    #
    #     })


# def room(request, disc_slug='last'):
#     print('--- ROOM FUNCTION - MESSAGING -----')
#
#     # When the message icon is pressed
#     if disc_slug == 'last':
#         discs = Discussion.objects.filter(slug__contains=request.user.id)
#         disc_slug = discs[len(discs) - 1].slug
#
#     # FOR ACTIVE OTHER USER : other active user infos
#
#     this_disc = Discussion.objects.get_or_create(slug=disc_slug)[0]
#     this_disc.save()
#
#     tst = [int(elt) for elt in disc_slug.split('n')[1:] if int(elt) != request.user.id][0]
#     other_user_active = Account.objects.get(id=tst)
#
#     ln_msgs = len(this_disc.messages.all()) - 1
#
#     if ln_msgs > 0:
#         other_active_all_msgs = this_disc.messages.all()
#         other_active_last_msg = other_active_all_msgs[ln_msgs].content
#
#         other_active_msg_date = str(other_active_all_msgs[ln_msgs].timestamp.day) + ' ' + \
#                                 str(other_active_all_msgs[ln_msgs].timestamp.strftime('%b'))
#
#     else:
#         other_active_last_msg = ''
#         time_now = datetime.now()
#         other_active_msg_date = str(time_now.day) + ' ' + str(time_now.strftime('%b'))
#
#     other_active_name = other_user_active.first_name + ' ' + other_user_active.last_name
#
#     # FOR CHAT HISTORY: Search for other accounts that discussed with active user
#     user_discussions = Discussion.objects.filter(slug__contains=request.user.id)
#
#     # deleting = [elt.delete() for elt in user_discussions if len(elt.messages.all()) == 0]
#
#     # user_discussions2 to reinitialize user_discussions after deleting
#     user_discussions2 = Discussion.objects.filter(slug__contains=request.user.id)
#     Discussions_without_other_active_user = [elt for elt in user_discussions2 if elt.slug != disc_slug]
#
#     print('DISCUSSION WITHOUT OTHER ', Discussions_without_other_active_user)
#     user_discussions_slugs = [elt.slug for elt in Discussions_without_other_active_user]
#
#     other_users_id = [[int(elt) for elt in list(slg)[1:] if int(elt) != request.user.id][0] for slg in
#                       user_discussions_slugs]
#
#     other_users_account = [Account.objects.get(id=elt) for elt in other_users_id]
#     print('OTHER USERS ACCOUNT ', other_users_account)
#     nb_msg = [len(elt.messages.all()) for elt in Discussions_without_other_active_user]
#
#     last_msg = [elt.messages.all()[nb - 1].content for elt, nb in zip(Discussions_without_other_active_user, nb_msg) if
#                 nb > 0]
#
#     last_msg_dates = [str(elt.messages.all()[nb - 1].timestamp.day) + ' ' +
#                       str(elt.messages.all()[nb - 1].timestamp.strftime('%b')) for elt, nb in
#                       zip(Discussions_without_other_active_user, nb_msg) if nb > 0]
#     last_msg_senders = [elt.first_name + ' ' + elt.last_name for elt in other_users_account]
#
#     last_msg.reverse()
#     last_msg_senders.reverse()
#     last_msg_dates.reverse()
#     user_discussions_slugs.reverse()
#
#     return render(request, 'messaging/room.html', {
#         'room_slug': mark_safe(json.dumps(disc_slug)),
#         'user_slug': mark_safe(json.dumps(request.user.slug)),
#         'historical_disc_data': zip(last_msg, last_msg_senders, last_msg_dates, user_discussions_slugs),
#         'other_active_name': other_active_name,
#         'other_active_last_msg': other_active_last_msg,
#         'other_active_msg_date': other_active_msg_date,
#     })
