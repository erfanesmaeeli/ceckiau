import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from app_account.models import Profile, Staff
from django.http import HttpResponseRedirect , HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout, login, authenticate
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from random import randint
import re


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

def signup(request):
    error_email = False
    error_password = False
    error_username = False
    error_ok = False

    if request.method == 'POST':
        fname = request.POST.get("cecfname")
        lname = request.POST.get("ceclname")
        university = request.POST.get("cecuniversity_type")
        email = request.POST.get("cecemail")
        try:
            username = request.POST.get("cecusername")
        except:
            username = False
        phone = request.POST.get("cecphonenumber")
        password = request.POST.get("cecpassword")
        password_repeat = request.POST.get("cecpassword-repeat")
        if username:
            join_uni = str(username)
            if join_uni[0:3] == "399" :
                join_uni = 99
            else:
                join_uni = join_uni[0:2]
            if User.objects.filter(username=username).exists() == True:
                a = 1
                return render(request, "signup.html" , {"a":a})

        if Profile.objects.filter(email=email).exists() == True:
            b = 1
            return render(request, "signup.html" , {"b":b})
        if password != password_repeat:
            c = 1
            return render(request, "signup.html" , {"c":c})
        if phone is not None :
            if Profile.objects.filter(phone=phone).exists() == True:
                d = 1
                return render(request, "signup.html" , {"d":d})
        if re.compile(r'[a-z]').match(fname) or re.compile(r'[A-Z]').match(fname) :
            e = 1
            return render(request, "signup.html" , {"e":e})
        if re.compile(r'[a-z]').match(lname) or re.compile(r'[A-Z]').match(lname) :
            f = 1
            return render(request, "signup.html" , {"f":f})

		# check username is valid
        # username = str(username)
        # if len(username) != 9:
        #     d = 1
        #     return render(request, "signup.html" , {"d":d})
        if username:
            user = User.objects.create_user(username = username)
        else:
            user = User.objects.create_user(username=email)
        user.set_password(password)
        user.profile.fname = fname
        user.profile.lname = lname
        user.profile.university = university
        user.profile.email = email
        if username:
            user.profile.join_uni = join_uni
        if phone is not None  :
            user.profile.phone = phone
        user.first_name = fname
        user.last_name = lname
        user.email = email

        user.set_password(password)
        user.save()
        if user.save() is not None:
            error_ok = True
        email = EmailMessage(
                 'عضویت در وب سایت',
                 """<html xmlns="http://www.w3.org/1999/xhtml" dir="rtl">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0;">
  <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500" rel="stylesheet">
    <style>
    /* Reset styles */ 
    body {
      font-family: 'Roboto', Arial, sans-serif;
      height: 100% !important;
      margin: 0; 
      min-width: 100%;
      padding: 0; 
      width: 100% !important; 
    }
    body, table, td, div, p, a {
      line-height: 100%;
      text-size-adjust: 100%;
      -webkit-font-smoothing: antialiased; 
      -ms-text-size-adjust: 100%; 
      -webkit-text-size-adjust: 100%;
    }
    table, td {
      border-collapse: collapse !important; 
      border-spacing: 0;
      mso-table-lspace: 0pt; 
      mso-table-rspace: 0pt; 
    }
    img {
      border: 0; 
      line-height: 100%; 
      outline: none; 
      text-decoration: none; 
      -ms-interpolation-mode: bicubic;
    }
    .action-item {
      /*background-color: #333;*/
      border: 1px solid #005f7f;
      /*color: #fcd107;*/
      color: #005f7f;
      padding: 8px 20px;
    }
    .action-item:hover {
      background-color: #333;
      border: 1px solid #333;
      color: #fcd107;
    }
    #outlook a {padding: 0;}
    .ReadMsgBody {width: 100%;}
    .ExternalClass {width: 100%;}
    .ExternalClass, 
    .ExternalClass p, 
    .ExternalClass span, 
    .ExternalClass font, 
    .ExternalClass td, 
    .ExternalClass div {line-height: 100%;}

    /* Rounded corners for advanced mail clients only */ 
    @media all and (min-width: 560px) {
      .container {
        border-radius: 8px; 
        -webkit-border-radius: 8px; 
        -moz-border-radius: 8px; 
        -khtml-border-radius: 8px;
      }
    }
    /* Set color for auto links (addresses, dates, etc.) */ 
    a, a:hover {color: #005f7f;}
    .footer a, 
    .footer a:hover {
      color: #999999;
    }
    </style>
    <!-- MESSAGE SUBJECT -->
</head>"""
                        +f"""<body topmargin="0" rightmargin="0" bottommargin="0" leftmargin="0" marginwidth="0" marginheight="0" width="100%" style="border-collapse: collapse; border-spacing: 0; margin: 0; padding: 0; width: 100%; height: 100%; -webkit-font-smoothing: antialiased; text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; line-height: 100%; background-color: #ececec; color: #333333;" bgcolor="#ececec" text="#333333">
<!-- WRAPPER TABLE -->
<table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; border-spacing: 0; margin: 0; padding: 0; width: 100%;">
  <tr>
    <br>
    <td align="center" valign="top" style="border-collapse: collapse; border-spacing: 0; margin: 0; padding: 0;" bgcolor="#ececec">
      <!-- WRAPPER -->
      <table border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#ffffff" width="560" style="box-shadow: 0px 0px 7px 0px rgb(48, 105, 152);border-radius:5px; border-collapse: collapse; border-spacing: 0; padding: 0; width: inherit; max-width: 660px; margin: 30px 0 0 0;" class="container">
      
      <!-- PRIMARY IMAGE -->
        <tr>
          <td align="center" valign="top" style="border-collapse: collapse; border-spacing: 0; margin: 0; padding:10px; padding-top: 20px;padding-bottom:20px;    box-shadow: 0 4px 4px -2px rgb(48, 105, 152);border-radius:5px">
            <img border="0" vspace="0" hspace="0" src="https://ceckiau.ir/static/img/Logo_nav_pyblue.png" alt="CEC KIAU BRAND IMAGE" title="" width="560" style="border: none; color: #333333; display: block; font-size: 13px; margin: 0; max-width: 560px; padding: 0; outline: none; text-decoration: none; width: 65%; -ms-interpolation-mode: bicubic;"/>
          </td>
        </tr>
      
      <!-- BRANDING -->
        <tr>
          <td align="center" valign="top" style="border-collapse: collapse; border-spacing: 0; margin: 10px; padding: 10px">
            <br>
            <br>
            
            <h1 style="color: rgb(48, 105, 152); font-family: 'Roboto', Arial, sans-serif; font-size: 30px; line-height: 120%; margin-top: 10px; box-shadow:0px 2px 2px 0px rgb(48, 105, 152); padding:20px; border-radius:5px;max-width: 450px">سلام {fname} {lname} عزیز</h1>
          </td>
        </tr>
        
        <!-- SUBHEADER -->
        <tr>
          <td align="center" valign="top" style="border-collapse: collapse; border-spacing: 0; margin: 0; padding: 0; padding-bottom: 3px; padding-left: 6.25%; padding-right: 6.25%; width: 87.5%; line-height: 150%; padding-top: 5px;">
            <h3 style="color: rgb(6, 167, 125); font-family: 'Roboto', Arial, sans-serif; font-size: 29px; font-weight: 800; line-height: 120%; margin: 20px 0 10px 0; padding: 20px 0; text-align: center;box-shadow:0px 2px 2px 0px rgb(6, 167, 125);border-radius:5px">ثبت نام شما در سایت باموفقیت انجام شد</h3>
          </td>
        </tr>
        <!-- CONTENT -->
        <tr>
          <td valign="top" style="border-collapse: collapse; border-spacing: 0; margin: 0; padding: 0; padding-right: 6.25%; padding-left: 6.25%; width: 87.5%;">
          <br>
            <p style="text-align:center;font-size: 20px; font-weight: 400; line-height: 160%; color: #333333; font-family: 'Roboto', Arial, sans-serif;">با مراجعه به صفحه پروفایل میتوانید اطلاعات خود را تکمیل نمایید</p>
          <br>
          <!-- social icons -->
          <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
            <tr>
                <td class="stylingblock-content-wrapper camarker-inner">
                    <table class="c-navigation" style="text-align:center" width="100%" cellspacing="0" cellpadding="0" border="0">
                    <tr>
                <td class="social_footer" style="padding:10px 10px;width:100%;border-top:1px solid #EEEEEE" valign="top" align="center">
                <table class="container" style="min-width:100%" width="100%" cellspacing="0" cellpadding="0" border="0" align="center">
                <tr><td valign="top" align="center">
                <table style="min-width:100%" width="100%" cellspacing="0" cellpadding="0" border="0" align="center">
                <tr>
                <td valign="top" align="center">

                <a href="https://www.instagram.com/ceckiau" style="text-decoration:none;">
                  <img alt="" src="https://ceckiau.ir/static/social-icons/Instagram.png" style="display:inline; width:50px; height:50px; margin:2px 12px">
                </a>

                <a href="https://aparat.com/ceckiau" style="text-decoration:none">
                  <img alt="" src="https://ceckiau.ir/static/social-icons/aparat.png" style="display:inline; width:50px; height:50px; margin:2px 12px">
                </a>

                <a href="https://t.me/ceckiau" style="text-decoration:none">
                  <img alt="" src="https://ceckiau.ir/static/social-icons/telegram.png" style="display:inline; width:50px; height:50px; margin:2px 12px"> 
                </a>

                </td>
                </tr>
                </table>
                </td>
                </tr>
                </table>
                </td>
                </tr>
                </table>
                </td>
            </tr>
            </table>
        <!----><!---->

          </td>
        </tr> 
      </table>
      <!-- FOOTER -->
      <table border="0" cellpadding="0" cellspacing="0" align="center" width="560" style="border-collapse: collapse; border-spacing: 0; padding: 0; width: inherit; max-width: 560px;" class="wrapper">
        <tr>
          <td align="center" valign="top" style="border-collapse: collapse; border-spacing: 0; margin: 0; padding: 40px 0; font-size: 21px; font-weight: 400; line-height: 150%; color: #999999; font-family: 'Roboto', Arial, sans-serif;" class="footer">      
            <a href="https://ceckiau.ir"style="text-decoration:none">www.CECkiau.ir</a> 
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
                 """,
                 'پشتیبانی انجمن علمی مهندسی کامپیوتر' +'<support@ceckiau.ir>',
                 [email],
             )
        email.content_subtype = "html"
        email.send() 


        return render(request, "signup.html", {"error_ok" : error_ok})
    return render(request, "signup.html")

