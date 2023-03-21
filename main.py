import datetime

def str_to_datetime(s):
    split=s.split('-')
    year, month, day = int(split[0]), int(split[1]), int(split[2])
    return datetime.datetime(year=year, month=month, day=day)

obj = str_to_datetime('2001-10-5')
print(obj)
