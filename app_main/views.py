import requests
from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from app_main.models import Slider , RoadMap , Team, Blog, CecMembers, AttachmentFiles
from app_course.models import Course
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
import re
from django.contrib import messages
from app_account.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import jdatetime
from app_main.forms import Post_Form
from django.db.models import Q
from django.template.loader import render_to_string
from django.db.models import Count


def users_panel(request):
    template = "panel/index.html"
    ctx = {}
    if request.user.is_anonymous:
        return HttpResponse("Permission denied. Login First")
    elif not request.user.profile.is_author and not request.user.is_superuser:
        return HttpResponse("Permisson denied.You are not admin in ceckiau.ir")
    user = request.user
    profile = request.user.profile
    ctx["user"] = user
    ctx["profile"] = profile
    
    if profile.phone and profile.email and profile.fname and profile.lname and profile.live and profile.birthday and profile.sex:
        ctx["user_full_data"] = True
    else:
        ctx["user_full_data"] = False

    return render(request, template, ctx)


def panel_new_post(request):
    template = "panel/new_post.html"
    ctx = {}
    if request.user.is_anonymous:
        return HttpResponse("Permission denied. Login First")
    elif not request.user.profile.is_author and not request.user.is_superuser:
        return HttpResponse("Permisson denied.You are not admin or author")
    user = request.user
    profile = request.user.profile
    ctx["user"] = user
    ctx["profile"] = profile

    new_post_form = Post_Form(request.POST or None, request.FILES or None, request=request, initial={'author': user})
    ctx["form"] = new_post_form

    if request.method == 'POST':
        if new_post_form.is_valid():
            if Blog.objects.filter(Q(slug=new_post_form.cleaned_data['slug']) | Q(slug=new_post_form.cleaned_data['title'].replace(' ', '-'))).exists():
                ctx["has_exists"] = True

            else:
                new_post = new_post_form.save()
                publish = new_post_form.cleaned_data['publish']
                if not new_post_form.cleaned_data['slug']:
                    new_post.slug = new_post_form.cleaned_data['title'].replace(' ', '-')
                if user.is_superuser:
                    if publish:
                        new_post.status = 2
                    else:
                        new_post.status = 4

                else:
                    if publish:
                        new_post.status = 1

                        # Email Configs
                        the_user = new_post_form.cleaned_data['author']
                        user_subject_waiting = "ایجاد پست جدید (درانتظار تایید)"
                        admin_subject_post_request = "پست جدید توسط نویسنده انجمن"
                        user_email_template_waiting = "panel/emails/to_user_post_waiting.html"
                        admin_email_template_post_request = "panel/emails/to_admin_post_request.html"
                        c = {
                        "user": the_user,
                        'post': new_post,
                        }
                        user_email_waiting = render_to_string(user_email_template_waiting, c)
                        admin_email_post_request = render_to_string(admin_email_template_post_request, c)

                        # send email to user (change status)
                        try:
                            send_mail(user_subject_waiting, user_email_waiting, 'CECkiau <support@ceckiau.ir>' , [the_user.email], fail_silently=False)
                        except:
                            messages.error(request, 'در ارسال ایمیل به نویسنده مشکلی پیش آمده. به اطلاع مدیر برسانید')

                        # send email to admin (post change status)
                        try:
                            send_mail(admin_subject_post_request, admin_email_post_request, 'CECkiau <support@ceckiau.ir>' , ["erfan.es00749@gmail.com", "fromiran98@gmail.com"], fail_silently=False)
                        except:
                            messages.error(request, 'در ارسال ایمیل به مدیر سایت مشکلی پیش آمده. به اطلاع مدیر برسانید')
                    else:
                        new_post.status = 4

                        # Email Configs
                        the_user = new_post_form.cleaned_data['author']
                        user_subject_waiting = "ایجاد پست جدید (درانتظار تایید)"
                        user_email_template_waiting = "panel/emails/to_user_post_waiting.html"
                        c = {
                        "user": the_user,
                        'post': new_post,
                        }
                        user_email_waiting = render_to_string(user_email_template_waiting, c)

                        # send email to user (change status)
                        try:
                            send_mail(user_subject_waiting, user_email_waiting, 'CECkiau <support@ceckiau.ir>' , [the_user.email], fail_silently=False)
                        except:
                            messages.error(request, 'در ارسال ایمیل به نویسنده مشکلی پیش آمده. به اطلاع مدیر برسانید')


                new_post.save()

                ctx["done"] = True
                if not publish:
                    ctx["draft"] = True
                ctx["post_url"] = "/panel/blog/" + str(new_post.id) + "/show/"

    return render(request, template, ctx)


