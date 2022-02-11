from django.contrib import admin
from app_account.models import Profile, Staff
import khayyam
import jdatetime



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fname', 'lname', 'join_uni', 'email', 'university', 'rank', 'get_time')
    list_filter = ('university', 'join_uni', 'DateCreate', 'education', 'rank')
    search_fields = ('fname', 'lname', 'university', 'email', 'education', 'join_uni', 'user__username', 'phone', 'DateCreate')
    ordering = ['-DateCreate', 'lname', 'fname']
    
    def get_time(self, obj):
        jalali_date = jdatetime.date.fromgregorian(day=obj.DateCreate.day,month=obj.DateCreate.month,year=obj.DateCreate.year)
        jalali_date = khayyam.JalaliDate(jalali_date.year, jalali_date.month ,jalali_date.day)
        jalali_date = jalali_date.strftime('%A %d / %m / %Y')
        return str(jalali_date) + str(obj.DateCreate.strftime(" ساعت %H:%M"))
    get_time.short_description = 'تاریخ عضویت'


class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_fname', 'profile_lname', 'phone', 'telegram', 'profile_email', 'profile_join_uni', 'date', 'time', 'state','DateCreate')
    list_editable = ('date', 'time', 'state')
    list_filter = ('state',)
    search_fields = ('user', 'profile_fname', 'profile_lname', 'phone', 'profile_email', 'profile_join_uni')
    ordering = ['state' , 'user__join_uni', 'user__lname', 'user__fname']
    
    def profile_fname(self, x):
        return x.user.fname
    profile_fname.short_description = 'نام'

    def profile_lname(self, x):
        return x.user.lname
    profile_lname.short_description = 'نام خانوادگی'

    def profile_email(self, x):
        return x.user.email
    profile_email.short_description = 'ایمیل'

    def profile_join_uni(self, x):
        return x.user.join_uni
    profile_join_uni.short_description = 'سال ورودی'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Staff, StaffAdmin)
