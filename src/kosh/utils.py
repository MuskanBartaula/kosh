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

class NepaliDateUtils(object):
    def __init__(self, date, *args, **kwargs):
        '''
            date must be of type nepali_date.date.NepaliDate
        '''
        if not isinstance(date, type(NepaliDate)):
            raise TypeError("Date must be instance of NepaliDate class")
        self.np_date = date

    def get_month_first_day(self, date=None):
        '''
            return the first date of the np_date passed as an argument
            
            Example:
                if 2077-5-23 then it return 2077-5-01
        '''
        return NepaliDate(self.np_date.year, self.np_date.month, 1)

    def get_month_last_day(self):
        '''
            return the last date of the np_date passed as an argument

            Example:
                if 2077-05-23 then it return 2077-05-31
        '''
        return self.get_next_month() - datetime.timedelta(days=1)

    def get_prev_month(self):
        '''
            return the last date of the previous month

            Example:
                if 2077-5-23 the it return 2077-4-32
        '''
        return self.get_month_first_day() - datetime.timedelta(days=1)

    def get_next_month(self):
        '''
            date must be of type nepali_date.date.NepaliDate
        '''
        first_day = self.get_month_first_day()
        next_month = first_day + datetime.timedelta(days=35)
        next_month_first_day = NepaliDate(next_month.year, next_month.month, 1)
        return next_month_first_day

    def start_end_date_in_ad(self):
        '''
            convert the Nepali first day and last day of a month to a english date 
            date must be of type nepali_date.date.NepaliDate
        '''
        start_date = self.get_month_first_day().to_english_date()
        end_date = self.get_month_last_day().to_english_date()
        return start_date, end_date
