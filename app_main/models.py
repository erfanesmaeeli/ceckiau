from django.db import models
from django.utils.safestring import mark_safe
import os
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from jdatetime import datetime as jd
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
import jdatetime

User = get_user_model()

# validators
english_input = RegexValidator(r'^[A-Za-z0-9.,-]+$', 'تنها استفاده از حروف انگلیسی مجاز می‌باشد.')

ROADMAP_STATES = (
    (1, 'انجام شده'),
    (2, 'در حال انجام'),
    (3, 'در آینده'),
)


BLOG_CATEGORY_TYPE = (
    (1, 'خبری'),
    (2, 'آموزشی'),
    (3, 'دانشجویی'),
    (4, 'انگیزشی'),
    (5, 'متفرقه'),
    (6, 'معرفی'),
    (7, 'علمی')
    )

BLOG_STATUS_TYPE = (
    (1, 'در انتظار تایید'),
    (2, 'تایید شده'),
    (3, 'عدم تایید'),
    (4, 'پیش‌نویس'),
    )


CEC_MEMBER_START_YEAR = (
    (1, '1385'),
    (2, '1386'),
    (3, '1387'),
    (4, '1388'),
    (5, '1389'),
    (6, '1390'),
    (7, '1391'),
    (8, '1392'),
    (9, '1393'),
    (10, '1394'),
    (11, '1395'),
    (12, '1396'),
    (13, '1397'),
    (14, '1398'),
    (15, '1399'),
    (16, '1400'),
    (17, '1401'),
    (18, '1402'),
    (19, '1403'),
    (20, '1404'),
    (21, '1405'),
    (22, '1406'),
    (23, '1407'),
    (24, '1408'),
    (25, '1409'),
    (26, '1410'),
    (27, '1411'),
    (28, '1412'),
    (29, '1413'),
    (30,  '1414')
)

CEC_MEMBER_END_YEAR = (
    (1, '1385'),
    (2, '1386'),
    (3, '1387'),
    (4, '1388'),
    (5, '1389'),
    (6, '1390'),
    (7, '1391'),
    (8, '1392'),
    (9, '1393'),
    (10, '1394'),
    (11, '1395'),
    (12, '1396'),
    (13, '1397'),
    (14, '1398'),
    (15, '1399'),
    (16, '1400'),
    (17, '1401'),
    (18, '1402'),
    (19, '1403'),
    (20, '1404'),
    (21, '1405'),
    (22, '1406'),
    (23, '1407'),
    (24, '1408'),
    (25, '1409'),
    (26, '1410'),
    (27, '1411'),
    (28, '1412'),
    (29, '1413'),
    (30,  '1414')
)

CEC_RANK_TYPES = (
    (1, 'دبیر'),
    (2, 'نایب دبیر'),
    (3, 'مسئول روابط عمومی'),
    (4, 'مسئول امور تبلیغات'),
    (5, 'مسئول مستندات و امور مالی'),
    (6, 'مسئول امور پژوهشی'),
    (7, 'مسئول امور آموزشی'),
    (8, 'عضو کادر فعال')
)


def check_roadmap_states(value):
    if not (1 <= value <= 3):
        raise ValidationError('در انتخاب وضعیت دقت نمائید!')

def check_blog_states(value):
    if not (1 <= value <= 7):
        raise ValidationError('در انتخاب دسته بندی دقت نمائید!')



def image_path(instance, filename):
    return 'slider-image/%s' % (filename)

def team_cover_path(instance, filename):
    return 'team_cover_image/%s' % (filename)

def team_avatar_path(instance, filename):
    return 'team_avatar_image/%s' % (filename)

def blog_image_path(instance, filename):
    return 'blog-main-image/%s' % (filename)

def cec_members_avatar_path(instance, filename):
    return 'cec_members_avatar_image/%s' % (filename)
    
def attachment_files_path(instance, filename):
    return 'blog_attachment_files/%s' % (filename)


class Slider(models.Model):
    class Meta:
        verbose_name = "اسلاید"
        verbose_name_plural = "اسلایدر"
    publish = models.BooleanField('نمایش در سایت',default=True)
    name = models.CharField('نام اسلایدر' , max_length=128 , null=True , blank=True)
    image = models.ImageField('عکس' , upload_to=image_path, null=True, blank=True)


    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" width="372" height="90"/>'.format("/media/"+str(self.image)) )


class RoadMap(models.Model):
    DateCreate = jmodels.jDateField(verbose_name='در تاریخ', auto_now_add=False , null=True , blank=True)
    state = models.PositiveSmallIntegerField(verbose_name='وضعیت' , choices=ROADMAP_STATES , null=True , validators=[check_roadmap_states])
    text = models.TextField(verbose_name='توضیحات ویژگی' ,null=True)
    link = models.CharField('لینک صفحه' ,max_length=120 , null=True, blank=True)


    class Meta:
        verbose_name = 'ویژگی های نقشه راه آینده'
        verbose_name_plural = 'نقشه راه آینده'


    def __str__(self):
        return '%s - %s' %(self.text,self.DateCreate)

