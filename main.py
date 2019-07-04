import wapstatus
from datetime import datetime

event_id = 38

main_event_start = datetime.strptime('2019-08-25 00:00', '%Y-%m-%d %H:%M')  # Main event start shift date/time
main_start_event_end = datetime.strptime('2019-08-26 00:00', '%Y-%m-%d %H:%M')
earliest_wap_date = datetime.strptime('2019-08-16 00:00',
                                      '%Y-%m-%d %H:%M')  # Earliest date/time that a WAP can be given
day_off_date = datetime.strptime('2019-08-22 00:00',
                                 '%Y-%m-%d %H:%M')  # If your first day working is before the 23rd you may take a day off during pre-event.
train_r_role_id = '2200'  # User WAP/Credits should only count 1 training (even if 1+ scheduled)
bar_role_id = '2184'

wapstatus = wapstatus.WapStatus(
    event_id,
    main_event_start,
    main_start_event_end,
    earliest_wap_date,
    day_off_date,
    train_r_role_id,
    bar_role_id
)
wapstatus.run()