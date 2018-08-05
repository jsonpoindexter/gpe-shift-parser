import unittest
import json
import wapstatus
from collections import OrderedDict
from datetime import datetime

event_id = 31

main_event_start = datetime.strptime('2018-08-26 00:00', '%Y-%m-%d %H:%M')  # Main event start shift date/time
main_start_event_end = datetime.strptime('2018-08-27 00:00', '%Y-%m-%d %H:%M')
earliest_wap_date = datetime.strptime('2018-08-17 00:00',
                                      '%Y-%m-%d %H:%M')  # Earliest date/time that a WAP can be given
day_off_date = datetime.strptime('2018-08-23 00:00',
                                 '%Y-%m-%d %H:%M')  # If your first day working is before the 23rd you may take a day off during pre-event.
train_r_role_id = '1755'  # User WAP/Credits should only count 1 training (even if 1+ scheduled)
bar_role_id = '1752'


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
            main_event_start,
            main_start_event_end,
            earliest_wap_date,
            day_off_date,
            train_r_role_id,
            bar_role_id
        )


        user_shifts = [
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2018-08-20 18:00',
                'Shift End': '2018-08-21 00:00',
            },
        ]

        result = OrderedDict()
        result['User ID'] = user_shifts[0]['User ID']
        result['User Nickname'] = user_shifts[0]['User Nickname']
        result['WAP Status'] = False
        result['WAP Issue Date'] = '2018-08-19'
        result['First shift day scheduled'] = '2018-08-20 18:00'
        result['Pre-Event Shifts Possible'] = 6
        result['Pre-event shifts scheduled'] = 1
        result['Qualifies for Pre-event day off'] = True
        result['Pre-event shifts required for WAP'] = 5
        result['Main-event shifts scheduled'] = 0
        result['Must work all pre-event dates'] = False
        result['Pre Event Training-Refresh Shifts'] = 0
        result['Main Event Training-Refresh Shifts'] = 0

        self.assertEqual(wstatus.determine_wap_status(user_shifts), result)

    # User works all pre-event shifts, 0 main event == False wap status
    def test_11(self):

        wstatus = wapstatus.WapStatus(
            event_id,
            main_event_start,
            main_start_event_end,
            earliest_wap_date,
            day_off_date,
            train_r_role_id,
            bar_role_id
        )


        user_shifts = [
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2018-08-20 18:00',
                'Shift End': '2018-08-21 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2018-08-21 18:00',
                'Shift End': '2018-08-22 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2018-08-22 18:00',
                'Shift End': '2018-08-23 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2018-08-23 18:00',
                'Shift End': '2018-08-24 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2018-08-24 18:00',
                'Shift End': '2018-08-25 00:00',
            },
            {
                'User ID': '6915',
                'User Nickname': 'Dino',
                'Role ID': '1781',
                'Shift Start': '2018-08-25 18:00',
                'Shift End': '2018-08-26 00:00',
            },
        ]

        result = OrderedDict()
        result['User ID'] = user_shifts[0]['User ID']
        result['User Nickname'] = user_shifts[0]['User Nickname']
        result['WAP Status'] = False
        result['WAP Issue Date'] = '2018-08-19'
        result['First shift day scheduled'] = '2018-08-20 18:00'
        result['Pre-Event Shifts Possible'] = 6
        result['Pre-event shifts scheduled'] = 6
        result['Qualifies for Pre-event day off'] = True
        result['Pre-event shifts required for WAP'] = 5
        result['Main-event shifts scheduled'] = 0
        result['Must work all pre-event dates'] = False
        result['Pre Event Training-Refresh Shifts'] = 0
        result['Main Event Training-Refresh Shifts'] = 0

        print(json.dumps(wstatus.determine_wap_status(user_shifts)))

        self.assertEqual(wstatus.determine_wap_status(user_shifts), result)


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
