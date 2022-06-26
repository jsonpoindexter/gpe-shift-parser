import wapstatus
from datetime import datetime

event_id = 47  # Babalooey event ID found by going to https://www.babalooey.com/dept/1/admin/reports/events and
# inspecting the dropdown list

pre_event_start = datetime.strptime('2022-08-06 00:00', '%Y-%m-%d %H:%M')  # Ignore shifts before this date
main_event_start = datetime.strptime('2022-08-28 00:00', '%Y-%m-%d %H:%M')  # Main event start shift date/time
earliest_wap_date = datetime.strptime('2022-08-16 00:00',
                                      '%Y-%m-%d %H:%M')  # Earliest date/time that a WAP can be given
day_off_date = datetime.strptime('2022-08-25 00:00',
                                 '%Y-%m-%d %H:%M')  # If your first day working is before the 25th you may take a day off during pre-event.
train_r_role_id = '2745'  # Refresh training does not count towards WAP
bar_role_id = '2726'  # Bar role does not count towards WAP
parent_ids = ['1mhIlvF8NjmhashXpssmIJjRVDpSfZKBk']  # Google Drive Parent folder ID

wapstatus = wapstatus.WapStatus(
    event_id,
    pre_event_start,
    main_event_start,
    earliest_wap_date,
    day_off_date,
    train_r_role_id,
    bar_role_id,
    parent_ids
)
wapstatus.run()