class Team(models.Model):
    name = models.CharField(verbose_name="نام نام خانوادگی" , max_length=50, null=True)
    description = models.TextField(verbose_name="توضیحات" , null=True)
    cover = models.ImageField(verbose_name="عکس پس زمینه", upload_to=team_cover_path, default='team_cover_path/default_cover.jpg')
    avatar = models.ImageField(verbose_name="عکس پروفایل", upload_to=team_avatar_path, default='team_avatar_path/default_avatar.jpg')
    website = models.CharField(verbose_name="وب سایت" , null=True, blank=True, max_length=128)
    telegram = models.CharField(verbose_name="تلگرام" , null=True, blank=True, max_length=128)
    instagram = models.CharField(verbose_name="اینستاگرام" , null=True, blank=True, max_length=128)
    twitter = models.CharField(verbose_name="توئیتر" , null=True, blank=True, max_length=128)
    linkedin = models.CharField(verbose_name="لینکدین" , null=True, blank=True, max_length=128)
    github = models.CharField(verbose_name="گیتهاب" , null=True, blank=True, max_length=128)
    dribbble = models.CharField(verbose_name="دریبل" , null=True, blank=True, max_length=128)

    class Meta:
        verbose_name = 'عضو تیم فنی'
        verbose_name_plural = 'تیم فنی'

    def __str__(self):
        return self.name

    def avatar_tag(self):
        return mark_safe('<img src="{}" height="90"/>'.format("/media/"+str(self.avatar)) )


class Blog(models.Model):
    slug = models.SlugField(null=True, allow_unicode=True, blank=False, validators=[english_input])
    publish = models.BooleanField('نمایش در سایت',default=True)
    show_author = models.BooleanField('نمایش نام نویسنده',default=True)
    status = models.PositiveSmallIntegerField(verbose_name='وضعیت تایید پست', choices=BLOG_STATUS_TYPE , null=True, default=1)
    category = models.PositiveSmallIntegerField(verbose_name='دسته بندی', choices=BLOG_CATEGORY_TYPE , null=True ,validators=[check_blog_states])
    title = models.CharField(verbose_name='عنوان' , max_length=128, null=True)
    DateCreate = jmodels.jDateField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    LastEdit = jmodels.jDateTimeField(verbose_name="تاریخ آخرین ادیت",auto_now_add=True)
    TimeCreate = models.TimeField(verbose_name="ساعت ایجاد", default=timezone.now, editable=False, null=True)
    _DateCreate = models.DateTimeField( auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده", null=True, related_name="author")
    text = RichTextUploadingField(verbose_name='متن' , null=True)
    image = models.ImageField(verbose_name='تصویر پست' , upload_to=blog_image_path)
    meta_description = models.TextField(verbose_name='محتوای متا‌تگ' , null=True, blank=False , max_length=160)

    def author_name(self):
        return self.author.first_name + " " + self.author.last_name

    def get_absolute_url(self):
        params = {'slug': self.slug}
        return reverse('app-main:blog-post', kwargs=params)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)

        super().save(*args, **kwargs)


    @property
    def get_category(self):
        return dict(BLOG_CATEGORY_TYPE)[self.category]

    @get_category.setter
    def get_category(self, category_type):
        reversed_types = {v: k for k, v in dict(BLOG_CATEGORY_TYPE).items()}
        self.category = reversed_types.get(category_type)


    @property
    def get_status(self):
        return dict(BLOG_STATUS_TYPE)[self.status]

    @get_status.setter
    def get_status(self, status_type):
        reversed_types = {v: k for k, v in dict(BLOG_STATUS_TYPE).items()}
        self.status = reversed_types.get(status_type)


    def image_tag(self):
        return mark_safe('<img src="{}" width="200" height="200"/>'.format("/media/"+str(self.image)) )

    class Meta:
        ordering = ('_DateCreate', )
        verbose_name = "پست"
        verbose_name_plural = "پست های بلاگ"

    def __str__(self):
        return self.title