def panel_all_posts(request):
    template = "panel/all_posts.html"
    ctx = {}
    if request.user.is_anonymous:
        return HttpResponse("Permission denied. Login First")
    elif not request.user.profile.is_author and not request.user.is_superuser:
        return HttpResponse("Permisson denied.You are not admin or author")
    user = request.user
    profile = request.user.profile
    if user.is_superuser:
        all_blog = Blog.objects.all().order_by('-_DateCreate')
    else:
        all_blog = Blog.objects.filter(author=user).order_by('-_DateCreate')
    ctx["user"] = user
    ctx["profile"] = profile
    ctx["blog"] = all_blog

    return render(request, template, ctx)


def panel_delete_post(request, id):
    if request.user.is_anonymous:
        return HttpResponse("Permission denied. Login First")
    elif not request.user.profile.is_author and not request.user.is_superuser:
        return HttpResponse("Permisson denied.You are not admin or author")
    if request.method == 'POST':
        try:
            post = Blog.objects.get(id=id)
            profile = request.user.profile
            user = request.user
            if user.is_superuser or post.author == user:
                post.delete()
                messages.success(request, 'پست حذف گردید')
                return redirect('/panel/blog/all/')
        except Exception as e:
            messages.error(request, 'مشکلی پیش آمده مجدد تلاش کنید')
            return redirect('/panel/blog/all/')

