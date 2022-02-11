from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ValidationError
from datetime import datetime
from jdatetime import datetime as jd
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django_jalali.db import models as jmodels


User = get_user_model()


EDUCATION_TYPES = (
    (1, 'دانش‌آموزش'),
    (2, 'دیپلم'),
    (3, 'دانشجو'),
    (4, 'کاردانی'),
    (5, 'کارشناسی'),
    (6, 'کارشناسی ارشد'),
    (7, 'دکتری'),
)

UNIVERSITY_TYPES = (
    (1, 'دانشگاه آزاد کرج'),
    (2, 'سایر دانشگاه ها'),
    (3, 'دانشجو نیستم'),
)

RANK_TYPES = (
    (1, 'کاربر عادی'),
    (2, 'نویسنده'),
    (3, 'کادر انجمن'),
    (4, 'هیئت رئیسه انجمن'),
    (5, 'معاون ارشد'),
    (6, 'مدیرکل')
)

SEX_TYPES = (
    (1, 'آقا'),
    (2, 'خانم')
)

LIVE_TYPES = (
    (1, 'کرج'),
    (2, 'تهران'),
    (3, 'سایر')
)

STAFF_STATE = (
    (1, 'ارسال درخواست'),
    (2, 'مصاحبه'),
    (3, 'در صف بررسی'),
    (4, 'تایید نهایی'),
    (5, 'عدم تایید')
)

def check_education(value):
    if not (1 <= value <= 7):
        raise ValidationError('در انتخاب سطح تحصیلات دقت نمائید!')

def check_university(value):
    if not (1 <= value <= 3):
        raise ValidationError('در انتخاب سطح دانشگاه دقت نمائید!')

def check_rank(value):
    if not (1 <= value <= 6 ):
        raise ValidationError('در انتخاب سطح سمت ناحیه کاربری دقت نمائید!')

def check_sex(value):
    if not (1 <= value <= 2 ):
        raise ValidationError('در انتخاب سطح جنسیت دقت نمائید!')

def check_live(value):
    if not (1 <= value <= 3 ):
        raise ValidationError('در انتخاب سطح محل زندگی دقت نمائید!')

def check_staff(value):
    if not (1 <= value <= 5 ):
        raise ValidationError('در انتخاب وضعیت عضو کادر دقت نمائید!')

def avatar_path(instance, filename):
    return 'profile-avatar/%s' % (filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='profile')
    fname = models.CharField('نام', max_length=30, null=True, blank=True)
    lname = models.CharField('نام خانوادگی', max_length=50, null=True, blank=True)
    university= models.PositiveSmallIntegerField('دانشگاه', choices=UNIVERSITY_TYPES, default=1, validators=[check_university])
    email = models.EmailField('پست الکترونیک', max_length=70,blank=True , null = True)
    education = models.PositiveSmallIntegerField('تحصیلات', choices=EDUCATION_TYPES, default= 5, validators=[check_education])
    join_uni= models.PositiveSmallIntegerField('سال ورودی', default=0)
    phone = models.CharField('شماره همراه', max_length=15, null=True, blank=True)
    rank = models.PositiveSmallIntegerField('ناحیه کاربری' , choices=RANK_TYPES , default=1)
    show_profile = models.BooleanField('نمایش پروفایل' ,default=False)
    DateCreate = models.DateTimeField( auto_now_add=True)
    telegram = models.CharField('آیدی تلگرام', max_length=50, null=True , blank=True)
    avatar = models.ImageField('عکس پروفایل' , upload_to=avatar_path, default='profile-avatar/default.jpg')
    birthday = models.CharField('تاریخ تولد', max_length=15, null=True, blank=True)
    sex = models.PositiveSmallIntegerField('جنسیت', choices=SEX_TYPES , null=True, blank=True , validators=[check_sex])
    live = models.PositiveSmallIntegerField('محل زندگی', choices=LIVE_TYPES , null=True, blank=True , validators=[check_live])

    code = models.IntegerField('کد امنیتی' , default = 0 , editable=False)

    is_author = models.BooleanField('نویسنده است', default=False)
    is_teacher = models.BooleanField('مدرس است', default=False)

    bio = models.TextField("درباره من", null=True, blank=True, max_length=300)

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل ها"


    def get_full_name(self):
        return self.fname + " " + self.lname

    def __str__(self):
        return self.user.username
    def image_tag(self):
        return mark_safe('<img src="{}" width="372" height="90"/>'.format("/media/profile-avatar/"+str(self.avatar)) )


class Staff(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE , related_name='staff' , verbose_name="کاربر")
    want = models.TextField(verbose_name="توقع از انجمن" , null=True)
    purpose = models.TextField(verbose_name="هدف از عضویت در کادر" , null=True)
    skills = models.TextField(verbose_name="مهارت ها" , null=True)
    phone = models.CharField('تلفن همراه', max_length=15, null=True)
    telegram = models.CharField('آیدی تلگرام', max_length=50, null=True , blank=True)
    date = jmodels.jDateField(verbose_name='تاریخ ملاقات', auto_now_add=False , null=True , blank=True)
    time = models.TimeField(verbose_name="ساعت ملاقات" ,  null=True , blank=True)
    DateCreate = jmodels.jDateField(verbose_name="تاریخ درخواست", auto_now_add=True)
    state = models.SmallIntegerField(verbose_name="وضعیت" , choices=STAFF_STATE, null=True, blank=True , validators=[check_staff] , default=1 )

    class Meta:
        verbose_name = "عضو کادر"
        verbose_name_plural = "اعضای کادر"

    def __str__(self):
        return "%s - %s" %(self.user.fname,self.user.lname)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        if instance.profile is not None :
            instance.profile.save()

@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()


# delete file
# @receiver(models.signals.post_delete, sender=Profile)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.avatar:
#         if os.path.isfile(instance.avatar.path):
#             os.remove(instance.avatar.path)

# @receiver(models.signals.pre_save, sender=Profile)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False

#     try:
#         old_file = sender.objects.get(pk=instance.pk).avatar
#     except sender.DoesNotExist:
#         return False

#     new_file = instance.avatar
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
