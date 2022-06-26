import csv, itertools, urllib, babalooey, json, time, sys
# from pg import DB
from operator import itemgetter
from datetime import datetime, timedelta
from collections import OrderedDict
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


class WapStatus:
    def __init__(self, event_id, pre_event_start, main_event_start, earliest_wap_date, day_off_date, train_r_role_id,
                 bar_role_id,
                 parent_ids):
        self.event_id = event_id
        self.pre_event_start = pre_event_start
        self.main_event_start = main_event_start
        self.main_start_event_end = main_event_start + timedelta(days=1)
        self.earliest_wap_date = earliest_wap_date
        self.day_off_date = day_off_date
        self.train_r_role_id = train_r_role_id
        self.bar_role_id = bar_role_id
        self.parent_ids = parent_ids
        # self.db = DB(dbname='wap_test', host='localhost', port=5432, user='postgres', passwd='postgres')

    def determine_wap_status(self, grouped_shifts):
        wap_results = list()
        for user_shifts in grouped_shifts:
            if user_shifts[0]['User ID'].strip() is "":
                continue  # ignore unassigned shifts

            #  Filter out shifts that are before pre_event_start or are for shift roles that don't count towards WAP
            valid_shifts = []
            for shift in itertools.ifilter(
                    lambda shift: datetime.strptime(
                        shift['Shift Start'], '%Y-%m-%d %H:%M') > self.pre_event_start and
                                  shift['Role ID'] != self.bar_role_id and
                                  shift['Role ID'] != self.train_r_role_id,
                    user_shifts):
                valid_shifts.append(shift)
            if not valid_shifts:
                continue

            first_shift_date = min([datetime.strptime(shift['Shift Start'], '%Y-%m-%d %H:%M') for shift in
                                    valid_shifts])  # Determine first scheduled shift
            wap_date = max(self.earliest_wap_date,
                           first_shift_date - timedelta(days=2))  # Determine earliest WAP date
            pre_event_shifts_possible = max(
                (self.main_event_start - first_shift_date.replace(hour=0, minute=0, second=0, microsecond=0)).days,
                0)  # Determine how many possible pre-event shifts can be worked
            qualifies_day_off = first_shift_date < self.day_off_date  # If first day working is before the day_off_date user may potentially take a day off during pre-event.
            all_pre_event = self.day_off_date <= first_shift_date < self.main_event_start  # If first working shift is on the day_off_date then user must work all 3 days Pre-Event (23, 24, 25).

            pre_event_shifts = []
            main_event_shifts = []

            for shift in valid_shifts:
                if datetime.strptime(shift['Shift End'],
                                     '%Y-%m-%d %H:%M') <= self.main_event_start:  # Get all shifts scheduled before main event
                    pre_event_shifts.append(shift)

                if datetime.strptime(shift['Shift Start'],
                                     '%Y-%m-%d %H:%M') >= self.main_event_start:  # Get all shifts scheduled during main event
                    main_event_shifts.append(shift)

            shift_count = len(pre_event_shifts) + len(main_event_shifts)
            main_event_shifts = len(main_event_shifts)
            pre_event_shifts = len(pre_event_shifts)

            # Determine how many pre-event shifts need to be worked based on previous variables
            if qualifies_day_off:
                required_pre_event_shifts = pre_event_shifts_possible - 1
            elif all_pre_event:
                required_pre_event_shifts = pre_event_shifts_possible
            else:
                required_pre_event_shifts = 0

            met_main_event_requirements = main_event_shifts >= 2
            met_pre_event_requirements = pre_event_shifts >= required_pre_event_shifts

            wap_status = met_main_event_requirements and met_pre_event_requirements and (
                    first_shift_date <= self.main_start_event_end)

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
                           id=wap_result['User ID'],
                           nickname=wap_result['User Nickname'],
                           status=wap_result['WAP Status'],
                           issue_date=wap_result['WAP Issue Date'],
                           first_day=wap_result['First shift day scheduled'],
                           pre_event_shifts_possible=wap_result['Pre-Event Shifts Possible'],
                           pre_event_shifts_scheduled=wap_result['Pre-event shifts scheduled'],
                           pre_event_day_off=wap_result['Qualifies for Pre-event day off'],
                           pre_event_shifts_required=wap_result['Pre-event shifts required for WAP'],
                           main_event_shifts_scheduled=wap_result['Main-event shifts scheduled'],
                           work_all_pre_event_days=wap_result['Must work all pre-event dates'])

    def export_to_csv(self, wap_results):
        keys = wap_results[0].keys()
        filename = 'wap_results-' + time.strftime("%Y%m%d-%H%M%S") + '.csv'

        with open(filename, 'wb') as output_file:  # TODO: a way to not convert to csv?
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(wap_results)
        output_file.close()

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        drive_service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': filename,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': self.parent_ids
        }
        media = MediaFileUpload(filename, mimetype='text/csv', resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        os.remove(filename)

    def run(self):
        file = open("babalooey-cred")
        babalooey_cred = file.read().split(',')
        client = babalooey.Babalooey(babalooey_cred[0], babalooey_cred[1])
        grouped_shifts = client.get_event_report(self.event_id)
        wap_results = self.determine_wap_status(grouped_shifts)
        # (newTrueWap, changedToTrueWap, changedToFalseWap) = self.check_last_wap(wap_results)
        # self.insert_into_db(wap_results)
        self.export_to_csv(wap_results)
        # print('changedToFalseWap:', changedToFalseWap)
        # print('changedToTrueWap:', changedToTrueWap)
        # print('newTrueWap:', newTrueWap)
        # self.db.close()
