import csv
# from collections import defaultdict
import itertools
from operator import itemgetter

main_event_start = '2018-08-26 00:00'

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
