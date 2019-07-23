import csv
import itertools
import urllib
import babalooey
import json
import time
from pg import DB
from operator import itemgetter
from datetime import datetime, timedelta
from collections import OrderedDict
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


class WapStatus:
    def __init__(self, event_id, main_event_start, main_start_event_end, earliest_wap_date, day_off_date, train_r_role_id, bar_role_id):
        self.event_id = event_id
        self.main_event_start = main_event_start
        self.main_start_event_end = main_start_event_end
        self.earliest_wap_date = earliest_wap_date
        self.day_off_date = day_off_date
        self.train_r_role_id = train_r_role_id
        self.bar_role_id = bar_role_id
        self.db = DB(dbname='wap_test', host='localhost', port=5432, user='postgres', passwd='postgres')

    def determine_wap_status(self, grouped_shifts):
        wap_results = list()
        for user_shifts in grouped_shifts:
            if user_shifts[0]['User ID'].strip() is not "": # ignore unassigned shifts
                first_shift_date = min([datetime.strptime(shift['Shift Start'], '%Y-%m-%d %H:%M') for shift in
                                        user_shifts])  # Determine first scheduled shift
                wap_date = max(self.earliest_wap_date, first_shift_date - timedelta(days=1))  # Determine earliest WAP date
                pre_event_shifts_possible = max((self.main_event_start - first_shift_date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)).days,
                                                0)  # Determine how many possible pre-event shifts can be worked
                qualifies_day_off = first_shift_date < self.day_off_date  # If first day working is before the 23rd user may take a day off during pre-event.
                all_pre_event = self.day_off_date <= first_shift_date < self.main_event_start  # If first working shift is on the 23rd then user must work all 3 days Pre-Event (23, 24, 25).

                pre_event_shifts = []
                main_event_shifts = []
                pre_event_train_r = 0
                main_event_train_r = 0

                for shift in user_shifts:
                    if shift['Role ID'] == self.bar_role_id:
                        continue
                    if datetime.strptime(shift['Shift End'],
                                        '%Y-%m-%d %H:%M') <= self.main_event_start:  # Get all shifts scheduled before main event
                        pre_event_shifts.append(shift)
                        if shift['Role ID'] == self.train_r_role_id:
                            pre_event_train_r += 1

                    if datetime.strptime(shift['Shift Start'],
                                        '%Y-%m-%d %H:%M') >= self.main_event_start:  # Get all shifts scheduled during main event
                        main_event_shifts.append(shift)
                        if shift['Role ID'] == self.train_r_role_id:
                            main_event_train_r += 1

                shift_count = len(pre_event_shifts) + len(main_event_shifts)
                main_event_shifts = len(main_event_shifts)
                pre_event_shifts = len(pre_event_shifts)

                if (pre_event_train_r + main_event_train_r) > 1:
                    if pre_event_train_r == main_event_train_r:
                        pre_event_shifts -= pre_event_train_r - 1
                        main_event_shifts -= main_event_train_r
                    if pre_event_train_r > main_event_train_r:
                        pre_event_shifts -= pre_event_train_r - 1
                        main_event_shifts -= main_event_train_r
                    if pre_event_train_r < main_event_train_r:
                        main_event_shifts -= main_event_train_r - 1

                # Determine how many pre-event shifts need to be worked based on previous variables
                if qualifies_day_off:
                    required_pre_event_shifts = pre_event_shifts_possible - 1
                elif all_pre_event:
                    required_pre_event_shifts = pre_event_shifts_possible
                else:
                    required_pre_event_shifts = 0

                met_main_event_requirements = main_event_shifts >= 2
                met_pre_event_requirements = pre_event_shifts >= required_pre_event_shifts

                wap_status = met_main_event_requirements and met_pre_event_requirements and (first_shift_date <= self.main_start_event_end)

                result = OrderedDict()
                result['User ID'] = user_shifts[0]['User ID']
                result['User Nickname'] = user_shifts[0]['User Nickname']
                result['WAP Status'] = wap_status
                result['WAP Issue Date'] = wap_date.strftime('%Y-%m-%d')
                result['First shift day scheduled'] = first_shift_date.strftime('%Y-%m-%d %H:%M')
                result['Pre-Event Shifts Possible'] = pre_event_shifts_possible
                result['Pre-event shifts scheduled'] = pre_event_shifts
                result['Qualifies for Pre-event day off'] = qualifies_day_off
                result['Pre-event shifts required for WAP'] = required_pre_event_shifts
                result['Main-event shifts scheduled'] = main_event_shifts
                result['Must work all pre-event dates'] = all_pre_event
                result['Pre Event Training-Refresh Shifts'] = pre_event_train_r
                result['Main Event Training-Refresh Shifts'] = main_event_train_r
                wap_results.append(result)

        return wap_results

    def check_last_wap(self, wap_results):
        changedToTrueWap = list()
        changedToFalseWap = list()
        newTrueWap = list()
        for wap_result in wap_results:
            prev_wap_result = self.db.query("""
                select * from (
                    select
                        id,
                        timestamp,
                        status,
                        row_number() over(partition by id order by timestamp desc) as rn
                    from
                        wap_results
                ) t
                where t.rn = 1 AND t.id = $1
            """, wap_result['User ID']).getresult()
            if prev_wap_result:
                if prev_wap_result[0][2] != wap_result['WAP Status']:
                    if wap_result['WAP Status'] == True:
                        changedToTrueWap.append(wap_result)
                    else:
                        changedToFalseWap.append(wap_result)
            else:
                if wap_result['WAP Status'] == True:
                    newTrueWap.append(wap_result)
        return (newTrueWap, changedToTrueWap, changedToFalseWap)

    def insert_into_db(self, wap_results):
        for wap_result in wap_results:
            self.db.insert('wap_results',
                id = wap_result['User ID'],
                nickname = wap_result['User Nickname'],
                status = wap_result['WAP Status'] ,
                issue_date = wap_result['WAP Issue Date'],
                first_day = wap_result['First shift day scheduled'],
                pre_event_shifts_possible = wap_result['Pre-Event Shifts Possible'],
                pre_event_shifts_scheduled = wap_result['Pre-event shifts scheduled'],
                pre_event_day_off = wap_result['Qualifies for Pre-event day off'],
                pre_event_shifts_required = wap_result['Pre-event shifts required for WAP'],
                main_event_shifts_scheduled = wap_result['Main-event shifts scheduled'],
                work_all_pre_event_days = wap_result['Must work all pre-event dates'],
                pre_event_training_refresh_shifts = wap_result['Pre Event Training-Refresh Shifts'],
                main_event_training_refresh_shifts = wap_result['Main Event Training-Refresh Shifts'])

    def export_to_csv(self, wap_results):
        keys = wap_results[0].keys()
        filename = 'wap_results-' + time.strftime("%Y%m%d-%H%M%S") + '.csv'
        scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        gc = gspread.authorize(credentials)

        sh = gc.create("test1234")
        sh.share('jackyfryers@gmail.com', perm_type='user', role='writer')
        # with open(filename, 'wb') as output_file:  # TODO: a way to not convert to csv?
        #     dict_writer = csv.DictWriter(output_file, keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(wap_results)

    def run(self):
        file = open("babalooey-cred")
        baballooey_cred = file.read().split(',')
        client = babalooey.Babalooey(baballooey_cred[0], baballooey_cred[1])
        grouped_shifts = client.get_event_report(self.event_id)
        wap_results = self.determine_wap_status(grouped_shifts)
        (newTrueWap, changedToTrueWap, changedToFalseWap) = self.check_last_wap(wap_results)
        self.insert_into_db(wap_results)
        self.export_to_csv()
        print('changedToFalseWap:', changedToFalseWap)
        print('changedToTrueWap:', changedToTrueWap)
        print('newTrueWap:', newTrueWap)
        self.db.close()