def profile(request):
    if request.method == 'POST':
        fname = request.POST.get("cecfname")
        lname = request.POST.get("ceclname")
        phone = request.POST.get("cecphonenumber")
        cecprofileavatar = request.FILES.get('cecprofileavatar')
        cecbirthday = request.POST.get("cecbirthday")
        cecsex = request.POST.get("cecsex")
        ceclive = request.POST.get("ceclive")
        cec_showprofile = request.POST.get("cec_showprofile")


        user = request.user
        i = 0
        if fname is not None  :
            user.profile.fname = fname
            i+=1
        if lname is not None  :
            user.profile.lname = lname
            i+=1
        if phone is not None  :
            user.profile.phone = phone
        if cecprofileavatar :
            user.profile.avatar = cecprofileavatar
            i+=1
        if cecbirthday is not None  :
            user.profile.birthday = cecbirthday
            i+=1
        if cecsex is not None  :
            user.profile.sex =cecsex
            i+=1
        if ceclive is not None  :
            user.profile.live =ceclive
            i+=1
        if cec_showprofile is not None :
            user.profile.show_profile = cec_showprofile
            i+=1
        if i :
            user.save()
            messages.success(request, 'تغییرات شما با موفقیت اعمال شد')
            response = redirect('/user/profile/')
            return response
        return render(request , "profile.html")
    return render(request , "profile.html")