def panel_edit_post(request, id):
    template = "panel/edit_post.html"
    ctx = {}
    if request.user.is_anonymous:
        return HttpResponse("Permission denied. Login First")
    elif not request.user.profile.is_author and not request.user.is_superuser:
        return HttpResponse("Permisson denied.You are not admin or author")
    post = get_object_or_404(Blog, id=id)
    profile = request.user.profile
    user = request.user
    ctx["post"] = post
    ctx["user"] = user
    ctx["profile"] = profile
    counter = 0

    post_form = Post_Form(request.POST or None, request.FILES or None, request=request, instance=post)

    ctx["form"] = post_form
    if user.is_superuser or post.author == user:
        if request.method == 'POST':
            if post_form.is_valid():

                # if post.slug != post_form.cleaned_data['slug']:
                #     post_slug_edit = True
                #     counter += 1
                #
                # if post.publish != post_form.cleaned_data['publish']:
                #     post_publish_edit = True
                #     counter += 1
                #
                # if post.title != post_form.cleaned_data['title']:
                #     post_title_edit = True
                #     counter += 1
                #
                # if int(post.category) != int(post_form.cleaned_data['category']):
                #     post_category_edit = True
                #     counter += 1
                #
                # if post.image != post_form.cleaned_data['image']:
                #     post_image_edit = True
                #     counter += 1
                #
                # if post.text != post_form.cleaned_data['text']:
                #     post_content_edit = True
                #     counter += 1
                #
                # if post.meta_description != post_form.cleaned_data['meta_description']:
                #     post_meta_edit = True
                #     counter += 1

                post_form.save()
                
                if not user.is_superuser:
                    post.status = 1
                
                if post_form.cleaned_data['publish']:
                    if request.user.profile.is_author and not request.user.is_superuser and post.status == 4:
                        post.status = 1

                        # Email Configs
                        the_user = post.author
                        user_subject_edited_waiting = "تکمیل و ثبت پست (درانتظار تایید)"
                        admin_subject_post_edited = "تکمیل و ثبت پست توسط نویسنده انجمن"
                        user_email_template_edited_waiting = "panel/emails/to_user_post_edited_waiting.html"
                        admin_email_template_post_edited = "panel/emails/to_admin_post_edited.html"
                        c = {
                        "user": the_user,
                        'post': post,
                        }
                        user_email_edited_waiting = render_to_string(user_email_template_edited_waiting, c)
                        admin_email_post_edited = render_to_string(admin_email_template_post_edited, c)

                        # send email to user (edited)
                        try:
                            send_mail(user_subject_edited_waiting, user_email_edited_waiting, 'CECkiau <support@ceckiau.ir>' , [the_user.email], fail_silently=False)
                        except:
                            messages.error(request, 'در ارسال ایمیل به نویسنده مشکلی پیش آمده. به اطلاع مدیر برسانید')

                        # send email to admin (post edited)
                        try:
                            send_mail(admin_subject_post_edited, admin_email_post_edited, 'CECkiau <support@ceckiau.ir>' , ["erfan.es00749@gmail.com", "fromiran98@gmail.com"], fail_silently=False)
                        except:
                            messages.error(request, 'در ارسال ایمیل به مدیر سایت مشکلی پیش آمده. به اطلاع مدیر برسانید')

                elif not post_form.cleaned_data['publish']:
                    post.status = 4

                    # Email Configs
                    the_user = post.author
                    user_subject_edited_waiting = "پست شما پیش نویس شد"
                    user_email_template_edited_waiting = "panel/emails/to_user_post_status.html"
                    c = {
                    "user": the_user,
                    'post': post,
                    }
                    user_email_edited_waiting = render_to_string(user_email_template_edited_waiting, c)

                    # send email to user (edited)
                    try:
                        send_mail(user_subject_edited_waiting, user_email_edited_waiting, 'CECkiau <support@ceckiau.ir>' , [the_user.email], fail_silently=False)
                    except:
                        messages.error(request, 'در ارسال ایمیل به نویسنده مشکلی پیش آمده. به اطلاع مدیر برسانید')

                post.LastEdit = jdatetime.datetime.now()

                
                post.save()

                messages.success(request, 'پست آپدیت شد')
                return redirect('app-main:show-post', id=id)

        return render(request, template, ctx)
    else:
        messages.error(request, 'مجاز به دیدن این پست نمی‌باشید')
        return redirect('/panel/blog/all/')

def panel_change_status_post(request, id):
    if request.user.is_anonymous:
        return HttpResponse("Permission denied. Login First")
    elif request.user.is_superuser:
        if request.method == 'POST':
            post_accepted, post_not_accepted, post_waiting = False, False, False

            post_accepted = request.POST.get("cec_post_accepted")
            post_not_accepted = request.POST.get("cec_post_not_accepted")
            post_waiting = request.POST.get("cec_post_waitng")

            post = Blog.objects.get(id=id)
            if post_accepted:
                post.status = 2

                # Email Configs
                the_user = post.author
                user_subject_accepted = "تایید پست شما"
                user_email_template_waiting = "panel/emails/to_user_post_accepted.html"
                c = {
                "user": the_user,
                'post': post,
                }
                user_email_accepted = render_to_string(user_email_template_waiting, c)

                # send email to user (waiting)
                try:
                    send_mail(user_subject_accepted, user_email_accepted, 'CECkiau <support@ceckiau.ir>' , [the_user.email], fail_silently=False)
                except:
                    messages.error(request, 'در ارسال ایمیل به نویسنده مشکلی پیش آمده. به اطلاع مدیر برسانید')

            elif post_not_accepted:
                post.status = 3

                # Email Configs
                the_user = post.author
                user_subject_accepted = "تغییر وضعیت پست شما"
                user_email_template_waiting = "panel/emails/to_user_post_status.html"
                c = {
                "user": the_user,
                'post': post,
                }
                user_email_accepted = render_to_string(user_email_template_waiting, c)

                # send email to user (waiting)
                try:
                    send_mail(user_subject_accepted, user_email_accepted, 'CECkiau <support@ceckiau.ir>' , [the_user.email], fail_silently=False)
                except:
                    messages.error(request, 'در ارسال ایمیل به نویسنده مشکلی پیش آمده. به اطلاع مدیر برسانید')

            elif post_waiting:
                post.status = 1
                # Email Configs
                the_user = post.author
                user_subject_accepted = "تغییر وضعیت پست شما"
                user_email_template_waiting = "panel/emails/to_user_post_status.html"
                c = {
                "user": the_user,
                'post': post,
                }
                user_email_accepted = render_to_string(user_email_template_waiting, c)

                # send email to user (waiting)
                try:
                    send_mail(user_subject_accepted, user_email_accepted, 'CECkiau <support@ceckiau.ir>' , [the_user.email], fail_silently=False)
                except:
                    messages.error(request, 'در ارسال ایمیل به نویسنده مشکلی پیش آمده. به اطلاع مدیر برسانید')

            post.save()
            messages.success(request, 'پست آپدیت شد')
            return redirect('/panel/blog/all/')
    else:
        return HttpResponse("Permisson denied.You are not admin or author")


