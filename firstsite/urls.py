from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from app_main import views
from django.conf.urls import handler404

admin.site.site_header = 'مدیریت انجمن علمی مهندسی کامپیوتر'                    # default: "Django Administration"
admin.site.index_title = 'صفحه اصلی'                 # default: "Site administration"
admin.site.site_title = 'پنل مدیریت انجمن علمی مهندسی کامپیوتر' # default: "Django site admin"



urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('boldozer/', admin.site.urls),
    # path('social/' , views.social),
    path('' ,include(('app_main.urls' , 'app_main') , namespace='app-main')) , 
    path('user/' , include(('app_account.urls', 'app_account'), namespace='app-account')) ,
    path('courses/' , include(('app_course.urls', 'app_course'), namespace='app-course')) ,
    # path('', views.coming_soon),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler404 = myapp.views.handler404
#handler500 = myapp.views.handler500
