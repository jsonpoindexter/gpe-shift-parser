import csv

reader = csv.DictReader(open('2018 - I, Robot-2018-07-27.csv'))

dict_list = []

for line in reader:
    dict_list.append(line)

print(dict_list[0])