def panel_settings(request):
    if request.user.is_anonymous:
        return HttpResponse("Permission denied. Login First")
    template = "panel/settings.html"
    user = request.user
    profile = request.user.profile
    user_full_name = profile.fname + " " + profile.lname
    ctx = {}
    ctx["user"] = user
    ctx["profile"] = profile
    ctx["user_full_name"] = user_full_name
    if request.method == 'POST':

        fname = request.POST.get("cecfname")
        lname = request.POST.get("ceclname")
        email = request.POST.get("email")
        phone = request.POST.get("cecphonenumber")
        sex = request.POST.get("cecsex")
        live = request.POST.get("ceclive")
        profileavatar = request.FILES.get('cecprofileavatar')
        birthday = request.POST.get("cecbirthday")
        bio = request.POST.get("cecbio")
        try:
            username = request.POST.get("cecusername")
        except:
            username = False

        user.first_name, profile.fname = fname, fname
        user.last_name, profile.lname = lname, lname
        user.email, profile.email = email, email
        if username:
            user.username = username
        if phone:
            profile.phone = phone
        if sex:
            profile.sex = sex
        if live:
            profile.live = live

        if profileavatar:
            profile.avatar = profileavatar
        if birthday:
            profile.birthday = birthday
        if bio:
            profile.bio = bio

        try:
            user.save()
            profile.save()
            messages.success(request, 'تغییرات اعمال شد')
            return redirect('app-main:settings')
        except Exception as e:
            messages.error(request, 'مشکلی پیش آمده مجدد تلاش کنید')

    return render(request, template, ctx)
    
def panel_all_authors(request):
    if request.user.is_anonymous:
        return HttpResponse("Permission denied. Login First")

    if not request.user.is_superuser:
        return HttpResponse("Permisson denied.You are not admin in ceckiau.ir")

    template = "panel/authors.html"
    ctx = {}
    ctx["user"] = request.user
    ctx["profile"] = request.user.profile
    ctx["authors"] = Profile.objects.filter(is_author=True).annotate(num_posts=Count('user__author')).order_by('-num_posts')
    return render(request, template, ctx)

