import csv
import sys

from datetime import date, datetime, timedelta

today = date.today()
file = sys.argv[1]

class Reminder:
    '''Base class for all reminders
    '''
    def __init__(self, reminder_type, date, text, days_in_advance=0):
        self._type = reminder_type
        try:
            self._date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError(f'Invalid date "{date}"')
        self._text = text
        self._days = timedelta(days=int(days_in_advance))

    def should_be_shown(self, ref):
        '''Whether the reminder should be shown in the output
        of the program.
        '''
        raise NotImplementedError(f'Unknown reminder type "{self._type}"')

    def report(self):
        '''Format the reminder for the output of the program.
        '''
        raise NotImplementedError(f'Unknown reminder type "{self._type}"')

class TaskReminder(Reminder):
    '''Reminder for a task. The reminder will be shown in the output once
    the provided date has passed. It will keep on showing from this point
    on until its entry is deleted from the reminder file.
    '''
    def __init__(self, date, text, days_in_advance=0):
        super().__init__('t', date, text, days_in_advance)
    
    def should_be_shown(self, ref):
        return self._date <= ref
    
    def report(self):
        return self._text
        
class BdayReminder(Reminder):
    def __init__(self, date, text, days_in_advance=1):
        super().__init__('b', date, text, days_in_advance)
    
    def should_be_shown(self, ref):
        return self.next_bday(ref) <= ref + self._days
    
    def report(self):
        days_until = (self.next_bday(today) - today).days
        if days_until == 0:
            return f'{self._text} has a birthday today'
        else:
            return f'{self._text} hasa birthday in {days_until} day(s)'

    def next_bday(self, ref):
        ref_year = ref.year
        bday_in_ref_year = self._date.replace(year=ref_year)
        if bday_in_ref_year < ref:
            return self._date.replace(year=ref_year + 1)
        else:
            return bday_in_ref_year

class AnniversaryReminder(Reminder):
    def __init__(self, date, text, days_in_advance=1):
        super().__init__('a', date, text, days_in_advance)
        
    def should_be_shown(self, ref):
        return self.next_anniversary(ref) <= ref + self._days
        
    def report(self):
        days_until = (self.next_anniversary(today) - today).days
        if days_until == 0:
            return f'{self._text} have an anniversary today'
        else:
            return f'{self._text} have an anniversary in {days_until} day(s).'
    
    def next_anniversary(self, ref):
        ref_year = ref.year
        anniversary_in_ref_year = self._date.replace(year=ref_year)
        if anniversary_in_ref_year < ref:
            return self._date.replace(year=ref_year + 1)
        else:
            return anniversary_in_ref_year

def should_be_ignored(row):
    '''Whether a row of the file should be ignored by the parser.
    There are two kinds of lines to be ignored: empty lines and
    single line comments starting with a hash sign (#).
    '''
    return (row == []) or (row[0][0] == '#')

def create_reminder(row):
    '''Use the first character of a row to create the specific
    wanted type of reminder. Unknown types will create a generic
    Reminder object which errors, alerting you of the unknown type
    (most likely a typo or an error in extension).
    '''
    if row[0] == 't':
        return TaskReminder(*row[1:])
    elif row[0] == 'b':
        return BdayReminder(*row[1:])
    elif row[0] == 'a':
        return AnniversaryReminder(*row[1:])
    else:
        return Reminder(*row)

print('Hello, here are your reminders for today:')

with open(file) as csvfile:
    reader = csv.reader(csvfile, skipinitialspace=True)
    for row in reader:
        if not should_be_ignored(row):
            reminder = create_reminder(row)
            if reminder.should_be_shown(today):
                print(f'* {reminder.report()}')
            
input("") # Keep window open until explicitly closed
