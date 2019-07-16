# gpe-shift-parser
Parse shifts from CSV and put them in a google sheets document.

# Requirements
* Python 2
`pip install urllib2`
`CREATE DATABASE wap;`
```
CREATE TABLE wap_results (
   id INT NOT NULL,
   nickname TEXT NOT NULL,
   status BOOLEAN NOT NULL,
   issue_date DATE NOT NULL,
   first_day DATE NOT NULL,
   pre_event_shifts_possible INT NOT NULL,
   pre_event_shifts_scheduled INT NOT NULL,
   pre_event_day_off BOOLEAN NOT NULL,
   pre_event_shifts_required INT NOT NULL,
   main_event_shifts_scheduled INT NOT NULL,
   work_all_pre_event_days BOOLEAN NOT NULL,
   pre_event_training_refresh_shifts INT NOT NULL,
   main_event_training_refresh_shifts INT NOT NULL,
   timestamp timestamp default current_timestamp
);
```

# Run
`python main.py`
