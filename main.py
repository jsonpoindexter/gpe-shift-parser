import csv
import itertools
from operator import itemgetter
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
results = list()
for user_shifts in grouped_shifts:
    # print("")

    first_shift_date = min([datetime.strptime(shift['Shift Start'], '%Y-%m-%d %H:%M') for shift in
                            user_shifts])  # Deternube first scheduled shift
    wap_date = max(earliest_wap_date, first_shift_date - timedelta(days=1))  # Determine earliest WAP date
    pre_event_shifts_possible = max((main_event_start - first_shift_date).days + 1, 0)  # Determine how many possible pre-event shifts can be worked
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

    # print("User ID: %s" % user_shifts[0]['User ID'])
    # print("first shift day scheduled: %s" % str(first_shift_date))
    # print("pre-event shifts possible: %s" % pre_event_shifts_possible)
    # print("pre-event shifts scheduled: %d" % pre_event_shifts_scheduled)
    # print("pre-event shifts required for wap: %d" % required_pre_event_shifts)
    # print("main event shifts scheduled: %d" % main_event_shifts)
    # print("qualifies for pre-event day off: %r" % qualifies_day_off)
    # print("must work all pre-event dates: %r" % all_pre_event)
    # print("earliest WAP date: %s", wap_date.strftime("%Y-%m-%d"))
    # print("WAP status: %r" % wap_status)
    # if not wap_status:
    #     if not met_main_event_requirements:
    #         print("WAP False reason: required main-event shifts are not equal to main-event shifts scheduled")
    #     if not met_event_requirements:
    #         print("WAP False reason: required main-event shifts are not equal to main-event shifts scheduled")
    # print("issue WAP Date: %s" % wap_date.strftime('%Y-%m-%d'))
    # print(json.dumps(user_shifts, indent=2))


    results.append({
        'User ID': user_shifts[0]['User ID'],
        'User Nickname': user_shifts[0]['User Nickname'],
        'WAP Status': wap_status,
        'WAP Issue Date': wap_date.strftime('%Y-%m-%d'),
        "First shift day scheduled: ": str(first_shift_date),
        'Pre-Event Shifts Possible': pre_event_shifts_possible,
        'Pre-event shifts scheduled': pre_event_shifts_scheduled,
        'Qualifies for Pre-event day off':  qualifies_day_off,
        'Pre-event shifts required for WAP':  required_pre_event_shifts,
        'Main-event shifts scheduled':  main_event_shifts,
        'Must work all pre-event dates':  all_pre_event
    })


###### Export to CSV ######
keys = results[0].keys()
filename = 'wap_results_%s.csv' % datetime.now().strftime("%Y%m%d-%H%M%S")
with open(filename, 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name("GPE-WAP-Status-Test-740031faadf4.json", scope)

gc = gspread.authorize(credentials)

# Open a worksheet from spreadsheet with one shot
worksheet = gc.open("test").sheet1


fooboo =open(filename)
gc.import_csv("1zQ4I1vwBuoNNKdEYTfgiYXSiGXGXIRNdWrXdcVbxrR4", fooboo)