def reset_password(request):
    global my_email

    email_is_not_exist = 0
    code_was_sent = 0
    code_was_true = 0
    code_was_false = 0
    password_is_not_ok = 0
    password_is_ok = 0
    bibot_was_false = 0

    if request.method == 'POST':
        email = request.POST.get("cecemail")
        cec_reset_code = request.POST.get("cec_reset_code")
        password = request.POST.get("cecpassword")
        password_repeat = request.POST.get("cecpassword-repeat")

        if email is not None and Profile.objects.filter(email=email).exists() == False:
            email_is_not_exist = 1
            return render(request , "resetpassword.html" , {"email_is_not_exist" : email_is_not_exist}) 

        elif email is not None and Profile.objects.filter(email=email).exists() == True:
            request.session['my_email'] = email
            code_was_sent = 1
            code = randint(10000,99999)
            user = Profile.objects.get(email=email)
            user.code = code
            user.save()
            email = EmailMessage(
                'فراموشی کلمه عبور',
                f"""<html dir="rtl">
                    <head></head>
                    <body>
                       <h2>کد امنیتی : {code}</h2>
                    </body>
                    </html>
                """,
                'پشتیبانی انجمن علمی مهندسی کامپیوتر' +'<support@ceckiau.ir>',
                [email],
                )
            email.content_subtype = "html"
            email.send()
            return render(request , "resetpassword.html" , {"code_was_sent" : code_was_sent}) 
        if cec_reset_code is not None:
            user = Profile.objects.get(email=request.session['my_email'])
            if (int(cec_reset_code) == int(user.code)):
                code_was_true = 1
                return render(request , "resetpassword.html" , {"code_was_true" : code_was_true})
            elif  int(cec_reset_code) != int(user.code) :   
                code_was_false = 1
                return render(request , "resetpassword.html" , {"code_was_false" : code_was_false})  
            elif check_bibot_response(request) == False :
                bibot_was_false = 1
                return render(request , "resetpassword.html" , {"bibot_was_false" : bibot_was_false})
        if password is not None :
            if password != password_repeat:
                password_is_not_ok = 1
                return render(request , "resetpassword.html" , {"password_is_not_ok" : password_is_not_ok}) 
            elif password == password_repeat :
                user = User.objects.get(email=request.session['my_email'])
                user.set_password(password)
                user.code = 0
                user.save()
                password_is_ok = 1
                return render(request , "resetpassword.html" , {"password_is_ok" : password_is_ok}) 

    


    return render(request , "resetpassword.html") 


