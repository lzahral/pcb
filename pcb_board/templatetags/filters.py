from django import template
from persiantools.jdatetime import JalaliDateTime, JalaliDate

register = template.Library()

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()
persian_digits = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

# def format_persian_number_with_separator_no_decimal(n):

#     try:
#         num_integer = int(float(n))
#         s = str(num_integer)


#         integer_part_persian = s.translate(persian_digits)

#         # اضافه کردن جداکننده هزارگان به بخش صحیح
#         formatted_integer = ""
#         count = 0
#         # از انتهای رشته شروع به پیمایش می‌کنیم
#         for digit in reversed(integer_part_persian):
#             if count > 0 and count % 3 == 0:
#                 formatted_integer += ',' # یا '.' اگر جداکننده نقطه می‌خواهید
#             formatted_integer += digit
#             count += 1

#         # برعکس کردن رشته برای رسیدن به ترتیب درست
#         formatted_integer = formatted_integer[::-1]

#         return formatted_integer

#     except ValueError:
#         # اگر ورودی قابل تبدیل به عدد صحیح نبود
#         return str(n)
#     except Exception as e:
#         # print(f"Error in format_persian_number_with_separator_no_decimal: {e}")
#         return str(n)

@register.filter(name='format_price') 
def format_price(value, currency_symbol='تومان'):

    try:
        num_value = float(value) # همچنان اول به float تبدیل می‌کنیم تا اعشارش حذف شود

        # استفاده از تابع کمکی به‌روز شده
        formatted_number = (num_value)

        # اضافه کردن نماد واحد پول
        return f"{formatted_number} {currency_symbol}"

    except ValueError:
        return str(value)
    except Exception as e:
        # print(f"Error in format_price_no_decimal: {e}")
        return str(value)
@register.filter
def locale_date(value):
    print(value)
    if not value:
        return ""

    months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد',
                'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    datetime = JalaliDate(value)
    date = f"{datetime.day} {months[datetime.month-1]} {datetime.year}"
    date = date.translate(persian_digits)
    return f"{date}"
@register.filter   

def get_date(value):
    print(value)
    if not value:
        return ""

    return JalaliDate(value).strftime("%Y/%m/%d").translate(persian_digits)
