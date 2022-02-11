from django import template
#import khayyam
import jdatetime


register = template.Library()


def jalali_date(date):
    #jalali_date = jdatetime.date.fromgregorian(day=date.day,month=date.month,year=date.year)
    #jalali_date = khayyam.JalaliDate(jalali_date.year, jalali_date.month ,jalali_date.day)
    #jalali_date = jalali_date.strftime('%A %d / %m / %Y')
    return date

register.filter('jalali_date', jalali_date)
