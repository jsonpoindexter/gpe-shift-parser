# [x] you must work every day pre-event plus two shifts during event week.
# [] If your first day working is before the 23rd you may take a day off during pre event.
#   If your first working shift is on the 23rd then you must work all 3 days Pre-Event (23, 24, 25).
# [] Your WAP / Credential date will be set one day before your first shift.
#   The earliest work shift is August 18th, thus the earliest arrival is the 17th,
#   For the first time, refresh training does count towards setting the date of your arrival.
# [] Bartender shifts DO NOT COUNT for an early entry.

import csv
import itertools
from operator import itemgetter
from datetime import datetime, timedelta

main_event_start = datetime.strptime('2018-08-26 00:00', '%Y-%m-%d %H:%M')  # Main event start shift date/time
earliest_wap_date = datetime.strptime('2018-08-17 00:00', '%Y-%m-%d %H:%M')  # Earliest date/time that a WAP can be given

reader = csv.DictReader(open('2018 - I, Robot-2018-07-27.csv'))


###### Filter and sort shifts ######
shifts = []
for shift in reader:
    if shift['User ID'] is not None and shift['User ID'].strip() is not "":  # Filter out shifts that dont contain a (or empty)_  User ID value
        shifts.append(shift)

shifts = sorted(shifts, key=itemgetter('User ID'))

grouped_shifts = []
for key, value in itertools.groupby(shifts, key=itemgetter('User ID')):  # Group shifts into Lists of Dictionaries by User Id
    user_shifts = []
    for user_shift in value:
        user_shifts.append(user_shift)
    grouped_shifts.append(user_shifts)


###### Determin WAP Status ######
for user_shifts in grouped_shifts:
    first_shift = min([datetime.strptime(shift['Shift Start'],  '%Y-%m-%d %H:%M') for shift in user_shifts]) #  Deternube first scheduled shift
    wap_date = max(earliest_wap_date, first_shift - timedelta(days=1))  # Determine earliest WAP date
    pre_event_shifts_possible = (main_event_start - first_shift).days +  1  # Determine how many possible pre-event shifts can be worked

    pre_event_shifts_scheduled = []
    main_event_shifts = []
    for shift in user_shifts:
        if shift['User Nickname'] == 'Dino':
            if datetime.strptime(shift['Shift End'], '%Y-%m-%d %H:%M') < main_event_start:   # Get all shifts scheduled before main event
                pre_event_shifts_scheduled.append(shift)
            if datetime.strptime(shift['Shift Start'], '%Y-%m-%d %H:%M') > main_event_start:  # Get all shifts scheduled during main event
                main_event_shifts.append(shift)
        shift_count = len(pre_event_shifts_scheduled) + len(main_event_shifts)

    if shift_count > 0:
        print("first shift day scheduled: %s" % str(first_shift))
        print("pre event shifts possible: %s" % pre_event_shifts_possible)
        print("pre event shifts scheduled: %d" % len(pre_event_shifts_scheduled))
        print("main event shifts scheduled: %d" % len(main_event_shifts))
        print("Issue WAP Date: %s" % wap_date.strftime('%Y-%m-%d'))
