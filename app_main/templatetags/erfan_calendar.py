from django import template
# import khayyam


register = template.Library()


def jalali_date(date):
    #jalali_date = khayyam.JalaliDate(date.year, date.month ,date.day)
    #jalali_date = jalali_date.strftime('%A %d / %m / %Y')
    return date

register.filter('jalali_date', jalali_date)
