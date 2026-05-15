from django import template
from persiantools.jdatetime import JalaliDateTime, JalaliDate

register = template.Library()

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

def format_persian_number_with_separator_no_decimal(n):
    try:
        num_integer = int(float(n))
        s = str(num_integer)


        formatted_integer = ""
        count = 0
        for digit in reversed(s):
            if count > 0 and count % 3 == 0:
                formatted_integer += ','
            formatted_integer += digit
            count += 1

        formatted_integer = formatted_integer[::-1]

        return formatted_integer

    except ValueError:
        return str(n)
    except Exception as e:
        return str(n)

@register.filter(name='format_price') 
def format_price(value, currency_symbol='تومان'):

    try:
        num_value = float(value) 
        formatted_number = format_persian_number_with_separator_no_decimal(num_value)
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
    time =  datetime.strftime("%H:%M")
    return f"{date} - {time}"


@register.filter   
def get_date(value):
    print(value)
    if not value:
        return ""

    return JalaliDate(value).strftime("%Y/%m/%d")

@register.filter
def attr(obj, field_name):
    return getattr(obj, field_name)