# [x] you must work every day pre-event plus two shifts during event week.
# [x] If your first day working is before the 23rd you may take a day off during pre-event.
# [x] If your first working shift is on the 23rd then you must work all 3 days Pre-Event (23, 24, 25).
# [x] Your WAP / Credential date will be set one day before your first shift.
# [x] The earliest work shift is August 18th, thus the earliest arrival is the 17th,
# [x] For the first time, refresh training does count towards setting the date of your arrival.
# [] Bartender shifts DO NOT COUNT for an early entry.

import csv
import itertools
from operator import itemgetter
from datetime import datetime, timedelta
import json

main_event_start = datetime.strptime('2018-08-26 00:00', '%Y-%m-%d %H:%M')  # Main event start shift date/time
earliest_wap_date = datetime.strptime('2018-08-17 00:00',
                                      '%Y-%m-%d %H:%M')  # Earliest date/time that a WAP can be given
day_off_date = datetime.strptime('2018-08-23 00:00',
                                 '%Y-%m-%d %H:%M')  # If your first day working is before the 23rd you may take a day off during pre-event.

reader = csv.DictReader(open('2018 - I, Robot-2018-07-27.csv'))

###### Filter and sort shifts ######
shifts = []
for shift in reader:
    if shift['User ID'] is not None and shift[
        'User ID'].strip() is not "":  # Filter out shifts that dont contain a (or empty)_  User ID value
        shifts.append(shift)

shifts = sorted(shifts, key=itemgetter('User ID'))

grouped_shifts = []
for key, value in itertools.groupby(shifts,
                                    key=itemgetter('User ID')):  # Group shifts into Lists of Dictionaries by User Id
    user_shifts = []
    for user_shift in value:
        user_shifts.append(user_shift)
    grouped_shifts.append(user_shifts)

###### Determin WAP Status ######
for user_shifts in grouped_shifts[0:3]:
    print("")

    first_shift_date = min([datetime.strptime(shift['Shift Start'], '%Y-%m-%d %H:%M') for shift in
                            user_shifts])  # Deternube first scheduled shift
    wap_date = max(earliest_wap_date, first_shift_date - timedelta(days=1))  # Determine earliest WAP date
    pre_event_shifts_possible = ( main_event_start - first_shift_date).days + 1  # Determine how many possible pre-event shifts can be worked
    qualifies_day_off = first_shift_date < day_off_date  # If first day working is before the 23rd user may take a day off during pre-event.
    all_pre_event = day_off_date <= first_shift_date < main_event_start  # If first working shift is on the 23rd then user must work all 3 days Pre-Event (23, 24, 25).

    pre_event_shifts_scheduled = []
    main_event_shifts = []
    for shift in user_shifts:
        if datetime.strptime(shift['Shift End'],
                             '%Y-%m-%d %H:%M') < main_event_start:  # Get all shifts scheduled before main event
            pre_event_shifts_scheduled.append(shift)
        if datetime.strptime(shift['Shift Start'],
                             '%Y-%m-%d %H:%M') > main_event_start:  # Get all shifts scheduled during main event
            main_event_shifts.append(shift)
    shift_count = len(pre_event_shifts_scheduled) + len(main_event_shifts)
    main_event_shifts = len(main_event_shifts)
    pre_event_shifts_scheduled = len(pre_event_shifts_scheduled)

    # Determine how many pre-event shifts need to be worked based on previous variables
    if qualifies_day_off:
        required_pre_event_shifts = pre_event_shifts_possible - 1
    elif all_pre_event:
        required_pre_event_shifts = pre_event_shifts_possible
    else:
        required_pre_event_shifts = None

    met_main_event_requirements = main_event_shifts >= 2
    met_event_requirements = required_pre_event_shifts == pre_event_shifts_scheduled

    wap_status = met_main_event_requirements and met_event_requirements

    if shift_count > 0:
        print("User ID: %s" % user_shifts[0]['User ID'])
        print("first shift day scheduled: %s" % str(first_shift_date))
        print("pre-event shifts possible: %s" % pre_event_shifts_possible)
        print("pre-event shifts scheduled: %d" % pre_event_shifts_scheduled)
        print("pre-event shifts required for wap: %d" % required_pre_event_shifts)
        print("main event shifts scheduled: %d" % main_event_shifts)
        print("qualifies for pre-event day off: %r" % qualifies_day_off)
        print("must work all pre-event dates: %r" % all_pre_event)
        print("WAP status: %r" % wap_status)
        if not wap_status:
            if not met_main_event_requirements:
                print("WAP False reason: required pre-event shifts are not equal to pre-event shifts scheduled")
            if not met_event_requirements:
                print("WAP False reason: required main-event shifts are not equal to main-event shifts scheduled")
        print("issue WAP Date: %s" % wap_date.strftime('%Y-%m-%d'))
        print(json.dumps(user_shifts, indent=2))
