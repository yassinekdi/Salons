from django.db import models
from ConfApp.utils import unique_slug_generator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from recoms.functions import *
from tagging.models import Tag

class MyAccountManager(BaseUserManager):

    def create_user(self,email,password=None):
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email=self.normalize_email(email), password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class Account(AbstractUser):

    Status_choice = (('Student', 'Student'), ('Researcher', 'Researcher'), ('Engineer', 'Engineer'),
                                          ('Commercial', 'Commercial'), ('Other', 'Other'))
    Sex_choice = (('Male', 'Male'),('Female','Female'))
    email = models.EmailField(verbose_name="email", max_length=60,unique="True")
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add="True")
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, null=True,blank=True)
    is_superuser = models.BooleanField(default=False)
    status = models.CharField(verbose_name="Status", max_length=20, choices=Status_choice)
    webpage = models.CharField(verbose_name="Webpage", max_length=50, default="LinkedIn, Researchgate, blog..")
    organism = models.CharField(verbose_name="Organism", max_length=50, default="University/Institute/Company..")
    key_words = models.CharField(verbose_name="Key words", max_length=250, default="Keywords")
    first_name = models.CharField(verbose_name="First name", max_length=20, default="")
    last_name = models.CharField(verbose_name="Last name", max_length=20, default="")
    is_chair = models.BooleanField(verbose_name='Chair',default=False)
    is_organizer = models.BooleanField(verbose_name='Organizer',default=False)
    is_presenting = models.BooleanField(verbose_name='Presenting',default=False)
    sex = models.CharField(verbose_name="Sex", choices=Sex_choice, max_length=6)
    country = models.CharField(verbose_name="Country", max_length=20, default="Country")
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyAccountManager()



    def __str__(self):
        return self.slug


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = slugify(instance)
        instance.slug = unique_slug_generator(instance)
#
#
pre_save.connect(slug_generator,sender=Account)



def add_tag(sender,instance,**kwargs):

    # transforming + cleaning keywords + adding tags
    sender_k = instance.key_words

    if len(sender_k)>0:

        Tag.objects.update_tags(instance, None)
        sender_k2 = sender_k.split(',')
        sender_k3 = []
        for elt in sender_k2:
            if len(elt.split(' '))>1:
                elt2 = elt.split(' ')
                sender_k3.append('-'.join(elt2))
            else:
                sender_k3.append(elt)

        add_tags = [Tag.objects.add_tag(instance, word) for word in sender_k3]


post_save.connect(add_tag,sender=Account)