import csv
# from collections import defaultdict
import itertools
from operator import itemgetter
from datetime import datetime

main_event_start = datetime.strptime('2018-08-26 00:00', '%Y-%m-%d %H:%M')

reader = csv.DictReader(open('2018 - I, Robot-2018-07-27.csv'))

shifts = []
for shift in reader:
    if shift['User ID'] is not None and shift['User ID'].strip() is not "":
        shifts.append(shift)

shifts = sorted(shifts, key=itemgetter('User ID'))

grouped_shifts = []
for key, value in itertools.groupby(shifts, key=itemgetter('User ID')):
    user_shifts = []
    for user_shift in value:
        user_shifts.append(user_shift)
    grouped_shifts.append(user_shifts)

for user_shifts in grouped_shifts:

    first_shift = min([datetime.strptime(shift['Shift Start'],  '%Y-%m-%d %H:%M') for shift in user_shifts])
    pre_event_shifts_possible = []
    pre_event_shifts_worked = []
    main_event_shifts = []
    for shift in user_shifts:
        if shift['User Nickname'] == 'Dino':
            if datetime.strptime(shift['Shift End'], '%Y-%m-%d %H:%M') < main_event_start:   # Get all shifts worked before main event
                pre_event_shifts_worked.append(shift)
            if datetime.strptime(shift['Shift Start'], '%Y-%m-%d %H:%M') > main_event_start:  # Get all shifts worked during main event
                main_event_shifts.append(shift)
        shift_count = len(pre_event_shifts_worked) + len(main_event_shifts)
    if shift_count > 0:
        print("first shift day worked: %s" % str(first_shift))
        print("pre event shifts possible: %s" % (main_event_start - first_shift).days)
        print("pre event shifts worked: %d" % len(pre_event_shifts_worked))
        print("main event shifts worked: %d" % len(main_event_shifts))