def check_bibot_response(request):
    if request.POST.get('bibot-response') is not None:
        if request.POST.get('bibot-response') != '':
            r = requests.post('https://api.bibot.ir/api1/siteverify/', data={
                'secret': 'your_site_key',
                'response': request.POST['bibot-response']
            })
            print(r.json())
            if r.json()['success']:
                # messages.success(request, 'فرایند تایید هویت شما با موفقیت انجام شد!')
                return True
            elif r.json()['error-codes']:
                for error_code in r.json()['error-codes']:
                    messages.error(request, error_code)
                return False
            else:
                # messages.error(request, 'بی‌بات به درستی حل نشده است!')
                return False
        else:
            # messages.error(request, 'بی‌بات به درستی حل نشده است!')
            return False
    # messages.error(request, 'ارتباط با سرور بی‌بات برقرار نشده است! آیا جاوااسکریپت شما فعال است؟')
    return False

def coming_soon(request):
    return render(request, "coming_soon.html")


def social(request):
    return render(request, "social.html")

def blog(request):
    post_list = Blog.objects.filter(publish=True, status=2).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "blog.html", {"post_list":post_list ,'page_obj': page_obj})

def blog_post(request, slug):
    ctx= {}
    post = Blog.objects.get(slug=slug) 
    if post.publish and post.status ==2:
        ctx["post"] = post
        ctx["attachment_files"] = post.files.all()
    elif post.author == request.user or request.user.is_superuser:
        ctx["post"] = post
        ctx["draft"] = True
        ctx["attachment_files"] = post.files.all()
    else:
        return render(request, "404.html")
    
    
    return render(request, "blog_post.html", ctx)


def team(request):
    team_list = Team.objects.all().order_by('id')
    return render(request, "team.html", {"team_list":team_list})

