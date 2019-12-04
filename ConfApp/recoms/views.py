from django.shortcuts import render
from .models import Session
from Account.models import Account
from django.views.generic import ListView
from tagging.models import Tag

import pandas as pd
from .functions import *




# def recoms(request):
#     sessions = Session.objects.all()[:5]
#     context = {'sessions': sessions}
#     return render(request,'recoms/Recom_page.html', context)



class RecomSessListView(ListView):
    model = Session
    template_name='recoms/RecomSess_page.html'
    context_object_name='sessions'
    paginate_by = 5

    def get_queryset(self):
        tags = self.request.user.key_words
        keywords= tags.split(',')
        keywords_treated = vocab2(keywords)
        recommended_sessions = instance_sessions[keywords_treated]
        indexs = [elt[0]+1 for elt in recommended_sessions]
        return Session.objects.filter(id__in=indexs)


def RecomAtnListView(request):

    # Recommendation part
    user_kwords = request.user.key_words.split(',')
    key_words_treated = vocab2(user_kwords)
    recommended_users_indexs= instance_users[key_words_treated]
    indexs = [elt[0] for elt in recommended_users_indexs]
    recommended_users_mails = list(corpus_users_dict.iloc[indexs,0])
    users = [Account.objects.get(email=mail) for mail in recommended_users_mails if Account.objects.get(email=mail) != request.user]

    # Messaging import
    my_account_id = request.user.id
    discussion_slug1 = [sorted([my_account_id,elt.id]) for elt in users]
    discussion_slug2 = ['n'+str(elt[0])+'n'+ str(elt[1]) for elt in discussion_slug1]

    template = 'recoms/RecomAtn_page.html'
    tags_list = [Tag.objects.get_for_object(acnt) for acnt in users]
    context = {'data': zip(users,tags_list,discussion_slug2),
               }

    return render(request,template,context)

# class RecomAtnListView(TaggedObjectList):
#     model = Account
#     template_name='recoms/RecomAtn_page.html'
#     context_object_name='users'
#     paginate_by = 5
#
#     def get_queryset(self):
#         # AFTER: do this only for recommended USERS
#
#         # turn kwords into lists
#
#         # treat lists using vocab2
#
#         # add tags
#
#         # turning kwords into lists
#         # for user in Account.objects.all():
#             # kwords_tolist = user.key_words.split(',')
#             # kwords_tolist = ','.join()
#             # user.key_words = kwords_tolist
#             # user.save()
#         return Account.objects.exclude(id=24)




# -------------------------------- Get corpus  of RF2018 titles -------------------------------
path_corpus=r'C:\\Users\\Cyala\\PycharmProjects\\ConfApp4\\Recommendation_branch\\Salons\\ConfApp\\recoms\\corpus.csv'
corpus3 = pd.read_csv(path_corpus)

range_columns = range(len(corpus3.columns))
corpus2= [list(corpus3.iloc[:,col]) for col in range_columns]
corpus_sessions = [remove9(elt) for elt in corpus2]


instance_sessions = WmdSimilarity(corpus_sessions,model,num_best=30)


# -------------------------------- Creating users corpus -------------------------------

corpus_users = [elt.key_words.split(',') for elt in Account.objects.exclude(email='admin@gmail.com')]
mails = [elt.email for elt in Account.objects.exclude(email='admin@mail.com')]
keywords = [elt.key_words for elt in Account.objects.exclude(email='admin@mail.com')]
corpus_users_dict = pd.DataFrame({'email': mails, 'kwords': keywords})

instance_users = WmdSimilarity(corpus_users,model,num_best=30)
