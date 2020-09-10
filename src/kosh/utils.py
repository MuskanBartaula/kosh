import datetime
from nepali_date import NepaliDate

def split_date(date):
    '''
        split the year month string and return it
        format: yyyy-mm-dd
    '''
    splitted_date = date.split('-')
    year = splitted_date[0]
    month = splitted_date[1]
    day = splitted_date[2]
    return year, month, day

def bs_to_ad(date_in_bs):
    '''
     date must be in format: yyyy-mm-dd in BS
     Split the date string and convert to english date as date object
    '''
    year, month, day = split_date(date_in_bs)
    en_date = NepaliDate(year, month, day).to_english_date()
    return en_date


def get_nepali_prev_month(np_date):
    '''
        date must be of type nepali_date.date.NepaliDate
    '''
    np_month_first_day = NepaliDate(np_date.year, np_date.month, 1)
    np_prev_month = np_month_first_day - datetime.timedelta(days=1)
    return np_prev_month

def start_end_date_of_bs_to_ad(np_date):
    '''
        convert the Nepali first day and last day of a month to a english date 
        date must be of type nepali_date.date.NepaliDate
    '''
    np_start_date = NepaliDate(np_date.year, np_date.month, 1)
    np_next_month_start_date = NepaliDate(np_date.year, np_date.month + 1, 1)
    np_end_date = np_next_month_start_date - datetime.timedelta(days=1)

    start_date = np_start_date.to_english_date()
    end_date = np_end_date.to_english_date()
    return start_date, end_date
