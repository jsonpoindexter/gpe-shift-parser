import requests
import sys
import csv
import itertools
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from operator import itemgetter
from contextlib import closing


# Possible API Args
# a => arguments
# i => id?
# o => options
# g =>
# p => ?
# s => start_date
# e => end_date

# EventId: 31 => 2018 - I Robot

class Babalooey:

    """
        Web Client for Babalooey.

        Example::
            import client
            c = client.Babalooey('EMAIL,'PASSWORD')
            print(c.get_profile())
    """

    def __init__(self, username, password):
        self.cookies = self.login(username, password)

    @staticmethod
    def login(username, password):  # Login, save cookies
        url = 'https://www.babalooey.com'
        res = requests.post(url)
        cookies = res.cookies

        url = 'https://www.babalooey.com/login.php'
        params = {
            'email': username,
            'password': password
        }
        res = requests.post(url, params=params, cookies=cookies, verify=False)
        if "Invalid Username or Password" in res.text:
            sys.exit('Error: Invalid Username or Password')

        return cookies

    # Get profile info for loggedin user
    def get_profile(self):
        url = 'https://www.babalooey.com/request.php'
        params = {
            'a': 'g',
            'o': 'users',
            'i': '-1',
            'd': '1'
        }
        res = requests.post(url, params=params, cookies=self.cookies)
        if "Invalid Username or Password" in res.text:
            sys.exit('Error: Invalid Username or Password')

        return res.json()

    # Get department info
    def get_department_info(self, id):
        url = 'https://www.babalooey.com/request.php'
        params = {
            'a': 'g',
            'o': 'deptgroups',
            'i': id
        }
        res = requests.post(url, params=params, cookies=self.cookies)
        if "Invalid Username or Password" in res.text:
            sys.exit('Error: Invalid Username or Password')

        return res.json()

    # Get event info
    def get_event_info(self, id):
        url = 'https://www.babalooey.com/request.php'
        params = {
            'a': 'g',
            'o': 'events',
            'i': id
        }
        res = requests.post(url, params=params, cookies=self.cookies)
        if "Invalid Username or Password" in res.text:
            sys.exit('Error: Invalid Username or Password')

        return res.json()

    # Get roles for department
    def get_roles_for_department(self, id):
        url = 'https://www.babalooey.com/request.php'
        params = {
            'a': 'g',
            'o': 'roles',
            'i': id,
            'p': 'w'
        }
        res = requests.post(url, params=params, cookies=self.cookies)
        if "Invalid Username or Password" in res.text:
            sys.exit('Error: Invalid Username or Password')

        return res.json()

    # Get shifts for department
    def get_shifts_for_department(self, id, start_date, end_date):
        url = 'https://www.babalooey.com/request.php'
        params = {
            'a': 'g',
            'o': 'shifts',
            'i': id,
            's': start_date,
            'e': end_date,
            'g': id
        }
        res = requests.post(url, params=params, cookies=self.cookies)
        if "Invalid Username or Password" in res.text:
            sys.exit('Error: Invalid Username or Password')

        return res.json()

    # Fetch a report (csv)
    def get_report(self, type, data):
        url = 'https://www.babalooey.com/dept/1/admin/reports/%s' % type
        rows = []
        with closing(requests.post(url, stream=True, cookies=self.cookies, data=data)) as r:
            reader = csv.DictReader(r.iter_lines(), delimiter=',', quotechar='"')
            for row in reader:
                rows.append(row)
        return rows

    # Gets all shifts available for event(id), filled or not
    # Returns List of Shifts(Dict) Grouped(List) by User ID
    def get_event_report(self, id):
        data = {
            'eventid': id,
            'submit': 'Download'
        }

        shifts = self.get_report("events", data)

        grouped_shifts = []
        for key, value in itertools.groupby(shifts, key=itemgetter(
                'User ID')):  # Group shifts into Lists of Dictionaries by User Id
            user_shifts = []
            for user_shift in value:
                user_shifts.append(user_shift)
            grouped_shifts.append(user_shifts)

        return grouped_shifts

    # Get all users
    def get_user_list(self, id):
        data = {
            'filterEventID': id,
            'submit': 'Download'
        }
        return self.get_report("userlist", data)

    # Get all users with summary of scheduled and worked shifts
    def get_user_shifts_summary(self, id):
        data = {
            'filterUsers': 'on',
            'filterEventID': id,
            'submit': 'Download'
        }
        return self.get_report("userlist", data)
