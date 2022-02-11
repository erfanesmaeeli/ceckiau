from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from django_jalali.db import models as jmodels
from django.utils.text import slugify
from django.urls import reverse
import os


def course_image_path(instance, filename):
    return 'Course-images/%s' % (filename)

COURSE_CATEGORY_TYPE = (
    (1, 'برنامه نویسی'),
    (2, 'فتوشاپ'),
    (3, 'بازی سازی'),
    (4, 'معرفی'),
    (5, 'طراحی وب'),
    (6, 'شبکه'),
    (7, 'کاربردی'),
    )

COURSE_STATE_TYPE = (
    (1, 'درحال برگزاری'),
    (2, 'تکمیل شده'),
    (3, 'به زودی'),
    )

def check_course_states(value):
    if not (1 <= value <= 7):
        raise ValidationError('در انتخاب دسته بندی دقت نمائید!')

def check_course_states1(value):
    if not (1 <= value <= 3):
        raise ValidationError('در انتخاب وضعیت دوره دقت نمائید!')

class Course(models.Model):
    slug = models.SlugField(null=True, allow_unicode=True, blank=True)
    _course_state = models.PositiveSmallIntegerField(verbose_name='وضعیت دوره', choices=COURSE_STATE_TYPE , null=True ,validators=[check_course_states1])
    _category = models.PositiveSmallIntegerField(verbose_name='دسته بندی', choices=COURSE_CATEGORY_TYPE , null=True ,validators=[check_course_states])
    title = models.TextField(verbose_name='عنوان دوره', null=True)
    teacher = models.CharField(verbose_name='مدرس دوره' ,max_length=128, null=True)
    info = models.TextField(verbose_name='معرفی کوتاه', null=True)
    description = RichTextUploadingField(verbose_name='توضیحات دوره', null=True)
    image = models.ImageField(verbose_name='عکس دوره',upload_to=course_image_path, null=True)
    DateCreate = jmodels.jDateField(verbose_name="تاریخ ایجاد دوره", auto_now_add=True)
    meta_description = models.TextField(verbose_name='محتوای متا‌تگ' , null=True, blank=True , max_length=160)



    def get_absolute_url(self):
        params = {'slug': self.slug}
        return reverse('app-course:course-detail', kwargs=params)

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug :
                self.slug = self.title.replace(' ', '-')
            
            else:
                self.slug = slugify(self.slug)
        else:
            self.slug = slugify(self.slug)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def category(self):
        return dict(COURSE_CATEGORY_TYPE)[self._category]

    @category.setter
    def category(self, category_type):
        reversed_types = {v: k for k, v in dict(COURSE_CATEGORY_TYPE).items()}
        self._category = reversed_types.get(category_type)

    # ----
    @property
    def state(self):
        return dict(COURSE_STATE_TYPE)[self._course_state]

    @state.setter
    def state(self, state_type):
        reversed_types = {v: k for k, v in dict(COURSE_STATE_TYPE).items()}
        self._course_state = reversed_types.get(state_type)


    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150"/>'.format("/media/"+str(self.image)) )    

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural =  'دوراه ها'


class CourseSession(models.Model):
    slug = models.SlugField(null=True, allow_unicode=True, blank=True)
    course = models.ForeignKey(Course,verbose_name='انتخاب دوره' , on_delete=models.CASCADE, null=True)
    title = models.TextField(verbose_name='عنوان قسمت',null=True)
    length = models.CharField(verbose_name='مدت زمان',max_length=10, null=True)
    description = RichTextUploadingField(verbose_name='توضیحات', null=True)
    video_aparat = models.TextField(verbose_name='لینک آپارات',null=True)
    # attachment_files = GenericRelation('AttachmentFiles')
    DateCreate = jmodels.jDateField(verbose_name="تاریخ ایجاد قسمت", auto_now_add=True)
    meta_description = models.TextField(verbose_name='محتوای متا‌تگ' , null=True, blank=True , max_length=160)


    def Course_Name(self):
        return self.course.title

    def get_absolute_url(self):
        params = {'course_slug': self.course.slug, 'course_session_slug': self.slug }
        return reverse('app-course:course-session-detail', kwargs=params)

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug :
                self.slug = self.title.replace(' ', '-')
            
            else:
                self.slug = slugify(self.slug)
        else:
            self.slug = slugify(self.slug)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'جلسات دوره'
        verbose_name_plural =  'جلسات دوره ها'

# class AttachmentFiles(models.Model):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey()
#     file = models.FileField(upload_to = 'attach-files') 


#     def __str__(self):
#         text = f" - {self.content_object.title}"
#         return text  

#     class Meta:
#         verbose_name = 'فایل ضمیمه شده'
#         verbose_name_plural =  'فایل های ضمیمه شده'



# dynamic add and remove course image 
# 
@receiver(models.signals.post_delete, sender=Course)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Course)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Course.objects.get(pk=instance.pk).image
    except Course.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
