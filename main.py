import wapstatus
from datetime import datetime

event_id = 47  # Babalooey event ID found by going to https://www.babalooey.com/dept/1/admin/reports/events and
# inspecting the dropdown list

main_event_start = datetime.strptime('2022-08-28 00:00', '%Y-%m-%d %H:%M')  # Main event start shift date/time
main_start_event_end = datetime.strptime('2022-08-29 00:00', '%Y-%m-%d %H:%M')
earliest_wap_date = datetime.strptime('2022-08-18 00:00',
                                      '%Y-%m-%d %H:%M')  # Earliest date/time that a WAP can be given
day_off_date = datetime.strptime('2022-08-23 00:00',
                                 '%Y-%m-%d %H:%M')  # If your first day working is before the 24th you may take a day
# off during pre-event.
train_r_role_id = '2745'  # Refresh training does not count towards WAP
bar_role_id = '2726' # Bare role does not count towards WAP
parent_ids = ['PARENT_ID']  # Google Drive Parent folder ID

wapstatus = wapstatus.WapStatus(
    event_id,
    main_event_start,
    main_start_event_end,
    earliest_wap_date,
    day_off_date,
    train_r_role_id,
    bar_role_id,
    parent_ids
)
wapstatus.run()
