from django.shortcuts import render
from django.http import HttpResponse
from Account.models import Account
from .utils import send_msg_notif, which_status_user, which_status, change_status_user
from django.db.models import Q
from tagging.models import Tag

# def alarm(req):
#     layer = get_channel_layer()
#     async_to_sync(layer.group_send)('events', {'type': 'test'})
#     return HttpResponse('<p>Done</p>')



def ProfilePage(request):
        user = request.user
        context={'profile_page': user}
        return render(request,'Attendees/profile_page.html', context)


def searchpage(request):

    my_account_id = request.user.id
    if request.method=='POST':

        try:

            if request.POST['q']:
                query = request.POST['q']
                users = Account.objects.filter(Q(last_name__icontains=query) | Q(first_name__icontains=query))

                # discussion slug creation
                discussion_slug1 = [sorted([my_account_id,elt.id]) for elt in users]
                discussion_slug2 = ['n'+str(elt[0])+'n'+ str(elt[1]) for elt in discussion_slug1]

                tags_list = [Tag.objects.get_for_object(acnt) for acnt in users]
                if len(users)>0:

                    context = {'users': zip(users,discussion_slug2,tags_list)
                              }


                    return render(request,'Attendees/Ids.html', context)
                else:
                    return render(request, 'Attendees/Ids2.html')
        except:
            labels = ['is_staff', 'is_organizer', 'is_chair', 'is_speaker']
            status = ['STAFF', 'ORGANIZER', 'CHAIR', 'SPEAKER']

            in_request = {elt: elt in request.POST for elt in labels}

            for elt in request.POST.keys():
                try:
                    updated_user = Account.objects.get(slug=elt)
                except:
                    pass


            all_confs = len(request.user.conferences.all()) - 1
            this_conf = request.user.conferences.all()[all_confs]

            for (ind,lab),st in zip(enumerate(labels),status):
                modified = not in_request[lab] == which_status_user(updated_user,ind)

                if modified:
                    is_status = request.POST.get(lab)
                    change_status_user(updated_user,ind)

                    #detect if status is added or removed:
                    if is_status=='no':
                        which_status(this_conf, ind).add(updated_user)

                        group_name = 'notif_status'
                        content = 'New status: ' + st
                        notif = {'user': str(updated_user.id),
                                 'content': content,
                                 'title': 'STATUS UPDATE',
                                 'sender': 'from STAFFS'}

                        send_msg_notif(group_name, notif)

                    else:
                        which_status(this_conf, ind).remove(updated_user)

                        group_name = 'notif_status'
                        content = 'Status Removed: ' + st
                        notif = {'user': str(updated_user.id),
                                 'content': content,
                                 'title': 'STATUS UPDATE',
                                 'sender': 'from STAFFS'}

                        send_msg_notif(group_name, notif)

    return render(request,'Attendees/Ids.html')


