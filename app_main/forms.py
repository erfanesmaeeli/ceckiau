from app_main.models import Blog
from ckeditor.widgets import CKEditorWidget
from django import forms
from tinymce.widgets import TinyMCE



class Post_Form(forms.ModelForm):
    disabled_fields = ('author',)
    
    text = forms.CharField(widget=TinyMCE(attrs={"id":"editor"}), label="<span class='mdi mdi-border-color icon-sm'></span> محتوای پست")
    class Meta:
        model = Blog
        fields = ['publish','show_author','slug', 'title', 'text', 'meta_description', 'category', 'author', 'image']
        labels = {
        'publish' : '',
        'slug': '<span class="mdi mdi-link-variant icon-sm"></span> پیوند یکتا',
        'title': '<span class="mdi mdi-code-tags icon-sm"></span> عنوان',
        'meta_description': '<span class="mdi mdi-comment-check-outline icon-sm"></span> محتوای متاتگ (SEO)',
        'category': '<span class="mdi mdi-folder-multiple-outline icon-sm"></span> دسته بندی',
        'author': '<span class="mdi mdi-account-outline icon-sm"></span> نویسنده',
    }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Post_Form, self).__init__(*args, **kwargs)
        self.fields['meta_description'].help_text = '<small class="form-text text-muted text-left pl-1 text-small">حداکثر 160 کاراکتر</small>'
        self.fields['slug'].widget.attrs['placeholder'] = 'به زبان انگلیسی و بدون استفاده از فاصله وارد کنید'
        self.fields['meta_description'].widget.attrs['placeholder'] = 'یک توضیح کوتاه جهت معرفی پست خود بنویسید ...'
        self.fields['image'].widget.attrs={
        'id':'chooseFile',
        'accept': '.png, .jpg, .jpeg'
        }
        
        if not self.request.user.is_superuser:
            self.fields['author'].widget = forms.HiddenInput()
                
            self.fields['author'].help_text = '<span class="text-muted text-small">نام نویسنده غیرقابل تغییر است!</span>'

    
