import unittest
import json
import wapstatus
from collections import OrderedDict
from datetime import datetime

event_id = 47
pre_event_start = datetime.strptime('2022-08-06 00:00', '%Y-%m-%d %H:%M')  # Ignore shifts that start before this date
main_event_start = datetime.strptime('2022-08-28 00:00', '%Y-%m-%d %H:%M')  # Main event start shift date/time
earliest_wap_date = datetime.strptime('2022-08-16 00:00',
                                      '%Y-%m-%d %H:%M')  # Earliest date/time that a WAP can be given
day_off_date = datetime.strptime('2022-08-25 00:00',
                                 '%Y-%m-%d %H:%M')  # If your first day working is before the 25th you may take a day off during pre-event.
train_r_role_id = '2745'  # Refresh training does not count towards WAP
bar_role_id = '2726'  # Bar role does not count towards WAP
parent_ids = ['fakeId']  # Google Drive Parent folder ID


class TestUM(unittest.TestCase):
    # Tests
    # [] - User must work every day pre-event plus two shifts during event week.
    # [] - User starts shift on 1st main event day == gets WAP, no need for pre-event shifts
    # [] - If  first day working is before the 23rd you may take a day off during pre event.
    # [] - If first working shift is on the 23rd then you must work all 3 days Pre-Event (23, 24, 25).
    # [] - WAP / Credential date will be set one day before your first shift.
    # [] - The earliest work shift is August 18th, thus the earliest arrival is the 17th,
    # [] - Refresh training does count towards setting the date of your arrival and as 1 credit
    # [] - Bartender shifts DO NOT COUNT for an early entry.

    # User works 1 pre event shift, 0 main event == False wap status
    def test_10(self):

        wstatus = wapstatus.WapStatus(
            event_id,
            pre_event_start,
            main_event_start,
            earliest_wap_date,
            day_off_date,
            train_r_role_id,
            bar_role_id,
            parent_ids
        )

        grouped_shifts = [[
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-20 18:00',
                'Shift End': '2022-08-21 00:00',
            },
        ]]

        result = OrderedDict()
        result['User ID'] = grouped_shifts[0][0]['User ID']
        result['User Nickname'] = grouped_shifts[0][0]['User Nickname']
        result['WAP Status'] = False
        result['WAP Issue Date'] = '2022-08-18'
        result['First shift day scheduled'] = '2022-08-20 18:00'
        result['Pre-Event Shifts Possible'] = 8
        result['Pre-event shifts scheduled'] = 1
        result['Qualifies for Pre-event day off'] = True
        result['Pre-event shifts required for WAP'] = 7
        result['Main-event shifts scheduled'] = 0
        result['Must work all pre-event dates'] = False

        self.assertEqual(wstatus.determine_wap_status(grouped_shifts)[0], result)

    # User works all pre-event shifts, 0 main event == False wap status
    def test_11(self):

        wstatus = wapstatus.WapStatus(
            event_id,
            pre_event_start,
            main_event_start,
            earliest_wap_date,
            day_off_date,
            train_r_role_id,
            bar_role_id,
            parent_ids
        )

        grouped_shifts = [[
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-20 18:00',
                'Shift End': '2022-08-21 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-21 18:00',
                'Shift End': '2022-08-22 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-22 18:00',
                'Shift End': '2022-08-23 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-23 18:00',
                'Shift End': '2022-08-24 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-24 18:00',
                'Shift End': '2022-08-25 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-25 18:00',
                'Shift End': '2022-08-26 00:00',
            },
        ]]

        result = OrderedDict()
        result['User ID'] = grouped_shifts[0][0]['User ID']
        result['User Nickname'] = grouped_shifts[0][0]['User Nickname']
        result['WAP Status'] = False
        result['WAP Issue Date'] = '2022-08-18'
        result['First shift day scheduled'] = '2022-08-20 18:00'
        result['Pre-Event Shifts Possible'] = 8
        result['Pre-event shifts scheduled'] = 6
        result['Qualifies for Pre-event day off'] = True
        result['Pre-event shifts required for WAP'] = 7
        result['Main-event shifts scheduled'] = 0
        result['Must work all pre-event dates'] = False

        self.assertEqual(wstatus.determine_wap_status(grouped_shifts)[0], result)

    # Test that user event shifts before pre_event_start are not counted
    def test_12(self):
        wstatus = wapstatus.WapStatus(
            event_id,
            pre_event_start,
            main_event_start,
            earliest_wap_date,
            day_off_date,
            train_r_role_id,
            bar_role_id,
            parent_ids
        )

        grouped_shifts = [[
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-05 10:00',
                'Shift End': '2022-08-05 11:00',
            },
        ]]

        result = []

        self.assertEqual(wstatus.determine_wap_status(grouped_shifts), result)

    # Test that user event shifts before pre_event_start are not counted but after pre_event_start are counted
    def test_13(self):
        wstatus = wapstatus.WapStatus(
            event_id,
            pre_event_start,
            main_event_start,
            earliest_wap_date,
            day_off_date,
            train_r_role_id,
            bar_role_id,
            parent_ids
        )

        grouped_shifts = [[
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-05 10:00',
                'Shift End': '2022-08-05 11:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-20 18:00',
                'Shift End': '2022-08-21 00:00',
            },
        ]]

        expected_result = OrderedDict()
        expected_result['User ID'] = grouped_shifts[0][0]['User ID']
        expected_result['User Nickname'] = grouped_shifts[0][0]['User Nickname']
        expected_result['WAP Status'] = False
        expected_result['WAP Issue Date'] = '2022-08-18'
        expected_result['First shift day scheduled'] = '2022-08-20 18:00'
        expected_result['Pre-Event Shifts Possible'] = 8
        expected_result['Pre-event shifts scheduled'] = 1
        expected_result['Qualifies for Pre-event day off'] = True
        expected_result['Pre-event shifts required for WAP'] = 7
        expected_result['Main-event shifts scheduled'] = 0
        expected_result['Must work all pre-event dates'] = False

        result = wstatus.determine_wap_status(grouped_shifts)[0]
        self.assertEqual(result['WAP Status'], expected_result['WAP Status'])
        self.assertEqual(result['WAP Issue Date'], expected_result['WAP Issue Date'])
        self.assertEqual(result['Pre-Event Shifts Possible'], expected_result['Pre-Event Shifts Possible'])
        self.assertEqual(result['Pre-event shifts scheduled'], expected_result['Pre-event shifts scheduled'])
        self.assertEqual(result['Qualifies for Pre-event day off'], expected_result['Qualifies for Pre-event day off'])
        self.assertEqual(result['Pre-event shifts required for WAP'], expected_result['Pre-event shifts required for WAP'])
        self.assertEqual(result['Main-event shifts scheduled'], expected_result['Main-event shifts scheduled'])
        self.assertEqual(result['Must work all pre-event dates'], expected_result['Must work all pre-event dates'])

    # Test that user event shifts before pre_event_start are not counted but after pre_event_start and main event shifts are counted
    def test_13(self):
        wstatus = wapstatus.WapStatus(
            event_id,
            pre_event_start,
            main_event_start,
            earliest_wap_date,
            day_off_date,
            train_r_role_id,
            bar_role_id,
            parent_ids
        )

        grouped_shifts = [[
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-05 10:00',
                'Shift End': '2022-08-05 11:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-20 18:00',
                'Shift End': '2022-08-21 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-28 06:00',
                'Shift End': '2022-08-28 12:00',
            },
        ]]

        expected_result = OrderedDict()
        expected_result['User ID'] = grouped_shifts[0][0]['User ID']
        expected_result['User Nickname'] = grouped_shifts[0][0]['User Nickname']
        expected_result['WAP Status'] = False
        expected_result['WAP Issue Date'] = '2022-08-18'
        expected_result['First shift day scheduled'] = '2022-08-20 18:00'
        expected_result['Pre-Event Shifts Possible'] = 8
        expected_result['Pre-event shifts scheduled'] = 1
        expected_result['Qualifies for Pre-event day off'] = True
        expected_result['Pre-event shifts required for WAP'] = 7
        expected_result['Main-event shifts scheduled'] = 1
        expected_result['Must work all pre-event dates'] = False

        result = wstatus.determine_wap_status(grouped_shifts)[0]
        self.assertEqual(result['WAP Status'], expected_result['WAP Status'])
        self.assertEqual(result['WAP Issue Date'], expected_result['WAP Issue Date'])
        self.assertEqual(result['Pre-Event Shifts Possible'], expected_result['Pre-Event Shifts Possible'])
        self.assertEqual(result['Pre-event shifts scheduled'], expected_result['Pre-event shifts scheduled'])
        self.assertEqual(result['Qualifies for Pre-event day off'], expected_result['Qualifies for Pre-event day off'])
        self.assertEqual(result['Pre-event shifts required for WAP'], expected_result['Pre-event shifts required for WAP'])
        self.assertEqual(result['Main-event shifts scheduled'], expected_result['Main-event shifts scheduled'])
        self.assertEqual(result['Must work all pre-event dates'], expected_result['Must work all pre-event dates'])

    # Test that user who works on main_event_start has WAP status of True and is issued 2 days before main_event_start
    def test_14(self):
        wstatus = wapstatus.WapStatus(
            event_id,
            pre_event_start,
            main_event_start,
            earliest_wap_date,
            day_off_date,
            train_r_role_id,
            bar_role_id,
            parent_ids
        )

        grouped_shifts = [[
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2022-08-28 06:00',
                'Shift End': '2022-08-28 12:00',
            },
        ]]

        expected_result = OrderedDict()
        expected_result['User ID'] = grouped_shifts[0][0]['User ID']
        expected_result['User Nickname'] = grouped_shifts[0][0]['User Nickname']
        expected_result['WAP Status'] = True
        expected_result['WAP Issue Date'] = '2022-08-26'
        expected_result['First shift day scheduled'] = '2022-08-28 06:00'
        expected_result['Pre-Event Shifts Possible'] = 0
        expected_result['Pre-event shifts scheduled'] = 0
        expected_result['Qualifies for Pre-event day off'] = False
        expected_result['Pre-event shifts required for WAP'] = 0
        expected_result['Main-event shifts scheduled'] = 1
        expected_result['Must work all pre-event dates'] = False

        result = wstatus.determine_wap_status(grouped_shifts)[0]
        self.assertEqual(result['WAP Status'], expected_result['WAP Status'])
        self.assertEqual(result['WAP Issue Date'], expected_result['WAP Issue Date'])
        self.assertEqual(result['Pre-Event Shifts Possible'], expected_result['Pre-Event Shifts Possible'])
        self.assertEqual(result['Pre-event shifts scheduled'], expected_result['Pre-event shifts scheduled'])
        self.assertEqual(result['Qualifies for Pre-event day off'], expected_result['Qualifies for Pre-event day off'])
        self.assertEqual(result['Pre-event shifts required for WAP'], expected_result['Pre-event shifts required for WAP'])
        self.assertEqual(result['Main-event shifts scheduled'], expected_result['Main-event shifts scheduled'])
        self.assertEqual(result['Must work all pre-event dates'], expected_result['Must work all pre-event dates'])

    def determin_training_credits(self,
                                  pre_event_shifts,
                                  main_event_shifts,
                                  pre_event_train_r,
                                  main_event_train_r
                                  ):
        if (pre_event_train_r + main_event_train_r) > 1:  # either pre/main event shifts > 1
            # even
            if pre_event_train_r == main_event_train_r:
                pre_event_shifts -= pre_event_train_r - 1
                main_event_shifts -= main_event_train_r

            # pre-event > main-event
            if pre_event_train_r > main_event_train_r:
                pre_event_shifts -= pre_event_train_r - 1
                main_event_shifts -= main_event_train_r
            # pre-vent < main-event
            if pre_event_train_r < main_event_train_r:
                main_event_shifts -= main_event_train_r - 1
        return pre_event_shifts, main_event_shifts

    def test_1(self):  # no training session
        self.assertEqual(self.determin_training_credits(1, 1, 0, 0), (1, 1))

    def test_2(self):  # pre-event train: 1 main-event train: 0
        self.assertEqual(self.determin_training_credits(1, 1, 1, 0), (1, 1))

    def test_3(self):  # pre-event train: 0 main-event train: 1
        self.assertEqual(self.determin_training_credits(1, 1, 0, 1), (1, 1))

    def test_4(self):  # pre-event train: 2 main-event train: 0
        self.assertEqual(self.determin_training_credits(2, 1, 2, 0), (1, 1))

    def test_5(self):  # pre-event train: 0 main-event train: 2
        self.assertEqual(self.determin_training_credits(1, 2, 0, 2), (1, 1))

    def test_6(self):  # pre-event train: 2 main-event train: 2
        self.assertEqual(self.determin_training_credits(2, 2, 2, 2), (1, 0))

    def test_7(self):  # pre-event train: 2 main-event train: 2
        self.assertEqual(self.determin_training_credits(3, 2, 2, 2), (2, 0))

    def test_8(self):  # pre-event train: 2 main-event train: 2
        self.assertEqual(self.determin_training_credits(3, 2, 3, 2), (1, 0))

    def test_9(self):  # pre-event train: 2 main-event train: 2
        self.assertEqual(self.determin_training_credits(2, 2, 2, 0), (1, 2))


if __name__ == '__main__':
    unittest.main()
