from django import template
from persiantools.jdatetime import JalaliDateTime, JalaliDate

register = template.Library()

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='format_price') 
def format_price(value, currency_symbol='تومان'):
    try:
        num_value = float(value)
        formatted_number = (num_value)
        return f"{formatted_number} {currency_symbol}"

    except ValueError:
        return str(value)
    except Exception as e:
        return str(value)
    
    
@register.filter
def locale_date(value):
    if not value:
        return ""

    months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد',
                'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    
    datetime = JalaliDateTime(value)
    date = f"{datetime.day} {months[datetime.month-1]} {datetime.year}"
    time =  datetime.strftime("%H:%M:%S")
    return f"{date} - {time}"


@register.filter   
def get_date(value):
    print(value)
    if not value:
        return ""

    return JalaliDate(value).strftime("%Y/%m/%d")
