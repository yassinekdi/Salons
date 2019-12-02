from django.shortcuts import render
from .models import Session
from Account.models import Account
from django.views.generic import ListView
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
        sim = instance[keywords_treated]
        indexs = [elt[0]+1 for elt in sim]
        return Session.objects.filter(id__in=indexs)


class RecomAtnListView(ListView):
    model = Account
    template_name='recoms/RecomAtn_page.html'
    context_object_name='users'
    paginate_by = 5


# -------------------------------- Get corpus  of RF2018 titles -------------------------------
path_corpus=r'C:\\Users\\Cyala\\PycharmProjects\\ConfApp4\\Recommendation_branch\\Salons\\ConfApp\\recoms\\corpus.csv'
corpus3 = pd.read_csv(path_corpus)

range_columns = range(len(corpus3.columns))
corpus2= [list(corpus3.iloc[:,col]) for col in range_columns]
corpus = [remove9(elt) for elt in corpus2]

# Lecoz = ['measurement', 'sediment', 'hydrometry', 'hydro-acoustic', 'modeling', 'restoration', 'uncertainty',
#  'morphidynamics',  'LSPIV',  'rating curves', 'bayesian']
#
instance = WmdSimilarity(corpus,model,num_best=30)
# sim=instance[Lecoz]
# indexs = [elt[0] for elt in sim]
# for elt in indexs:
#     print('SESSION RECOMMENDED: ', Session.objects.get(id=elt+1))