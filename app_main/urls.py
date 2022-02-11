from django.urls import path
from app_main import views

urlpatterns = [
    path('', views.home , name = "home"),
    path('login/' , views.login_ , name = "login") ,
    path('logout/' , views.logout_ , name = "logout") ,
    path('roadmap/' , views.roadmap , name = "roadmap") ,
    path('social/' , views.social , name = "socialpage") ,
    path('team/' , views.team , name = "team") ,
    path('blog/', views.blog, name="blog"),
    path('blog/<str:slug>/', views.blog_post, name='blog-post'),
    path('members/', views.cec_members, name="cec-members"),
    path('panel/', views.users_panel, name="panel"),
    path('panel/blog/new-post/', views.panel_new_post, name="new-post"),
    path('panel/blog/all/', views.panel_all_posts, name="all-posts"),
    path('panel/blog/<int:id>/delete', views.panel_delete_post, name="delete-post"),
    path('panel/blog/<int:id>/show/', views.panel_edit_post, name="show-post"),
    path('panel/blog/<int:id>/status/', views.panel_change_status_post, name="change-status-post"),
    path('panel/settings/', views.panel_settings, name="settings"),
    path('panel/blog/authors/', views.panel_all_authors, name="all-authors"),
    # path('send_erfan_email/', views.send_erfan_email),

]