class AttachmentFiles(models.Model):
    blog = models.ForeignKey(Blog, verbose_name="پست", on_delete=models.CASCADE, null=True, related_name="files")
    name = models.CharField(verbose_name="نام فایل", max_length=120, null=True, blank=True)
    file = models.FileField(verbose_name="فایل", null=True, upload_to=attachment_files_path)

    def filename(self):
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.basename(self.file.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "فایل"
        verbose_name_plural = "فایل های ضمیمه شده در بلاگ"

    def __str__(self):
        return '%s - %s - %s' %(self.blog.category, self.blog.title, self.name)

class years_list(models.Model):
    start_year = models.SmallIntegerField('از سال', choices=CEC_MEMBER_START_YEAR, null=True, default=1)
    end_year = models.SmallIntegerField('تا سال', choices=CEC_MEMBER_END_YEAR, null=True, default=1)

    @property
    def get_start_year(self):
        return dict(CEC_MEMBER_START_YEAR)[self.start_year]

    @get_start_year.setter
    def get_start_year(self, cec_member_start_year):
        reversed_types = {v: k for k, v in dict(CEC_MEMBER_START_YEAR).items()}
        self.start_year = reversed_types.get(cec_member_start_year)

    @property
    def get_end_year(self):
        return dict(CEC_MEMBER_END_YEAR)[self.end_year]

    @get_end_year.setter
    def get_end_year(self, cec_member_end_year):
        reversed_types = {v: k for k, v in dict(CEC_MEMBER_END_YEAR).items()}
        self.end_year = reversed_types.get(cec_member_end_year)

    @property
    def get_year(self):
        return '%s - %s' %(self.get_end_year, self.get_start_year)

    def __str__(self):
        return ' سال تحصیلی %s - %s' %(self.get_end_year, self.get_start_year)

    class Meta:
        verbose_name = "سال"
        verbose_name_plural = "سال های تحصیلی"

class rank_list(models.Model):
    year = models.ForeignKey(years_list, on_delete=models.CASCADE, verbose_name="سال تحصیلی", null=True)
    rank_type = models.CharField(verbose_name="دسته بندی" ,max_length=50, null=True, help_text="بعنوان مثال: اعضای هیئت رئیسه")
    rank_type_order = models.PositiveSmallIntegerField(verbose_name="اولویت دسته بندی" , null=True, help_text="بعنوان مثال عدد 1 بالاترین درجه است")
    name = models.CharField(verbose_name="نام سمت" ,max_length=50, null=True)
    order = models.PositiveSmallIntegerField(verbose_name="اولویت سمت" , null=True, help_text="بعنوان مثال عدد 1 بالاترین درجه است")
    info = models.TextField(verbose_name="توضیحات (اختیاری)", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "درجه"
        verbose_name_plural = "درجه های اعضای انجمن"

class CecMembers(models.Model):
    name = models.CharField(verbose_name="نام نام خانوادگی" , max_length=100, null=True)
    year = models.ForeignKey(years_list, on_delete=models.CASCADE, verbose_name="سال تحصیلی", null=True)
    rank = models.ForeignKey(rank_list, on_delete=models.CASCADE, verbose_name="سمت", null=True)
    avatar = models.ImageField(verbose_name="عکس پروفایل", upload_to=cec_members_avatar_path)

    class Meta:
        verbose_name = "عضو"
        verbose_name_plural = "اعضای هیئت رئیسه و کادر"

    def __str__(self):
        return self.name

    def profile_pic(self):
        return mark_safe('<img src="{}" height="90"/>'.format("/media/"+str(self.avatar)) )


#** delete files for slider
@receiver(models.signals.post_delete, sender=Slider)
def auto_delete_file_on_delete_1(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Slider)
def auto_delete_file_on_change_1(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Slider.objects.get(pk=instance.pk).image
    except Slider.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


#** delete files for team (cover image)
@receiver(models.signals.post_delete, sender=Team)
def auto_delete_file_on_delete_2(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)

@receiver(models.signals.pre_save, sender=Team)
def auto_delete_file_on_change_2(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Team.objects.get(pk=instance.pk).cover
    except Team.DoesNotExist:
        return False

    new_file = instance.cover
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


#** delete files for team (avatar image)
@receiver(models.signals.post_delete, sender=Team)
def auto_delete_file_on_delete_3(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.cover:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

@receiver(models.signals.pre_save, sender=Team)
def auto_delete_file_on_change_3(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Team.objects.get(pk=instance.pk).avatar
    except Team.DoesNotExist:
        return False

    new_file = instance.avatar
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)



#** delete image for blog post main image
@receiver(models.signals.post_delete, sender=Blog)
def auto_delete_file_on_delete_4(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Blog)
def auto_delete_file_on_change_4(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Blog.objects.get(pk=instance.pk).image
    except Blog.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


#** auto delete files for cec member (avatar image)
@receiver(models.signals.post_delete, sender=CecMembers)
def auto_delete_file_on_delete_5(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

@receiver(models.signals.pre_save, sender=CecMembers)
def auto_delete_file_on_change_5(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = CecMembers.objects.get(pk=instance.pk).avatar
    except CecMembers.DoesNotExist:
        return False

    new_file = instance.avatar
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