def staff_signup(request):
    ctx = {}
    current_user = request.user.profile
    if Staff.objects.filter(user=request.user.profile).exists() or current_user.rank != 1:
        ctx["user_exists"] = True
        return render(request, "staff_signup.html" , ctx)

    if request.method == 'POST':
        want = request.POST.get("cec-staff-want")
        purpose = request.POST.get("cec-staff-purpose")
        skills = request.POST.get("cec-staff-skills")
        phone = request.POST.get("cec-staff-phonenumber")
        telegram = request.POST.get("cec-staff-telegram")

        request.session['want'] = want
        request.session['purpose'] = purpose
        request.session['skills'] = skills

        # if Staff.objects.filter(username=username).exists() == True:
        #     a = 1
        # if Profile.objects.filter(phone=phone).exists() == True:
        #     error_phone = 1 
        #     return render(request, "staff_signup.html" , {"error_phone":error_phone})
       
        new_staff = Staff(user=current_user, want=want , purpose=purpose, skills=skills, phone=phone, telegram=telegram, state=1)
        new_staff.save()
        current_user.phone = phone
        if new_staff is not None:
            ctx["done"] = True
        email = EmailMessage(
                 'عضویت در کادرانجمن',
                 """<html dir="rtl" lang="fa">
                        <head></head>				
                        <style>
                            img{
                                display : flex;
                                margin : 0 auto;
                            }
                            .text-blue{
                                color : rgb(48, 105, 152);
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
                            
                        </style>
                        """ + f"""
                        <body>
                            <img style = "display:flex; margin:0 auto;" src="http://s7.picofile.com/file/8382214126/Logo_nav_pyblue.png" alt="cec kiau logo" height="60" width="207">
                            <br>
                            <h2 style="color : rgb(48, 105, 152); font-weight: 600; text-align:center; direction:rtl " class="text-blue bold center">سلام {current_user.fname} {current_user.lname} عزیز ;</h2>
                            <h3 style="color : rgb(48, 105, 152); font-weight: 600; text-align:center; direction:rtl " class="text-blue bold center">درخواست عضویت شما در کادر با موفقیت ثبت گردید</h4>
                            <h3 style="color : rgb(48, 105, 152); font-weight: 600; text-align:center; direction:rtl " class="text-blue bold center">با مراجعه به صفحه پروفایل خود از ادامه مراحل عضویت خود مطلع شوید.</h3>
                            <br>
                            <h3 class="center" style = "text-align:center" >> انجمن علمی مهندسی کامپیوتر دانشگاه آزاد کرج <</h3>
                        </body>
                        </html>
                 """,
                 'پشتیبانی انجمن علمی مهندسی کامپیوتر' +'<support@ceckiau.ir>',
                 [current_user.email],
             )
        email.content_subtype = "html"
        email.send() 

        email2 = EmailMessage(
                 'درخواست عضویت در کادر',
                 """<html dir="rtl" lang="fa">
                        <head></head>				
                        <style>
                            img{
                                display : flex;
                                margin : 0 auto;
                            }
                            .text-blue{
                                color : rgb(48, 105, 152);
                            }
                            .bold{
                                font-weight: 600;
                            }
                            .right{
                                text-align: right;
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
                            
                        </style>
                        """ + f"""
                        <body>
                            <img style = "display:flex; margin:0 auto;" src="http://s7.picofile.com/file/8382214126/Logo_nav_pyblue.png" alt="cec kiau logo" height="60" width="207">
                            <br>
                            <h2 style="color : rgb(48, 105, 152); font-weight: 600; text-align:right; direction:rtl " class="text-blue bold right">نوع درخواست: عضویت در کادر</h2>
                            <h2 style="color : rgb(48, 105, 152); font-weight: 600; text-align:right; direction:rtl " class="text-blue bold right">درخواست کننده:  {current_user.fname} {current_user.lname}</h2>
                            <h3 style="color : rgb(48, 105, 152); font-weight: 600; text-align:right; direction:rtl " class="text-blue bold right">سال ورودی: {current_user.join_uni}</h3>
                            <h3 style="color : rgb(48, 105, 152); font-weight: 600; text-align:right; direction:rtl " class="text-blue bold right">توقع ایشان از انجمن :</h4>
                            <h3 style="color : #333333; font-weight: 600; text-align:right; direction:rtl" class=" bold right">{current_user.staff.want}</h4>
                            <h3 style="color : rgb(48, 105, 152); font-weight: 600; text-align:right; direction:rtl " class="text-blue bold right">هدف ایشان از عضویت :</h3>
                            <h3 style="color : #333333; font-weight: 600; text-align:right; direction:rtl" class=" bold right">{current_user.staff.purpose}</h4>
                            <h3 style="color : rgb(48, 105, 152); font-weight: 600; text-align:right; direction:rtl " class="text-blue bold right">مهارت های ایشان :</h3>
                            <h3 style="color : #333333; font-weight: 600; text-align:right; direction:rtl" class=" bold right">{current_user.staff.skills}</h4>
                            <br>
                            <h3 class="center" style = "text-align:center" >> انجمن علمی مهندسی کامپیوتر دانشگاه آزاد کرج <</h3>
                        </body>
                        </html>
                 """,
                 'مدیریت انجمن علمی مهندسی کامپیوتر' +'<support@ceckiau.ir>',
                 ["erfan.es00749@gmail.com", "fromiran98@gmail.com"],
             )
        email2.content_subtype = "html"
        email2.send()


        return render(request, "staff_signup.html", ctx)
    return render(request, "staff_signup.html")
