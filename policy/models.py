from django.db import models
import cloudinary
# from django.contrib import admin
from cloudinary.models import CloudinaryField
import datetime as dt
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, UserManager
)
from django.db.models.signals import post_save
from django.utils.translation import gettext as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# from rest_framework.authtoken.models import Token
# from rest_framework.authtokenknox.models import Token
# Create your models here.




class User(AbstractBaseUser):

    
    first_name = models.CharField(max_length=50, blank=True, unique=True)
    username = models.CharField(max_length=50, blank=True, unique=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    id_no = models.IntegerField(null=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, default='')
    bio = models.TextField(max_length=500, blank=True, null=True)
    is_admin = models.BooleanField(default=True,null=True)
    is_agent = models.BooleanField(default=False,null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_no = models.CharField(max_length=20, default='', null=True)
    address = models.CharField(max_length=100, default='',null=True)

    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    #  USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['']
    # EMAIL_FIELD='email'

    
    objects = UserManager()
    
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.email

    def has_perm(self, app_label):
        "Does the user have permission to view the app 'app_label'?"
        return True

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_agent(self):
        "Is the user active?"
        return self.agent




    def __str__(self):
        return self.email

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            import pdb; pdb.set_trace()
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.Userprofile.save()

# accounts.models.py

class UserManager(BaseUserManager):

    def create_user(self, email=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        # user = self.model(
        #     email=self.normalize_email(email),
        # )

        # email = self.normalize_email(email)
        user = self.model()

        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.agent = True
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username = first_name,
            email = email,
            password = password,
        )
        user.agent = True
        user.admin = True
        user.save(using=self._db)
        return user

        




# class User(AbstractBaseUser): 
#     ...
#     objects = UserManager() 


class Policy(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    category = models.ForeignKey("Category", related_name='policy',on_delete=models.CASCADE, null = True)
    policy_number = models.CharField(max_length=20, null = True)
    policy_contact = models.CharField(max_length=30, null = True)
    category  = models.CharField(max_length=30,null = True)
    form = models.TextField(max_length=300,null = True)
    slug = models.SlugField(max_length=200,null = True, db_index=True)
    signed = models.DateTimeField(auto_now_add=True,null = True)
    updated = models.DateTimeField(auto_now=True,null = True)

    def __str__(self):
        return self.policy_number

    def post_product(self):
        self.save()

    def delete_product(self):
        self.delete()
    class Meta:
        ordering = ('-signed',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.policy_number

    def get_absolute_url(self):
        return reverse("policy", kwargs={
            "pk" : self.pk

        })

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null = True)
    cv = CloudinaryField('image' ,null = True)
    profile_picture = CloudinaryField('image' ,null = True)
    remarks = models.TextField(null = True)


    def __str__(self):
        return self.remarks

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,null = True)
    cv = CloudinaryField('image',null = True)
    profile_picture = CloudinaryField('image')
    date_joined = models.DateTimeField( default=timezone.now, null = True) 
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('U', 'Unisex/Parody'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    EMPLOYMENT_CHOICES = (('E', 'Employed'), ('U', 'Unemployed'), ('S', 'Self-employed'))
    employment_status =models.CharField(max_length=1 ,choices=EMPLOYMENT_CHOICES, null = True)
    policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, related_name='userprofile', blank=True)
    bank_accountno = models.IntegerField( null = True)

    
    objects = UserManager()

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):

    #     if created:
    #         UserProfile.objects.create(user=instance)





class AgentProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    cv = CloudinaryField('image',null = True)
    profile_picture = CloudinaryField('image',null = True)
    job_number = models.CharField(max_length=20, blank=True,null = True)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('U', 'Unisex/Parody'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null = True)

    def __str__(self):
        return self.job_number

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            AgentProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
            instance.agentprofile.save()


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, null = True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True,null = True)

    class Meta:
    
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('policy_list_by_category', args=[self.slug])


# @receiver(post_save,sender = settings.AUTH_USER_MODEL)
# def create_auth_token(sender , instance = None, created = False, **kwargs):
#     if created:
#         Token.objects.created(user = instance)
