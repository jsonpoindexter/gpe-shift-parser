import wapstatus
from datetime import datetime

event_id = 38

main_event_start = datetime.strptime('2022-08-15 00:00', '%Y-%m-%d %H:%M')  # Main event start shift date/time
main_start_event_end = datetime.strptime('2022-08-27 23:00', '%Y-%m-%d %H:%M')
earliest_wap_date = datetime.strptime('2022-08-16 00:00',
                                      '%Y-%m-%d %H:%M')  # Earliest date/time that a WAP can be given
day_off_date = datetime.strptime('2022-08-25 00:00',
                                 '%Y-%m-%d %H:%M')  # If your first day working is before the 25rd you may take a day off during pre-event.
train_r_role_id = '2745'  # User WAP/Credits should only count 1 training (even if 1+ scheduled)
bar_role_id = '2726'
parent_ids = ['1VJvc4riiDHdTDQhVGRGlQKH93DxQwOG6'] # Google Drive Parent folder ID

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