def cec_members(request):
    years = []
    ctx = {}
    has_staff = []
    years.append(CecMembers.objects.first().year.get_year)
    all_members_central = CecMembers.objects.all().exclude(rank__rank_type = 'اعضای کادر').order_by('rank__order')
    for i in all_members_central:
        if i.year.get_year not in years:
            years.append(i.year.get_year)
    all_members_staff = CecMembers.objects.filter(rank__rank_type = 'اعضای کادر').order_by('rank__order')
    for staff in all_members_staff:
        for y in years:
            if staff.year.get_year == y and y not in has_staff:
                has_staff.append(y)
    ctx["has_staff"] = has_staff
    years = sorted(years)
    years = years[::-1]
    ctx["central_members"] = all_members_central
    ctx["staff_members"] = all_members_staff
    page = request.GET.get('page', 1)
    paginator = Paginator(years, 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    ctx["years"] = page_obj
    return render(request, "cec_members.html", ctx)


# def send_my_email(request):
#     users = Profile.objects.all()
#     for user in users:
#         email = EmailMessage(
#                  'Happy Engineer Day',
#                  """
#                  <html dir="rtl" lang="fa">
#                         <head></head>
#                         <style>
#                             img{
#                                 display : flex;
#                                 margin : 0 auto;
#                             }
#                             .text-blue{
#                                 color : #306998;
#                             }
#                             .bold{
#                                 font-weight: 600;
#                             }
#                             .center{
#                                 text-align: center;
#                             }
#                             .justify{
#                                 text-align:justify;
#                                 line-height : 2
#                             }
#                             h1 , h2 , h3 , h4 , h5 , h6 , p{
#                                 direction: rtl !important;
#                             }
#                             .im , .hx .ii{
#                                direction: rtl !important;
#                             }
#                             .mybtn{
#                                 display: block;
#                                 width: 170px;
#                                 margin: 0 auto;
#                                 text-align: center;
#                                 font-weight: 600;
#                                 outline: none;
#                                 border-radius: 50px;
#                                 border: 1px solid #cdcdcd;
#                                 font-style: normal;
#                                 text-decoration: none !important;
#                                 padding: 10px;
#                                 color: black;
#                                 transition: 0.5s ease;
#                             }
#                             .mybtn:hover{
#                                 background :  #306998;
#                                 color : white !important;
#                                 transition: 0.5s ease;
#                                 border : solid 1px black
#                             }
#                         </style>"""
#                         +f"""<body>
#                             <br>
#                             <img style = "display:flex; margin:0 auto;" src="https://ceckiau.ir/media/blog-main-image/engineer-day.jpg" alt="cec kiau logo" height="233" width="350">
#                             <h1 style="color : #306998; font-weight: 600; text-align:center; direction:rtl " class="bold center">سلام {user.fname} {user.lname} 🌷</h1>
#                             <h2 style="color : #306998; font-weight: 600; text-align:center; direction:rtl" class="bold center"> 🖥 روزت مبارک مهندس عزیز 🖥</h2>
#                             <h2 style="color : #306998; font-weight: 600; text-align:center; direction:rtl " class="bold center">ما دنیای جادویی قدرتمند، هوشمند و با ارتباط را میسازیم </h2>                            <hr style= "width:50%">



#                             <h3 class="center" style = "text-align:center" >** انجمن علمی مهندسی کامپیوتر دانشگاه آزاد کرج **</h3>
#                             <a class="mybtn" href="https://ceckiau.ir" style = "display: block;
#                                 width: 170px;
# 								margin: 0 auto;
#                                 text-align: center;
#                                 font-weight: 600;
#                                 outline: none;
#                                 border-radius: 50px;
#                                 border: 1px solid #cdcdcd;
#                                 font-style: normal;
#                                 text-decoration: none !important;
#                                 padding: 10px;
#                                 color: black;
#                                 transition: 0.5s ease;">www.CECkiau.ir</a>
#                         </body>
#                         </html>
#                  """,
#                  'روابط عمومی انجمن علمی مهندسی کامپیوتر' +'<support@ceckiau.ir>',
#                  [user.email],
#              )
#         email.content_subtype = "html"
#         email.send()
#     return HttpResponse("Done!")

def send_erfan_email(request):
    users = Profile.objects.all()
    for user in users:
        email = EmailMessage(
                 'Happy Student Day 1399',
                 """<html dir="rtl" lang="fa">
                        <head></head>
                        <style>
                            img{
                                display : flex;
                                margin : 0 auto;
                            }
                            .text-blue{
                                color : #306998;
                            }
                            .bold{
                                font-weight: 600;
                            }
                            .center{
                                text-align: center;
                            }
                            .justify{
                                text-align:justify;
                                line-height : 2
                            }
                            h1 , h2 , h3 , h4 , h5 , h6 , p{
                                direction: rtl !important;
                            }
                            .im , .hx .ii{
                               direction: rtl !important;
                            }
                            .mybtn{
                                display: block;
                                width: 170px;
                                margin: 0 auto;
                                text-align: center;
                                font-weight: 600;
                                outline: none;
                                border-radius: 50px;
                                border: 1px solid #cdcdcd;
                                font-style: normal;
                                text-decoration: none !important;
                                padding: 10px;
                                color: black;
                                transition: 0.5s ease;
                            }
                            .mybtn:hover{
                                background :  #306998;
                                color : white !important;
                                transition: 0.5s ease;
                                border : solid 1px black
                            }
                        </style>"""
                        +f"""<body>
                            <br>
                            <img style = "display:flex; margin:0 auto;" src="https://ceckiau.ir/media/blog-main-image/Student-Day.png" alt="cec kiau logo" height="300" width="300">
                            <h1 style="color : #306998; font-weight: 600; text-align:center; direction:rtl " class="bold center">سلام {user.fname} {user.lname} 🌷</h1>
                            <h2 style="color : #306998; font-weight: 600; text-align:center; direction:rtl" class="bold center"> 🖥 روزت مبارک کامپیوتری عزیز 🖥</h2>
                            <h3 style="color : #06a77d; font-weight: 600; text-align:center; direction:rtl " class="bold center">برایتان یک کلیپ از دانشگاه آماده کرده‌ایم که میتوانید در لینک زیر آنرا مشاهده کنید. 😊</h3>                            <hr style= "width:50%">
                            <a href="https://ceckiau.ir/blog/Happy-Student-Day-1399/"> <h2 style="color : #306998; font-weight: 600; text-align:center; direction:rtl" class="bold center"> مشاهده کلیپ </h2></a>


                            <h3 class="center" style = "text-align:center" >** انجمن علمی مهندسی کامپیوتر دانشگاه آزاد کرج **</h3>
                            <a class="mybtn" href="https://ceckiau.ir" style = "display: block;
                                width: 170px;
                                margin: 0 auto;
                                text-align: center;
                                font-weight: 600;
                                outline: none;
                                border-radius: 50px;
                                border: 1px solid #cdcdcd;
                                font-style: normal;
                                text-decoration: none !important;
                                padding: 10px;
                                color: black;
                                transition: 0.5s ease;">www.CECkiau.ir</a>
                        </body>
                        </html>

                 """,
                 'روابط عمومی انجمن علمی مهندسی کامپیوتر' +'<support@ceckiau.ir>',
                 [user.email],
                )
        email.content_subtype = "html"
        try:
            email.send()
        except:
            pass
    return HttpResponse("Done!")

def roadmap(request):
    ctx = {}
    ctx["roadmap"] = RoadMap.objects.all().order_by('-id')
    ctx["roadmap_completed"] = RoadMap.objects.filter(state=1).order_by('-DateCreate')

    return render(request , "roadmap.html" , ctx)


def home(request):
    courses_list = Course.objects.all().order_by('-id')
    myslider = Slider.objects.filter(publish=True).order_by('-id')[1:]
    last_slide = Slider.objects.filter(publish=True).order_by('-id')[0]
    i = 0
    while last_slide.publish !=True:
          last_slide = Slider.objects.all().order_by('-id')[i+1]

    return render(request , "home.html" , {"myslider" : myslider , "last_slide":last_slide, "courses_list":courses_list})


def login_(request):
    errorـusername = False
    errorـpassword = False
    error = False
    error_captcha = False
    if request.method == 'POST':
        username = (request.POST.get("cecusername")).lower()
        password = request.POST.get("cecpassword")
        user = authenticate(request, username=username, password=password)

        if User.objects.filter(username=username).exists() == False:
            errorـusername = True
        elif user is None:
            errorـpassword = True
        elif check_bibot_response(request) == False :
            error_captcha = True
        myslider = Slider.objects.filter(publish=True).order_by('-id')[1:]
        last_slide = Slider.objects.filter(publish=True).order_by('-id')[0]
        i = 0
        while last_slide.publish !=True:
            if last_slide.publish ==False:
                last_slide = Slider.objects.all().order_by('-id')[i+1]
        context = {
            "errorـusername" : errorـusername,
            "errorـpassword" : errorـpassword,
            "error_captcha" : error_captcha,
            "myslider" : myslider ,
            "last_slide" : last_slide
        }
        referer = request.META.get('HTTP_REFERER')
        referer = re.sub('^https?:\/\/', '', referer).split('/')
        my_url = ""
        for i in range(1,len(referer),1):
            my_url += "/"+referer[i]
#check_bibot_response(request)
        if user is not None and errorـpassword==False and errorـusername==False:
            login(request, user)
            messages.success(request, 'شما با موفقیت وارد سایت شدید')
            if my_url == "/login/" or my_url == "/user/signup/" or my_url == "/user/reset-password/" or my_url == "/":
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect("/")
        if request.path =="/login/"  :
            return render(request , "home.html" ,context)
        elif request.path =="/user/signup/":
            return render(request , "signup.html" ,context)
    return HttpResponse("کار خوبی نکردی !!!")


def logout_(request):
    logout(request)
    messages.info(request, 'شما با موفقیت از سایت خارج شدید')
    if request.META.get('HTTP_REFERER'):
        referer = request.META.get('HTTP_REFERER')
        referer = re.sub('^https?:\/\/', '', referer).split('/')
        my_url = ""
        for i in range(1,len(referer),1):
            my_url += "/"+referer[i]
        for i in ["/panel/",]:
            if i in my_url:
                return HttpResponseRedirect("/")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
