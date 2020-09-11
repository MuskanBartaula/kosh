from django import template

from nepali_date import NepaliDate

register = template.Library()


def nepali_date(value, arg):
    nepali_date = NepaliDate.to_nepali_date(value)
    formatted_nepali_date = nepali_date.strfdate(arg)
    return formatted_nepali_date

register.filter('nepali_date', nepali_date)

